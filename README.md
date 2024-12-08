# OpenAFPM CAD Core

Repository containing [OpenAFPM](https://www.openafpm.net/) wind turbine model made with open-source CAD program [FreeCAD](https://www.freecad.org/).

## Installing Package

From the root of this repository:

    pip install --editable .


## Installing Macros

From the root of this repository:

    ./link_macros.bash


## Related Repositories
* [openafpm-cad-visualization](https://github.com/gbroques/openafpm-cad-visualization)
* [openafpm-cad-desktop-app](https://github.com/gbroques/openafpm-cad-desktop-app)


## Prerequisites

1. Install [Micromamba](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html).


## Setup
Execute the following commands from the root of this repository.

1. Create `openafpm-cad-core` conda environment.

       micromamba env create --file environment.yml

2. Activate `openafpm-cad-core` environment.

       micromamba activate openafpm-cad-core

3. Add the `$CONDA_PREFIX/lib` directory to `$PYTHONPATH` (this allows `FreeCAD` to be imported as a module within python).

       ./add_conda_path_to_python_path.sh

4. Deactivate and re-activate `openafpm-cad-core` environment.

       micromamba deactivate && micromamba activate openafpm-cad-core


5. Verify `freecad` executable is accessible:

       freecad --version

## Docs
Run `./make_docs.sh` from `docs/` with `openafpm-cad-core` conda environment activated.


## How to Upgrade FreeCAD Version
The version of FreeCAD is defined in `environment.yml` within the root of this repository.

1. Check if there's a newer version from FreeCAD's [GitHub releases page](https://github.com/FreeCAD/FreeCAD/releases) or [Wiki](https://wiki.freecad.org/Feature_list#Release_notes).
2. Increase version for `freecad` in `environment.yml`.
3. Remove `openafpm-cad-core` conda environment created in the "Setup" section.

       micromamba remove --name openafpm-cad-core --all

4. Reperform steps in the [Setup](#setup) section to recreate `openafpm-cad-core` conda environment.
5. Regression test all functionality. (TODO: Write documentation for this)
6. Update "Supported FreeCAD Versions" section in [README.md](./README.md).

## Generating OBJ Files for openafpm-cad-visualization

1. Activate the `openafpm-cad-core` conda environment.
2. If `openafpm-cad-visualization` is cloned up a directory from this repository, then run:

       python macros/visualize.py ../openafpm-cad-visualization/public/

## Troubleshooting

Run `/macros` from FreeCAD's GUI to see FreeCAD related warnings and errors.

Currently, macros must be manually edited to remove multi-threading to avoid a pickle-related serialization error.

## Supported FreeCAD Versions

Currently tested with FreeCAD `1.0.0`.


## Links
* [[YouTube] Wind Empowerment Webinar - OpenAFPM tools for designing AFPM generators for Small Wind Turbines](https://www.youtube.com/watch?v=hk0j-qxkG9s&ab_channel=WindEmpowerment)
* [Wind Empowerment](https://windempowerment.com/)
* [WISIONS of Sustainability](https://wisions.net/)
* [Hugh Piggott's blog](http://scoraigwind.co.uk/)
  * [A Wind Turbine Recipe Book (metric edition) by Hugh Piggott](http://scoraigwind.co.uk/pdf-metric-edition-of-recipe-book-at-scribd/)
* [[Wikipedia] Wind turbine design](https://en.wikipedia.org/wiki/Wind_turbine_design)
