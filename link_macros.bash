#!/bin/bash
# --------------------------------------------------------------------------
# Convenience script to create symlinks to FreeCAD's default macro directory
# for each macro in macros/.
#                                               
# Supports Linux operating systems.
#
# Contributions to support MacOS & Windows are welcomed.
# --------------------------------------------------------------------------

# Exit on error.
set -e

is_linux()
{
    [ "$(uname --kernel-name)" = "Linux" ]
}

is_macOS()
{
     "$(uname --kernel-name)" = "Darwin" ]
}

if is_linux; then
    macro_dir=`realpath ~/.local/share/FreeCAD/Macro`
elif is_macOS; then
    echo "Error: MacOS not supported. Please contribute changes on GitHub." >&2
    echo "See default Macro directory for MacOS here:" >&2
    echo "https://wiki.freecad.org/How_to_install_macros#Default_directory" >&2
    exit 1
else # Windows
    echo "Error: Windows not supported. Please contribute changes on GitHub." >&2
    echo "See default Macro directory for Windows here:" >&2
    echo "https://wiki.freecad.org/How_to_install_macros#Default_directory" >&2
    exit 1
fi

macros=`find macros -type f`

SAVEIFS=$IFS
IFS=$(echo -en "\n\b")
for macro in $macros
do
    filename=`basename $macro`
    echo "ln --symbolic --force $(pwd)/$macro $macro_dir/$filename"
    ln --symbolic --force $(pwd)/$macro $macro_dir/$filename
done
IFS=$SAVEIFS
