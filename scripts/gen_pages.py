"""Generate criteria definition documentation pages for each edition."""
from pathlib import Path

import mkdocs_gen_files

from scenario_vetting_criteria import editions


partials_dir = Path(__file__).parent.parent / "docs" / "partials"
if not partials_dir.is_dir():
    raise Exception("Partials directory not found!")


summary_partial = "summary"
component_partials = [
    "types",
    "metadata",
    "thresholds",
    "reference_data",
    "sources",
]
all_partials = [summary_partial] + component_partials


page_template = """---
edition: {edition}
---
{outdated_notice}

{{% include 'partials/{partial}.md' %}}
"""


outdated_template = """
!!! warning

    This page documents an **outdated edition** of the criteria definitions.
    Click [here](../../edition-{latest_edition}/{partial}) to get to the
    latest edition.
"""


summary_nav_entries = []
component_nav_entries = []

for i, edition in enumerate(reversed(editions)):
    summary_nav_entries.append(
        f"    - [Edition {edition}](edition-{edition}/summary.md)\n"
    )

    component_nav_entries.append(f"    - Edition {edition}\n")
    for partial in component_partials:
        component_nav_entries.append(
            f"        - [{partial.capitalize().replace('_', ' ')}]"
            f"(edition-{edition}/{partial}.md)\n"
        )

    for partial in all_partials:
        outdated_notice = (
            outdated_template.format(
                latest_edition=list(editions)[-1],
                partial=partial,
            )
            if i
            else ""
        )
        page_path = f"edition-{edition}/{partial}"
        with mkdocs_gen_files.open(f"{page_path}.md", "w") as file_handle:
            file_handle.write(page_template.format(
                edition=edition,
                partial=partial,
                outdated_notice=outdated_notice,
            ))


summary_nav = (
    ["- Summary\n", "    - [Overview](index.md)\n"]
    + summary_nav_entries
)
component_nav = (
    ["- Components\n", "    - [Overview](components/index.md)\n"]
    + component_nav_entries
)

with open(partials_dir.parent / "nav.md") as file_handle:
    static_nav_lines = file_handle.readlines()

with mkdocs_gen_files.open("nav.md", "w") as file_handle:
    file_handle.writelines(summary_nav + component_nav + static_nav_lines)
