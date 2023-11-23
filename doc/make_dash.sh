#!/usr/bin/env sh

convert _static/favicon.ico _static/favicon.png

doc2dash --verbose -j -f -n XArray \
    --index-page "index.html" \
    --icon _static/favicon.png  \
    -u "https://docs.xarray.dev/en/stable/" \
    -d "$HOME/.local/share/Zeal/Zeal/docsets" \
    _build/html
