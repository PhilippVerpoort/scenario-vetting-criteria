Operations are meant to determine the outcome of the procedure of scenario vetting. Vetted scenarios should either me dropped or assigned flags of different colours, as defined below.


```python exec="true" session="index" showcode="false"
import pandas as pd
from scenario_vetting_criteria import load_criteria
from IPython.display import display

operations, criteria_thrsh, criteria_meta, criteria_types = load_criteria(['operations', 'criteria-thresholds', 'criteria-metadata', 'criteria-types']).values()

print(
    pd.DataFrame.from_records(operations)
    .assign(
        criterion_type=lambda df: df['criterion_type'].map({k: v['name'] for k, v in criteria_types.items()}),
        threshold_severity=lambda df: df['level_of_concern'].str.replace('_', ' '),
        threshold_type=lambda df: df['threshold_type'].apply(', '.join),
    )
    .rename(columns=lambda x: x.upper().replace('_', ' '))
    .fillna('')
    .to_markdown(index=False)
)
```
