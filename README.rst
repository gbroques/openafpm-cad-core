OpenAFPM CAD Core
=================

OpenAFPM (Axial Flux Permanent Magnet) generators for wind electric systems.

Installing Package
------------------
From ``~/.FreeCAD/Mod``:

.. code-block::

   ln -s path/to/openafpm-cad-core/ openafpm-cad-core


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

Docs
----
Run ``./make_docs.sh`` from ``docs/`` with ``openafpm-cad-core`` conda environment activated.

FreeCAD Version
---------------
Requires FreeCAD 19.1 or greater.
