Rotor Disk
==========
For T Shape, H Shape, and Star Shape.

MagnAFPM
--------
* ``RotorDiskRadius``
* ``DiskThickness``

User
----
* ``RotorInnerCircle``
* ``HubHolesPlacement``
* ``HubHoles``

Calculated
""""""""""

===================== ==========================================================
Name                  Calculation
===================== ==========================================================
``NumberOfHoles``     ``RotorDiskRadius <= 187.5 ? 4 : 6``
===================== ==========================================================

Star Shape
^^^^^^^^^^
In addition to the above parameters and calculations.

MagnAFPM
--------
* ``MagnetLength``

Calculated
""""""""""
============================ ==========================================================
Name                         Calculation
============================ ==========================================================
``PocketInnerWidth``         ``2 * 3.14159 * PocketInnerCircumradius / 12``
``PockentOuterWidth``        ``2 * 3.14159 * PocketOuterCicrumradius / 12``
``PocketInnerCircumradius``  ``HubHolesPlacement + 3 * HubHoles``
``RotorResinCastHoleRadius`` ``RotorDiskRadius - MagnetLength - 25``
``PocketOuterCicrumradius``  ``RotorResinCastHoleRadius - 12``
``SmallHoleRadius``          ``HubHoles - 4``
``SmallHolesCircumradius``   ``(PocketOuterCicrumradius - PocketInnerCircumradius)
                             / 2 + PocketInnerCircumradius``
============================ ==========================================================
