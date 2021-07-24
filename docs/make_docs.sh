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

rm -rf $build_directory
rm -rf openafpm_cad_core

python \
    -m sphinx \
    $source_directory \
    $build_directory
