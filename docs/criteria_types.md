All criteria defined are assigned a type from the list provided below. The types are used for meta information about criteria, but are also used to define [operations](../operations/).


```python exec="true" session="index" showcode="false"
import pandas as pd
from scenario_vetting_criteria import load_criteria
from IPython.display import display

criteria_types = load_criteria('criteria-types')

print(
    pd.DataFrame.from_dict(criteria_types, orient='index')
    .reset_index(drop=True)
    .rename(columns=lambda x: x.upper())
    .to_markdown(index=False)
)
```
