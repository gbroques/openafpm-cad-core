#!/bin/bash
# -----------------------------------------------------------------------
# Creates a symlink to FreeCAD Macro directory for each macro in macros/.
# -----------------------------------------------------------------------

macros=`find macros -type f`

SAVEIFS=$IFS
IFS=$(echo -en "\n\b")
for macro in $macros
do
    filename=`basename $macro`
    echo "Creating symlink to $filename:"
    macro_dir="~/.local/share/FreeCAD/Macro"
    echo "    ln --symbolic --force $(pwd)/$macro $macro_dir/$filename"
    ln --symbolic --force "$(pwd)/$macro $macro_dir/$filename"
    printf "\n"
done
IFS=$SAVEIFS
