# Define path to data directory and check if it exists.
DATA_DIR <- paste0(system.file(package = "scenariovettingcriteria"), "/extdata")
if (!dir.exists(DATA_DIR)) {
    stop("Could not find data directory.")
}

# Get list of releases.
release_dirs <- list.dirs(path = DATA_DIR, full.names = TRUE, recursive = FALSE)
release_dirs <- release_dirs[grepl("/release-", release_dirs)]
if (length(release_dirs) == 0) {
    stop("Could not find releases.")
}

#' Available releases of the criteria definitions.
#'
#' A named list mapping release date strings to their directory paths within
#' the installed package.
#'
#' @export
releases <- setNames(
    as.list(release_dirs),
    sub("^release-", "", basename(release_dirs))
)
