"""Tests for edition directory structure."""
import re


EDITION_NAME_RE = re.compile(r"^edition-\d{4}-\d{2}-\d{2}$")
REQUIRED_FILES = {"criteria-types.yaml", "sources.bib"}
REQUIRED_DIRS = {"criteria", "reference-data"}


def test_edition_name_format(edition_path):
    assert EDITION_NAME_RE.match(edition_path.name), (
        f"'{edition_path.name}' does not match the expected 'edition-YYYY-MM-DD' pattern."
    )


def test_required_files_present(edition_path):
    present = {p.name for p in edition_path.iterdir()}
    missing = REQUIRED_FILES - present
    assert not missing, (
        f"{edition_path.name}: missing required files: {sorted(missing)}"
    )


def test_required_directories_present(edition_path):
    present = {p.name for p in edition_path.iterdir() if p.is_dir()}
    missing = REQUIRED_DIRS - present
    assert not missing, (
        f"{edition_path.name}: missing required directories: {sorted(missing)}"
    )


def test_criteria_dirs_match_types(edition_path, criteria_types_dict, criteria_dirs):
    defined = set(criteria_types_dict)
    present = set(criteria_dirs)
    errors = []
    if extra := present - defined:
        errors.append(f"directories not listed in criteria-types.yaml: {sorted(extra)}")
    if missing := defined - present:
        errors.append(f"types in criteria-types.yaml with no directory: {sorted(missing)}")
    assert not errors, f"{edition_path.name}: " + "; ".join(errors)


def test_each_criteria_type_has_required_files(edition_path, criteria_dirs):
    errors = []
    for name, path in criteria_dirs.items():
        for fname in ("descriptions.yaml", "thresholds.csv"):
            if not (path / fname).exists():
                errors.append(f"{name}/{fname}")
    assert not errors, (
        f"{edition_path.name}: missing files:\n" + "\n".join(f"  {e}" for e in errors)
    )
