# Define path to data directory and check if it exists.
DATA_DIR <- paste0(system.file(package = "scenariovettingcriteria"), "/extdata")
if (!dir.exists(DATA_DIR)) {
    stop("Could not find data directory.")
}

# Get list of editions.
edition_dirs <- list.dirs(path = DATA_DIR, full.names = TRUE, recursive = FALSE)
edition_dirs <- edition_dirs[grepl("/edition-", edition_dirs)]
if (length(edition_dirs) == 0) {
    stop("Could not find editions.")
}

#' Available editions of the criteria definitions.
#'
#' A named list mapping edition date strings to their directory paths within
#' the installed package.
#'
#' @export
editions <- setNames(
    as.list(edition_dirs),
    sub("^edition-", "", basename(edition_dirs))
)
