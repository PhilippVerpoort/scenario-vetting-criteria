The reference data is used to define some of the [criteria thresholds](../criteria_thrsh). The identifiers used in the reference data column of the thresholds correspond to the identifiers of the reference data below.


```python exec="true" session="index" showcode="false"
import yaml

from scenario_vetting_criteria import load_criteria, ref_data_paths

from IPython.display import display


sources = load_criteria('sources')
sources_formatted = format_sources(sources)

for ref_data in ref_data_paths:
    reference_data = load_criteria('reference-data', reference_subset=ref_data).drop(columns='reference_data')
    reference_data_meta = load_criteria('reference-metadata', reference_subset=ref_data)[ref_data]

    source = reference_data_meta['source']
    source_cite = sources_formatted[source]['cite'] if source in sources_formatted else source
    description = reference_data_meta['description'].replace("{{source}}", f"[{source_cite}](/sources/#{source})")

    print(f"## {ref_data}\n\n")
    print(description)
    print("\n\n")
    print(
        reference_data
        .apply(lambda col: col.str.replace("|", "\|") if col.name == 'variable' else col)
        .rename(columns=lambda x: x.upper())
        .fillna('')
        .to_markdown(index=False)
    )
    print("\n\n")
```
