The reference data is used to define some of
the [criteria thresholds](../criteria_thrsh). The identifiers used in the
reference data column of the thresholds correspond to the identifiers of the
reference data below.

```python exec="true" session="index" showcode="false"
import yaml

from scenario_vetting_criteria import load_criteria

reference_data, reference_metadata, sources = load_criteria(
    ["reference-data", "reference-metadata", "sources"],
    release="{{ release }}",
).values()
sources_formatted = format_sources(sources)

for ref, df_ref in reference_data.groupby("reference_data"):
    source = reference_metadata[ref].get("source")
    source_cite = (
        sources_formatted[source]["cite"]
        if source in sources_formatted else
        source
    )
    description = reference_metadata[ref].get("description", "").replace(
        "{% raw %}{{source}}{% endraw %}",
        f"[{source_cite}](/sources/#{source})",
    )

    print(f"## `{ref}`\n\n")
    print(description)
    print("\n\n")
    print(
        df_ref
        .drop(columns="reference_data")
        .apply(
            lambda col: col.str.replace("|", "\|")
            if col.name == "variable" else
            col
        )
        .rename(columns=lambda x: x.upper())
        .fillna("")
        .to_markdown(index=False)
    )
    print("\n\n")
```
