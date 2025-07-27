The reference data is used by some [criteria thresholds](../criteria_thrsh).


```python exec="true" session="index" showcode="false"
import pandas as pd
from scenario_vetting_criteria import load_criteria, ref_paths
from IPython.display import display

for source in ref_paths:
    print(f"## {source}\n\n")

    reference_data = load_criteria('reference-data', reference_subset=source)

    print(
        reference_data
        .apply(lambda col: col.str.replace("|", "\|") if col.name == 'variable' else col)
        .rename(columns=lambda x: x.upper())
        .fillna('')
        .to_markdown(index=False)
    )
    print("\n\n")
```
