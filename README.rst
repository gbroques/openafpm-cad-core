OpenAFPM CAD Core
=================

Repository containing `OpenAFPM <https://www.openafpm.net/>`_ wind turbine CAD model.

Installing Package
------------------
From the root of this repository:

.. code-block::

   pip install --editable .


Installing Macros
-----------------
From the root of this repository:

.. code-block::

   ./link_macros.bash

Links
-----
* `OpenAFPM - Online Design Tools for Locally Manufactured Small Wind Turbines <https://www.openafpm.net/>`_
* `[YouTube] Wind Empowerment Webinar - OpenAFPM tools for designing AFPM generators for Small Wind Turbines <https://www.youtube.com/watch?v=hk0j-qxkG9s&ab_channel=WindEmpowerment>`_
* `Wind Empowerment <https://windempowerment.com/>`_
* `WISIONS of Sustainability <https://wisions.net/>`_
* `Hugh Piggott's blog <http://scoraigwind.co.uk/>`_

  * `A Wind Turbine Recipe Book (metric edition) by Hugh Piggott <http://scoraigwind.co.uk/pdf-metric-edition-of-recipe-book-at-scribd/>`_

* `[Wikipedia] Wind turbine design <https://en.wikipedia.org/wiki/Wind_turbine_design>`_

Related Repositories
--------------------
* `openafpm-cad-visualization <https://github.com/gbroques/openafpm-cad-visualization>`_
* `openafpm-cad-desktop-app <https://github.com/gbroques/openafpm-cad-desktop-app>`_

Prerequisites
-------------

1. Install `conda <https://docs.conda.io/projects/conda/en/latest/>`_.

Setup
-----
Execute the following commands from the root of this repository.

1. Create ``openafpm-cad-core`` conda environment.

   .. code-block::

      conda env create --file environment.yml

2. Activate ``openafpm-cad-core`` environment.

   .. code-block::

      conda activate openafpm-cad-core

3. Add the ``$CONDA_PREFIX/lib`` directory to ``$PYTHONPATH`` (this allows ``FreeCAD`` to be imported as a module within python).
  
   .. code-block::

      ./add_conda_path_to_python_path.sh

4. Deactivate and re-activate ``openafpm-cad-core`` environment.

   .. code-block::

     conda deactivate && conda activate openafpm-cad-core


5. Verify ``freecad`` executable is accessible:

   .. code-block::

     freecad --version

Docs
----
Run ``./make_docs.sh`` from ``docs/`` with ``openafpm-cad-core`` conda environment activated.

How to Upgrade FreeCAD Version
------------------------------
The version of FreeCAD is defined in ``environment.yml`` within the root of this repository.

1. Check if there's a newer version from FreeCAD's `GitHub releases page <https://github.com/FreeCAD/FreeCAD/releases>`_ or `Wiki <https://wiki.freecad.org/Feature_list#Release_notes>`_.
2. Increase version for ``freecad`` in ``environment.yml``.
3. Remove ``openafpm-cad-core`` conda environment created in the "Setup" section.

   .. code-block::

      conda remove --name openafpm-cad-core --all

4. Perform steps in the "Setup" section to create ``openafpm-cad-core`` conda environment.
5. Regression test all functionality. (TODO: Write documentation for this)

Supported FreeCAD Versions
--------------------------
Currently tested with FreeCAD ``21.0``.
