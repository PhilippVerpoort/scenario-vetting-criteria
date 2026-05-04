"""Generate criteria definition documentation pages for each release."""
from pathlib import Path

import mkdocs_gen_files

from scenario_vetting_criteria import releases


partials_dir = Path(__file__).parent.parent / "docs" / "partials"
if not partials_dir.is_dir():
    raise Exception("Partials directory not found!")


# partials = sorted(
#     [partial_path.stem for partial_path in partials_dir.glob("*.md")]
# )
partials = [
    "types",
    "metadata",
    "thresholds",
    "reference_data",
    "sources",
]


page_template = """---
release: {release}
---
{outdated_notice}

{{% include 'partials/{partial}.md' %}}
"""


outdated_template = """
!!! warning

    This page documents an **outdated release** of the criteria definitions. 
    Click [here](../../release-{latest_release}/{partial}) to get to the 
    latest release.
"""


nav_entries = []
for i, release in enumerate(reversed(releases)):
    nav_entries += f"    - Release {release}\n"
    for partial in partials:
        outdated_notice = (
            outdated_template.format(
                latest_release=list(releases)[-1],
                partial=partial,
            )
            if i
            else ""
        )
        page_path = f"release-{release}/{partial}"
        nav_entries += (
            f"        - "
            f"[{partial.capitalize().replace('_', ' ')}]"
            f"({page_path}.md)\n"
        )
        with mkdocs_gen_files.open(f"{page_path}.md", "w") as file_handle:
            file_contents = page_template.format(
                release=release,
                partial=partial,
                outdated_notice=outdated_notice,
            )
            file_handle.write(file_contents)


with open(partials_dir.parent / "nav.md") as file_handle:
    lines = file_handle.readlines()

with mkdocs_gen_files.open("nav.md", "w") as file_handle:
    print("".join(lines[0:2] + nav_entries + lines[2:]))
    file_handle.writelines(lines[0:2] + nav_entries + lines[2:])
