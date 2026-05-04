{% include-markdown "../README.md" %}

You can use the navigation sidebar to inspect individual releases and components.

## Releases
The validation criteria are continuously updated and made available as separate releases. These releases are currently available:

```python exec="true" session="index" showcode="false"
from scenario_vetting_criteria import releases
for i, release in enumerate(reversed(releases)):
    print(f"* Release {release}" + ("(latest)" if not i else ""))
```

## Components
Each releases contains the following components:

* Types — Distinguishes criteria based on the purpose
* Thresholds — Defines threshold levels for all criteria across different years
* Metadata — Explains the justification for defining criteria and the specific threshold level chosen
* Reference data — Used for setting threshold levels relative to some external data source
* Sources — Bibliographic information on sources and references used
