This page contains bibliographic information for the sources used for providing the [reference data](../reference_data/) and in the justifications given in the [criteria metadata](../criteria_meta/).


```python exec="true" session="index" showcode="false"
import pandas as pd
from scenario_vetting_criteria import load_criteria
from scenario_vetting_criteria.formatting import format_sources
from IPython.display import display

sources = load_criteria('sources')
sources_formatted = format_sources(sources, form='html')

for ref_id, ref_data in sources_formatted.items():
    print(f"* <span id=\"{ref_id}\">[<a href=\"../sources/#{ref_id}\">{ref_id}</a>] {ref_data['bib']}</span>")
```
