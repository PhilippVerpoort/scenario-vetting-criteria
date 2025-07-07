# define path to data directory and check if it exists
DATA_DIR <- paste0(system.file(package = "scenariovettingcriteria"), "/extdata")
if (!dir.exists(DATA_DIR)) {
  stop("Could not find data directory.")
}


# define file paths to individual criteria files
component_paths <- list.files(path = DATA_DIR, recursive = FALSE, full.names = TRUE)
file_paths_list <- lapply(component_paths, function(component_path) {
  component <- sub("\\..*", "", basename(component_path))
  list(name = component, path = component_path)
})
#' @export
file_paths <- setNames(lapply(file_paths_list, function(x) x$path), sapply(file_paths_list, function(x) x$name))
