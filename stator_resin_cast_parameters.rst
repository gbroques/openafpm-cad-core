Stator Resin Cast
=================

MagnAFPM
--------
* ``StatorThickness``
* ``RotorDiskRadius``
* ``MagnetLength``
* ``CoilLegWidth``

User
----
* ``Holes``

Variants
--------

T Shape
^^^^^^^

Calculated
""""""""""
===================== ==========================================================
Name                  Calculation
===================== ==========================================================
``InnerHoleRadius``   ``RotorDiskRadius`` - ``MagnetLength`` - ``CoilLegWidth``
``HolesCircumradius`` ``RotorDiskRadius`` + ``CoilLegWidth`` + ``20``
===================== ==========================================================

Static
""""""
===================== ===================
Name                  Value
===================== ===================
``HolePaddingRadius`` ``25``
``HoleRotationAngle`` ``360° / 3 = 120°``
===================== ===================

H Shape
^^^^^^^

Calculated
""""""""""
===================== =========================================================
Name                  Calculation
===================== =========================================================
``InnerHoleRadius``   ``RotorDiskRadius`` - ``MagnetLength`` - ``CoilLegWidth``
``HolesCircumradius`` ``RotorDiskRadius`` + ``CoilLegWidth`` + ``20``
===================== =========================================================

Static
""""""
===================== ===================
Name                  Value
===================== ===================
``HolePaddingRadius`` ``35``
``HoleRotationAngle`` ``360° / 4 = 90°``
===================== ===================

Star Shape
^^^^^^^^^^

Calculated
""""""""""
===================== ================================================================
Name                  Calculation
===================== ================================================================
``InnerHoleRadius``   ``RotorDiskRadius`` - ``MagnetLength`` - ``CoilLegWidth``
``HolesCircumradius`` ``RotorRadius`` + ``CoilLegWidth`` + ``0.5`` *
                      (``OuterCircleRadius`` -
                      ``RotorRadius`` -
                      ``CoilLegWidth``)
``OuterCircumradius`` (``RotorDiskRadius`` + ``CoilLegWidth`` + ``20``) / ``cos(30°)``
===================== ================================================================
