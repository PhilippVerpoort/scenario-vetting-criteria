# Scenario Validation Criteria

Common definitions of validation criteria for scenarios produced by
Integrated Assessment Models (IAMs).

Extensive documentation is available at
**[philippverpoort.github.io/scenario-vetting-criteria](https://philippverpoort.github.io/scenario-vetting-criteria/)**.

---

## Background

IAMs are computational models that produce scenarios of economy, energy
system, land use, and greenhouse-gas emissions developments over time, across
regions, and under different policy assumptions. Large ensembles of such
scenarios by multiple model families underpin major scientific assessments
such as the IPCC reports.

Scenarios are often validated in the process of producing new scenarios or
when in the process of collecting and assess existing scenario ensembles.
Specifically, scenarios are often checked against empirical observations,
near-term projections, and sustainability targets to identify scenarios that
are outdated, internally inconsistent, technically infeasible, or ecologically
undesirable. This package provides a versioned, machine-readable set of such
validation criteria so that different research groups can apply the same standards.

---

## Releases and versions

* **Releases:** The criteria definitions are continuously updated and published
in regular releases. These releases are named using a `YYYY-MM-DD` pattern that
indicates the date of the release. Releases remain accessible throughout new package
versions.
* **Versions:** As more releases are added, new version of the package are published.
The versions are named using a `vX.X.X` pattern, corresponding to major, minor, and
patch version numbers. Major version changes indicate breaking backwards-compatibility,
minor version changes indicate additional "features" (usually new releases), and
patch version changes indicate minor fixes. New versions retain copies of older releases
for backwards-compatibility.

---

## Repository structure

The core data lives in `inst/extdata/`. Each versioned release has its own
subdirectory:

```
inst/extdata/release-YYYY-MM-DD/
├── criteria-types.yaml          # Definitions of criterion types
├── operations.yaml              # Actions triggered by each criterion type
├── sources.bib                  # Bibliographic references
├── criteria/
│   ├── Historical Vetting/
│   │   ├── thresholds.csv       # Threshold values (variable, region, year, bounds)
│   │   └── metadata.yaml        # Justifications for criteria and thresholds
│   ├── Feasibility Concern/
│   │   ├── thresholds.csv
│   │   └── metadata.yaml
│   └── Sustainability Concern/
│       ├── thresholds.csv
│       └── metadata.yaml
└── reference-data/
    └── *.csv                    # External datasets used as threshold baselines
```

---

## Installation

### Python

The package is managed with [Poetry](https://python-poetry.org/). Install from
the repository:

```bash
git clone https://github.com/PhilippVerpoort/scenario-vetting-criteria.git
cd scenario-vetting-criteria
poetry install
```

Publication to PyPI is planned for later.

Requires Python ≥ 3.11. Optional dependencies: `pandas` (default CSV engine),
`pyyaml` (for metadata/types), `pybtex` (for sources).

### R

Install from the repository using `remotes`:

```r
remotes::install_github("PhilippVerpoort/scenario-vetting-criteria")
```

### Raw data

Download or clone the repository and use the files in `inst/extdata/` directly:

```bash
git clone https://github.com/PhilippVerpoort/scenario-vetting-criteria.git
```

---

## Citation

If you use this package in your research, please cite it using the metadata in
[`CITATION.cff`](CITATION.cff).

---

## License

[MIT](LICENSE.md)
