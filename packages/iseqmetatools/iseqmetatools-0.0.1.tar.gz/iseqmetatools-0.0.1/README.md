# Iseq meta

A bunch of scripts to operate on iseq meta

More info here: https://workflows-dev-documentation.readthedocs.io/en/latest/index.html

# Install

pip install iseqmetatools


# Parsing google spreadsheet to meta

You can parse inputs, outputs or workflows parameters for the workflow.
Example use for workflows parameters (after installing):

parse_workflows \
  --input-workflow-name "germline" \
  --input-credentials-json "/path/to/credentials.json" \
  --input-meta-json "/path/to/wdl/meta.json" \
  --input-google-spreadsheet-key "key" \
  --output-meta-json "/path/to/output/meta.json"

More info here:
https://workflows-dev-documentation.readthedocs.io/en/latest/Developer%20tools.html#parsing-google-spreadsheet-to-meta