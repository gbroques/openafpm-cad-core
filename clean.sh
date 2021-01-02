#!/bin/sh
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
find . -name "*.FCStd1" -type f -delete
