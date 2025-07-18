library(devtools)
library(roxygen2md)
library(Rd2md)


# produce *.Rd documentation files in directory ./man/
devtools::document()
message("./man/*.Rd documentation files created from in-code docu with devtools.")


# convert Roxygen documentation to make it more markdown-friendly
roxygen2md::roxygen2md()
message("./man/*.Rd files updated with roxygen2md.")


# convert *.Rd files to markdown files
rd_input_files <- list.files("./man/", pattern = "\\.Rd$", full.names = TRUE)
md_output_file <- file("./docs/code/R.md", open = "w")

for (rdf in rd_input_files) {
  md_text <- Rd2md::as_markdown(read_rdfile(rdf))
  writeLines(md_text, md_output_file)
  writeLines("\n\n---\n\n", md_output_file)  # Optional: separator between entries
}
close(md_output_file)
message("*.Rd files exported to markdown file with Rd2md.")
