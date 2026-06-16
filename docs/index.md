{{ readme_section('## Background', '## Repository structure') }}

Currently, the following editions are available:

```python exec="true" session="index" showcode="false"
from scenario_vetting_criteria import editions
for i, edition in enumerate(reversed(editions)):
    print(f"* Edition {edition}" + ("(latest)" if not i else ""))
```

## Components
Each edition contains the following components:

* Types — Distinguishes criteria based on the purpose
* Thresholds — Defines threshold levels for all criteria across different years
* Metadata — Explains the justification for defining criteria and the specific threshold level chosen
* Reference data — Used for setting threshold levels relative to some external data source
* Sources — Bibliographic information on sources and references used

You can use the navigation sidebar to inspect individual editions and components.
