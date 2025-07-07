The reference sources contain bibliographic information for the data provided in the [reference data](../reference_data/) and in the justifications provided in the [criteria metadata](../criteria_meta/).


```python exec="true" session="index" showcode="false"
import pandas as pd
from scenario_vetting_criteria import load_criteria
from scenario_vetting_criteria.formatting import format_sources
from IPython.display import display

reference_srcs = load_criteria('reference-sources')
reference_srcs_formatted = format_sources(reference_srcs)

for ref_id, ref_data in reference_srcs_formatted.items():
    print(f"* <span id=\"{ref_id}\">[{ref_id}] {ref_data['bib']}</span>")
```
