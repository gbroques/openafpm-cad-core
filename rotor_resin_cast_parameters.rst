Rotor Resin Cast
================

MagnAFPM
--------
* ``RotorDiskRadius``
* ``DiskThickness``
* ``MagnetLength``
* ``MagnetThickness``

User
----
* ``ResineRotorMargin``

Calculated
""""""""""
===================== ==========================================================
Name                  Calculation
===================== ==========================================================
``OuterRadius``       ``RotorDiskRadius`` + ``ResineRotorMargin``
``Thickness``         ``DiskThickness`` + ``MagnetThickness``
===================== ==========================================================

Variants
--------

T Shape
^^^^^^^

User
----
* ``HubHolesPlacement``

Calculated
""""""""""
===================== ==========================================================
Name                  Calculation
===================== ==========================================================
``InnerRadius``       ``HubHolesPlacement + 0.5 * (RotorRadius - MagnetLength - HubHolesPlacement)``
===================== ==========================================================

H Shape & Star Shape
^^^^^^^^^^^^^^^^^^^^

Calculated
""""""""""
===================== ==========================================================
Name                  Calculation
===================== ==========================================================
``InnerRadius``       ``RotorDiskRadius`` - ``MagnetLength`` - 25
===================== ==========================================================
