# load criteria definitions from a specific criteria file
csv_engines <- c('read.csv', 'readr', 'data.table')
load_criteria_file <- function(component, csv_engine = 'read.csv') {
  # check if component is known
  if (!(component %in% names(file_paths))) {
    stop(paste0("Unknown component: ", component, ". Please choose one from: ", toString(names(file_paths))))
  }

  # obtain file path and file type
  file_path <- file_paths[[component]]
  file_type <- tools::file_ext(file_path)

  # check CSV engine argument
  if (!(csv_engine %in% csv_engines)) {
    stop(paste("Unknown CSV engine:", csv_engine, ". Please choose one from:", toString(csv_engines)))
  }

  # open file as file stream and load
  suppressMessages({
    if (file_type == 'csv') {
      if (csv_engine != 'read.csv' && !require(csv_engine, character.only = TRUE, quietly = TRUE)) {
        stop(paste("Could not load library:", csv_engine))
      }
      if (component == 'criteria-thresholds') {
        if (csv_engine == 'read.csv') {
          df1 <- read.csv(file_path, sep=",", quote="\"", skip=2, header=TRUE)
          df2 <- read.csv(file_path, sep=",", quote="\"", skip=0, header=FALSE)
        } else if (csv_engine == 'readr') {
          df1 <- readr::read_csv(file_path, quote="\"", skip=2, col_names=TRUE)
          df2 <- readr::read_csv(file_path, quote="\"", skip=0, col_names=FALSE)
        } else if (csv_engine == 'data.table') {
          df1 <- data.table::fread(file_path, quote="\"", skip=2, header=TRUE)
          df2 <- data.table::fread(file_path, quote="\"", skip=0, header=FALSE)
        } else {
          stop(paste("Unknown CSV engine:", csv_engine, ". Please choose one from:", csv_engines))
        }
        df1 <- df1[, 1:6]
        df2 <- df2[, -c(1:6)]
        new_names <- paste(df2[1, ], df2[2, ], sep = ".")
        df2 <- df2[-(1:3), ]
        colnames(df2) <- new_names
        rownames(df2) <- NULL
        file_contents <- cbind(df1, df2)
      } else {
        if (csv_engine == 'read.csv') {
          file_contents <- read.csv(file_path, sep=",", quote="\"", skip=0, header=TRUE)
        } else if (csv_engine == 'readr') {
          file_contents <- readr::read_csv(file_path, quote="\"", skip=0, col_names=TRUE)
        } else if (csv_engine == 'data.table') {
          file_contents <- data.table::fread(file_path, sep=",", quote="\"", skip=0, header=TRUE)
        } else {
          stop(paste("Unknown CSV engine:", csv_engine, ". Please choose one from:", csv_engines))
        }
      }
    } else if (file_type == 'yaml') {
      if (!require("yaml", character.only = TRUE, quietly = TRUE)) {
        stop(paste0("Loading the criteria definition file '", basename(file_path), "' requires the 'pyyaml' package!"))
      }
      file_contents <- yaml.load_file(file_path)
    } else if (file_type == 'bib') {
      if (!require("bibtex", character.only = TRUE, quietly = TRUE)) {
        stop(paste0("Loading the criteria definition file '", basename(file_path), "' requires the 'bibtex' package!"))
      }
      file_contents <- read.bib(file_path)
    } else {
      stop(paste("Unknown file format:", basename(file_path)))
    }
  })

  return(file_contents)
}


#' @title load_criteria
#'
#' @description Loads and returns the criteria definitions contained in the package.
#'
#' @param components A string or list/vector of strings. The return type changes depending on whether a list/vector or a single string is provided.
#' @param csv_engine The method for loading CSV files if these are supposed to be loaded. Must be one of `read.csv`, `readr`, and `data.table`. Defaults to `read.csv`.
#'
#' @return Returns the loaded data. This data can be a dataframe or a nested list. If multiple data components are requested, then the components are returned inside a keyworded list.
#'
#' @examples
#' df.criteria.thresholds <- load_criteria('criteria-thresholds')
#' print(df.criteria.thresholds)
#' 
#' list.criteria.metadata <- load_criteria('criteria-metadata')
#' print(list.criteria.metadata)
#' 
#' criteria.defs <- load_criteria(c('criteria-thresholds', 'criteria-metadata', 'reference-data'))
#' print(criteria.defs[['criteria-metadata']])
#' 
#' @export
load_criteria <- function(components, csv_engine = 'read.csv') {
  if (is.character(components) && length(components) == 1) {
    # load single component
    return(load_criteria_file(components, csv_engine=csv_engine))
  } else {
    # loop over parts if it is a list or vector
    ret <- list()
    for (component in components) {
      ret[[component]] <- load_criteria_file(component, csv_engine=csv_engine)
    }
    return(ret)
  }
}
