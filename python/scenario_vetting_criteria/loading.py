import importlib

from .file_paths import file_paths


# for importing modules on demand and safely if modules are not installed
def _import_module(pkg: str):
    try:
        globals()[pkg] = importlib.import_module(pkg)
        return True
    except ImportError:
        return False


# load criteria definitions from a specific criteria file
csv_engines: list[str] = ['python', 'pandas']
def _load_criteria_file(component: str, csv_engine: str):
    # check if component is known
    if component not in file_paths:
        raise Exception(f"Unknown component: {component}. Please choose one from: {','.join(list(file_paths))}")

    # obtain file path and file type
    file_path = file_paths[component]
    file_type = file_path.suffixes[-1]

    # check CVS engine argument
    if csv_engine not in csv_engines:
        raise Exception(f"Unknown CSV engine: {csv_engine}. Please choose one from: {','.join(csv_engines)}")
    if csv_engine == 'python':
        csv_engine = 'csv'

    # open file as file stream and load
    with file_path.open('r') as file_stream:
        if file_type == '.csv':
            if not _import_module(csv_engine):
                raise Exception(f"Loading the criteria definition file '{file_path.stem}' requires the '{csv_engine}' package!")
            if csv_engine == 'csv':
                file_contents = list(csv.reader(file_stream, delimiter=',', quotechar='"'))
            elif csv_engine == 'pandas':
                if component == 'criteria-thresholds':
                    file_contents = pandas.read_csv(
                        file_stream,
                        delimiter=',',
                        quotechar='"',
                        header=[0, 1],
                        index_col=list(range(6)),
                    )
                else:
                    file_contents = pandas.read_csv(
                        file_stream,
                        delimiter=',',
                        quotechar='"',
                    )
        elif file_type == '.yaml':
            if not _import_module('yaml'):
                raise Exception(f"Loading the criteria definition file '{file_path.stem}' requires the pyyaml package!")
            file_contents = yaml.safe_load(file_stream)
        elif file_type == '.bib':
            if not _import_module('pybtex'):
                raise Exception(f"Loading the criteria definition file '{file_path.stem}' requires the pybtex package!")
            from pybtex.database.input import bibtex
            file_contents = bibtex.Parser().parse_file(file_stream)
        else:
            raise Exception(f"Unknown file format: {file_path.name}")
        return file_contents


# load all criteria definitions
def load_criteria(components: str | list[str] | tuple[str], csv_engine: str = 'pandas'):
    """
    Loads and returns the criteria definitions contained in the package.

    Parameters
    ----------
    components : str | list[str] | tuple[str]
        A string or list/vector of strings. The return type changes depending 
        on whether a list/vector or a single string is provided.
    csv_engine : str = 'pandas'
        The method for loading CSV files if these are supposed to be loaded. Must 
        be one of `read.csv`, `readr`, and `data.table`. Defaults to `read.csv`.

    Returns
    -------
        pd.DataFrame | dict[str, str] | dict[str, pd.DataFrame | dict[str, str]]
            Returns the loaded data. This data can be a dataframe or a nested list. 
            If multiple data components are requested, then the components are 
            returned inside a keyworded list.
    """
    if isinstance(components, str):
        return _load_criteria_file(components, csv_engine=csv_engine)
    else:
        return {
            component: _load_criteria_file(component, csv_engine=csv_engine)
            for component in components
        }
