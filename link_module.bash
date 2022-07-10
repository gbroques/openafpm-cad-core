#!/bin/bash
# -----------------------------------------------
# Creates a symlink to Mod directory for project.
# -----------------------------------------------
echo "Creating symlink to $(pwd)"
ln --symbolic --force $(pwd) ~/.local/share/FreeCAD/Mod/
