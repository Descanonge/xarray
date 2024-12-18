#!/usr/bin/env sh

convert _static/favicon.ico _static/favicon.png

doc2dash --verbose --enable-js --force --name XArray \
    --index-page "index.html" \
    --icon _static/favicon.png  \
    --parser "xarray.util.no_duplicate_intersphinx_parser.NoDuplicateInterSphinxParser" \
    -u "https://docs.xarray.dev/en/stable/" \
    -d "$HOME/.local/share/Zeal/Zeal/docsets" \
    _build/html
