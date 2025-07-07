# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     notebook_metadata_filter: source_hidden
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
#   source_hidden: true
# ---

# %% [markdown]
# ## Installation

# %% [markdown]
# While the Python package has not been released yet, you have to install it from GitHub source using:
#
# ```bash
# # when using poetry
# poetry add git+https://github.com:PhilippVerpoort/scenario-vetting-criteria.git
#
# # when using pip
# pip install git+https://github.com:PhilippVerpoort/scenario-vetting-criteria.git
# ```

# %% [markdown]
# ## Raw file paths

# %% [markdown]
# The package contains definition files for the criteria. The paths to those files are contained in `file_paths`.

# %%
from scenario_vetting_criteria import file_paths

for component_id, component_path in file_paths.items():
    print(f"{component_id}:  ...{str(component_path)[-40:]}")

# %% [markdown]
# ## Load functions

# %% [markdown]
# Instead of loading the data from these files manually, it is recommended to use the built-in load functions from the package via `load_criteria`. For instance, the following will load the definition of the thresholds values.

# %%
from scenario_vetting_criteria import load_criteria

load_criteria('criteria-thresholds')

# %% [markdown]
# Multiple files can be loaded in one go.

# %%
criteria = load_criteria(['criteria-thresholds', 'operations'])
display(criteria['operations'])

# %% [markdown]
# ## Formatting citations and sources

# %% [markdown]
# Loading the reference sources from the BibTeX file will return a pybtex object.

# %%
reference_srcs = load_criteria('reference-sources')

# %% [markdown]
# The entries in this object can be formatted according to some predefined style.

# %%
from scenario_vetting_criteria.formatting import format_sources
reference_srcs_formatted = format_sources(reference_srcs)
display(reference_srcs_formatted['Creutzig14'])

# %% [markdown]
# The `insert_citations` function can be used to insert citations into text with citation patterns.

# %%
from scenario_vetting_criteria.formatting import insert_citations

text = load_criteria('criteria-metadata')['sustainable_bioenergy']['justification_threshold']
text_inserted = insert_citations(text, reference_srcs_formatted)

print(text[:30], '...   →  ', text_inserted[:30], '...')

# %% [markdown]
# ## Apply vetting criteria to scenarios

# %% [markdown]
# A tutorial on how to apply the vetting criteria to a list of scenarios based on the [IAMC Nomenclature](https://nomenclature-iamc.readthedocs.io/en/stable/user_guide.html) package will be made available later.
