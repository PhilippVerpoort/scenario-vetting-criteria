"""Shared pytest fixtures."""
import yaml
import pytest
from pathlib import Path

from utils import load_csv_rows, parse_bib_keys


EXTDATA = Path(__file__).parent.parent / "inst" / "extdata"
EDITIONS = sorted(EXTDATA.glob("edition-*"))


@pytest.fixture(params=EDITIONS, ids=[e.name for e in EDITIONS])
def edition_path(request):
    return request.param


@pytest.fixture
def bib_keys(edition_path):
    """Set of all non-@comment entry keys in sources.bib."""
    return parse_bib_keys(edition_path / "sources.bib")


@pytest.fixture
def criteria_types_dict(edition_path):
    """Parsed criteria-types.yaml for this edition."""
    return yaml.safe_load((edition_path / "criteria-types.yaml").read_text())


@pytest.fixture
def criteria_dirs(edition_path):
    """Mapping of criteria type name → directory path."""
    root = edition_path / "criteria"
    return {d.name: d for d in sorted(root.iterdir()) if d.is_dir()}


@pytest.fixture
def reference_datasets(edition_path):
    """Mapping of dataset stem → CSV path for all reference data files."""
    ref_dir = edition_path / "reference-data"
    return {p.stem: p for p in sorted(ref_dir.glob("*.csv"))}


@pytest.fixture
def all_threshold_rows(edition_path, criteria_dirs):
    """All parsed threshold rows across every criteria type, with '_type' injected."""
    rows = []
    for crit_type, crit_dir in criteria_dirs.items():
        for row in load_csv_rows(crit_dir / "thresholds.csv"):
            row["_type"] = crit_type
            rows.append(row)
    return rows
