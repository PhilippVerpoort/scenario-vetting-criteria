The reference data is used by some [criteria thresholds](../criteria_thrsh).


```python exec="true" session="index" showcode="false"
import pandas as pd
from scenario_vetting_criteria import load_criteria
from IPython.display import display

reference_data, reference_srcs = load_criteria(['reference-data', 'reference-sources']).values()

print(
    reference_data
    .apply(lambda col: col.str.replace("|", "\|") if col.name == 'variable' else col)
    .rename(columns=lambda x: x.upper())
    .fillna('')
    .to_markdown(index=False)
)
```
