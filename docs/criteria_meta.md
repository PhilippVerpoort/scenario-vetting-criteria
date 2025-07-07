The criteria metadata contain contextual information about why certain criteria are necessary/relevant, and how threshold values are set. Moreover, each criterion has a [criteria type](../criteria_type) assigned to it.


```python exec="true" session="index" showcode="false"
import pandas as pd
from scenario_vetting_criteria import load_criteria
from scenario_vetting_criteria.formatting import format_sources, insert_citations
from IPython.display import display

criteria_meta, criteria_types, reference_srcs = load_criteria(['criteria-metadata', 'criteria-types', 'reference-sources']).values()
reference_srcs_formatted = format_sources(reference_srcs)

print(
    pd.DataFrame.from_dict(criteria_meta, orient='index')
    .reset_index(drop=True)
    .assign(
        type=lambda df: df['type'].map({k: v['name'] for k, v in criteria_types.items()}),
        justification_threshold=lambda df: df['justification_threshold'].apply(insert_citations, args=(reference_srcs_formatted, '../reference_srcs/')),
        justification_criterion=lambda df: df['justification_criterion'].apply(insert_citations, args=(reference_srcs_formatted, '../reference_srcs/')),
    )
    .rename(columns={
        'name': 'NAME',
        'type': 'TYPE',
        'justification_criterion': 'JUSTIFICATION OF THE CRITERION<br>(Why this criterion?)',
        'justification_threshold': 'JUSTIFICATION OF THE THRESHOLD<br>(Why this threshold?)'
    })
    .apply(lambda col: col.str.replace("\n", "<br>") if col.dtype == 'object' else col)
    .to_markdown(index=False)
)
```
