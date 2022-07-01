#!/bin/bash
# -------------------------------------------------------------
# Creates symlinks to ~/.FreeCAD/Mod for each macro in macros/.
# -------------------------------------------------------------

macros=`find macros -type f`

SAVEIFS=$IFS
IFS=$(echo -en "\n\b")
for macro in $macros
do
    filename=`basename $macro`
    echo "Creating symlink to $filename:"
    echo "    ln --symbolic --force "$(pwd)/$macro" ~/.local/share/FreeCAD/Macro/$filename"
    ln --symbolic --force "$(pwd)/$macro" ~/.local/share/FreeCAD/Macro/$filename
    printf "\n"
done
IFS=$SAVEIFS
