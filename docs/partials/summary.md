This page gives a criterion-by-criterion overview of all vetting criteria,
combining the scientific justifications with the computed threshold values.

```python exec="true" session="summary" showcode="false"
import pandas as pd
from itables import to_html_datatable
from scenario_vetting_criteria import load_criteria
from scenario_vetting_criteria.preprocessed import load_criteria_combined
from scenario_vetting_criteria.formatting import format_sources, insert_citations

edition = "{{ edition }}"

criteria_combined = load_criteria_combined(edition=edition).query("region == 'World'")
criteria_types, criteria_meta, sources = load_criteria(
    ["criteria-types", "criteria-metadata", "sources"],
    edition=edition,
).values()
sources_formatted = format_sources(sources)


def _fmt(text):
    """Insert citations and convert newlines to <br> for inline rendering."""
    return insert_citations(text, sources_formatted, "").replace("\n", "<br>")


def _pivot(df):
    """Pivot threshold_type (lower/upper) into side-by-side columns."""
    d = df.drop(columns="criterion").copy()
    # pivot_table drops rows where index values are NA; replace with empty
    # string so rows without a year constraint are preserved.
    d["year"] = d["year"].astype("object").where(d["year"].notna(), other="")
    pivoted = (
        d.pivot_table(
            index=["variable", "region", "year", "level_of_concern", "unit"],
            columns="threshold_type",
            values="value",
            aggfunc="first",
        )
        .rename_axis(None, axis=1)
        .reset_index()
    )
    col_order = ["variable", "region", "year", "unit", "level_of_concern", "lower", "upper"]
    return pivoted[[c for c in col_order if c in pivoted.columns]]


# Ordered list of criteria within the combined df (preserves CSV row order)
ordered_criteria = list(dict.fromkeys(criteria_combined["criterion"]))

for crit_type in criteria_types:
    type_criteria = [c for c in ordered_criteria if c.startswith(f"{crit_type}|")]
    if not type_criteria:
        continue

    print(f"## {crit_type}\n")

    for criterion in type_criteria:
        criterion_name = criterion.split("|", 1)[1]
        print(f"### {criterion_name}\n")

        meta = criteria_meta.get(criterion, {})
        if jc := meta.get("justification_criterion"):
            print(f"**Why this criterion?** {_fmt(jc)}\n")
        if jt := meta.get("justification_threshold"):
            print(f"**Why this threshold?** {_fmt(jt)}\n")

        df = _pivot(criteria_combined[criteria_combined["criterion"] == criterion].copy())
        table_html = to_html_datatable(df, connected=True, style="width:100%")
        print(f"<div>\n{table_html}\n</div>\n")

print("---\n\n## Sources\n")

df_srcs = pd.DataFrame.from_dict(sources_formatted, orient="index").reset_index()

{% raw %}

def _src_links(row):
    ret = []
    if row["url_doi"]:
        ret.append(
            "[ :simple-doi: DOI ]"
            f"({row['url_doi']})"
            "{ .sm-button } "
        )
    if row["url"] and (not row["doi"] or (row["doi"] == row["url_doi"])):
        ret.append(
            "[ :material-link-box: URL ]"
            f"({row['url']})"
            "{ .sm-button } "
        )
    if row["pdf"]:
        ret.append(
            "[ :fontawesome-solid-file-pdf: PDF ]"
            f"({row['pdf']})"
            "{ .sm-button } "
        )
    return "<br>".join(ret)

{% endraw %}

col1 = df_srcs["index"].apply(lambda r: f'<p id="{r}">`{r}`</p>').rename("Identifier")
col2 = df_srcs["bib"].rename("Bibliographic information")
col3 = df_srcs.apply(_src_links, axis=1).rename("Links")

print(
    pd.concat([col1, col2, col3], axis=1)
    .apply(lambda col: col.str.replace("|", "\\|").str.replace("\n", " "))
    .fillna("")
    .to_markdown(index=False)
)
```
