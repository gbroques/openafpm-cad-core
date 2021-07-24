#!/bin/sh
# --------------------------------------------------------------
# Make or build the documentation for OpenAFPM CAD Core.
# 
# Requires openafpm-cad-core conda environment to be activated.
# 
# For help on using Sphinx, run:
#   python -m sphinx --help
# --------------------------------------------------------------
source_directory="."
build_directory="_build"
python \
    -m sphinx \
    $source_directory \
    $build_directory
