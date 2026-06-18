{{ readme_section('## Background', '## Repository structure') }}

Currently, the following editions are available:

```python exec="true" session="index" showcode="false"
from scenario_vetting_criteria import editions
for i, edition in enumerate(reversed(editions)):
    suffix = " (latest)" if not i else ""
    print(f"* [Edition {edition}](edition-{edition}/summary/){suffix}")
```

