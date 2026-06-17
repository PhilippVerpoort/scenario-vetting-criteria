"""Preprocess criteria definitions for use with IAMC nomenclature package."""
import pandas as pd

from . import editions, load_criteria

try:
    import pycountry
except ImportError as ex:
    raise Exception("The `pycountry` package must be installed.")


def load_criteria_combined(edition: str | None = None) -> pd.DataFrame:
    """Load and combine criteria thresholds with reference data.

    Processes raw criteria definitions through six steps:
    melting bound types, exploding comma-separated fields, expanding
    ``All Countries``, resolving reference-data multipliers, and applying
    range/min/max operators across multiple sources.

    Parameters
    ----------
    edition : str, optional
        Define the edition of the criteria definition to load. If not
        provided, the latest edition will be used.

    Returns
    -------
    pd.DataFrame
        One row per (criterion, variable, region, year, level_of_concern,
        threshold_type) combination with columns ``value`` and ``unit``.

    """
    if edition is None:
        edition = list(editions)[-1]

    # Step 0: Load the raw criteria definitions.
    criteria_thrsh = load_criteria("criteria-thresholds", edition=edition)
    reference_data = load_criteria("reference-data", edition=edition)

    # Step 1: Melt threshold types (upper, lower) into column.
    criteria_step1 = (
        criteria_thrsh.melt(
            id_vars=[c for c in criteria_thrsh if c not in ["upper", "lower"]],
            value_vars=["upper", "lower"],
            var_name="threshold_type",
        )
        .dropna(subset="value")
    )

    # Step 2: Explode comma-separated values in variable, region, and year
    # columns.
    criteria_tmp = criteria_step1.copy()
    for col_name in ["variable", "region", "year"]:
        criteria_tmp[col_name] = criteria_tmp[col_name].str.split(",")
        criteria_tmp = criteria_tmp.explode(col_name)
        criteria_tmp[col_name] = criteria_tmp[col_name].str.strip()

    criteria_step2 = (
        criteria_tmp
        .reset_index(drop=True)
        .astype({"year": "Int64"})
    )

    # Step 3: Replace `All Countries` with country codes and explode.
    all_countries = (
        [country.alpha_3 for country in pycountry.countries] +
        ["KOS"]
    )
    criteria_step3 = (
        criteria_step2
        .assign(region=lambda df: df["region"].map(
            lambda r: all_countries if r == "All Countries" else r
        ))
        .explode("region")
        .reset_index(drop=True)
    )

    # Step 4: Explode sources.
    criteria_step4 = (
        pd.concat([
            # Extract operator and sources from column `reference_sources`.
            criteria_step3["reference_data"].str.extract(
                r"(?P<reference_multi_operator>[a-z]+)?"
                r"\(?(?P<reference_data>[^\)]+)\)?"
            ),
            # Combine with existing data.
            criteria_step3.drop(columns="reference_data"),
        ], axis=1)
        # Insert value `range` if operator is empty.
        .fillna({"reference_multi_operator": "range"})
        # Split list of sources by comma and expand.
        .assign(reference_data=lambda df: df["reference_data"].str.split(","))
        .explode("reference_data")
        .assign(reference_data=lambda df: df["reference_data"].str.strip())
        # Reset index.
        .reset_index(drop=True)
    )

    # Step 5: Merge with references list and compute absolute values.
    criteria_step5 = (
        criteria_step4
        # Merge with reference data.
        .merge(
            reference_data,
            on=["reference_data", "variable", "region", "year"],
        )
        # Assign new value and unit.
        .assign(
            value=lambda df: df.value_x * df.value_y,
            unit=lambda df: df.unit_y.fillna(df.unit_x),
        )
        # Combine with data that does not use a reference.
        .pipe(
            lambda df: pd.concat([
                df,
                criteria_step4.loc[criteria_step4["reference_data"].isnull()],
            ])
        )
        # Drop columns that are no longer needed.
        .drop(columns=[
            "value_x", "value_y",
            "unit_x", "unit_y",
            "reference_data",
        ])
        .reset_index(drop=True)
    )

    # Step 6: Apply operator for multiple sources.
    def combine(group):
        assert group["unit"].nunique() == 1, \
            "Unit must be the same across combined references."
        assert group["reference_multi_operator"].nunique() == 1, \
            "Operation must be the same across combined references."
        threshold_type = group.name[-1]
        # Determine operator
        operator = group["reference_multi_operator"].iloc[0]
        if operator == "range":
            operator = "min-max"
        if "-" in operator:
            operator = (
                operator
                .split("-")[["lower", "upper"]
                .index(threshold_type)]
            )
        # Apply operator and return.
        return pd.Series({
            "value": getattr(group["value"], operator)(),
            "unit": group["unit"].iloc[0],
        })

    return (
        criteria_step5
        .groupby([
            "criterion", "region", "year",
            "variable", "level_of_concern",
            "threshold_type",
        ], dropna=False)
        [["reference_multi_operator", "unit", "value"]]
        .apply(combine)
        .reset_index()
    )


def load_criteria_for_validator(edition: str | None = None) -> list[dict]:
    """Load criteria definitions for use with IAMC nomenclature validator.

    Parameters
    ----------
    edition : str, optional
        Define the edition of the criteria definition to load. If not
        provided, the latest edition will be used.

    Returns
    -------
    list[dict]
        Criteria definitions for use with IAMC nomenclature validator.

    """
    criteria_combined = load_criteria_combined(edition=edition)

    # Convert dataframe to list of nested dictionaries and return.
    return (
        criteria_combined
        .query("region=='World'")
        .rename(columns={
            "criterion": "name",
            "level_of_concern": "warning_level",
        })
        .assign(
            name=lambda df:
                df["name"]
                + ("|" + df["region"].astype(str))
                .where(df["region"].notna(), other="")
                + ("|" + df["year"].astype(str))
                .where(df["year"].notna(), other=""),
            threshold_type=lambda df: df["threshold_type"] + "_bound",
            warning_level=lambda df: df["warning_level"].map({
                "strong": "high",
                "medium": "medium",
            }),
        )
        .drop(columns="unit")
        .pivot(
            index=["name", "region", "year", "variable", "warning_level"],
            columns="threshold_type",
            values="value",
        )
        .reset_index()
        .groupby(["name", "region", "year", "variable"], dropna=False)
        [["warning_level", "upper_bound", "lower_bound"]]
        .apply(lambda df: list(df.apply(lambda row: row.to_dict(), axis=1)))
        .to_frame("validation")
        .reset_index()
        .apply(lambda row: row.dropna().to_dict(), axis=1)
        .tolist()
    )
