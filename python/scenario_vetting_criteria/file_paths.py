from pathlib import Path


# define path to data directory and check if it exists
DATA_DIR: Path = Path(__file__).parent / 'data'
if not (DATA_DIR.exists() and DATA_DIR.is_dir()):
    raise Exception('Could not find data directory.')


# define file paths to individual criteria files
file_paths = {
    component.name.split('.')[0]: DATA_DIR / component.name
    for component in DATA_DIR.glob('*')
    if component.suffix in ['.csv', '.yaml', '.bib']
}

ref_paths = {
    component.name.split('.')[0]: DATA_DIR / 'reference-data' / component.name
    for component in (DATA_DIR / 'reference-data').glob('*')
    if component.suffix == '.csv'
}
