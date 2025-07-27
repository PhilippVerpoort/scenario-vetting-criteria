Each criterion comes with a set of threshold values that scenarios have to surpass in order to be assigned a specific level of concern in regards to this criterion.

The thresholds values come in three degrees of severity: medium concern, strong concern, and very strong concern. Different [operations](../operations) can be set depending on the degree of severity.

Some thresholds are defined in relation to some reference, as set by the `reference_source` column. The [reference data](../reference_data) is defined separately. The values defined as thresholds therefore have to be multiplied with the values from the reference data before applying the criteria to scenario data.


```python exec="true" session="index" showcode="false"
import pandas as pd
from scenario_vetting_criteria import load_criteria
from IPython.display import display

criteria_thrsh, criteria_meta = load_criteria(['criteria-thresholds', 'criteria-metadata']).values()

print(
    criteria_thrsh
    .assign(criterion=lambda df: df['criterion'].map({k: v['name'] for k, v in criteria_meta.items()}))
    .rename(columns=lambda x: x.upper().replace('_', ' '))
    .apply(lambda col: col.str.replace("|", "\|") if col.dtype == 'object' else col)
    .fillna('')
    .to_markdown(index=False)
)
```
