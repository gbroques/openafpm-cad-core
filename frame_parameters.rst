Frame
=====
TODO: Does H Shape reference all these?
MagnAFPM
--------
* ``RotorDiskRadius``
* ``CoilLegWidth``

Furling
-------
* ``Offset``

User
----
* ``MetalLengthL``
* ``MetalThicknessL``
* ``Holes``
* ``YawPipeRadius``

Variants
--------

T Shape
^^^^^^^

Calculated
""""""""""
============================ ================================================================
Name                         Calculation
============================ ================================================================
``StatorHolesCircumradius``  ``RotorDiskRadius + CoilLegWidth + 20``
``BC``                       ``StatorHolesCircumradius - 25 + X``
``X``                        ``Offset - (I + MetalThicknessL + YawPipeRadius)``
``I``                        ``-0.0056 * RotorDiskRadius ^ 2 + 2.14 * RotorDiskRadius - 171``
============================ ================================================================

H Shape
^^^^^^^

Calculated
""""""""""
============================ ================================================================
Name                         Calculation
============================ ================================================================
``StatorHolesCircumradius``  ``RotorRadius + CoilLegWidth + 20``
``Delta``                    ``100 - 8 *
                             (25 - StatorHolesCircumradius * StatorHolesCircumradius)``
``alpha``                    ``(10 + Delta ^ 0.5) / 4``
``G``                        ``2 * alpha + 40``
``H``                        ``G - 2 * MetalLengthL``
``LengthH``                  ``G - 100`` (MasterH) ??????????
============================ ================================================================
