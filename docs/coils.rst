Coils
=====

* The number of magnets is a multiple of 4 between 8 and 32 inclusive.
* The number of coils is 3/4 the number of magnets.
* Thus, the number of coils is a multiple of 3 between 3 and 24 inclusive.
* RotorDiskRadius, MagnetWidth, and CoilLegWidth affect how many coils can fit in a stator.
* Stator mounting holes are aligned between coils by rotating coils by Angle / 2 (e.g. 20° for 9 coil T Shape).
* Angle = 360° / NumberCoil

=====  ===============  ============  ==========  ====== =============
Shape  RotorDiskRadius  NumberMagnet  NumberCoil  Angle  LidNotchAngle
=====  ===============  ============  ==========  ====== =============
T      115              8             6           60°    210°
T      150              12            9           40°    190°
T      185              16            12          30°    210°
T      102.96           20            15          24°    198°
T      120              24            18          20°    
T      140              28            21          17.14°    
T      140              32            24          15°    
H      225              16            12          30°
H      270              20            15          24°
Star   280              24            18          20°
Star   315              28            21          17.14°
Star   350              32            24          15°
=====  ===============  ============  ==========  ======


150° to stator mounting hole in quadrant II.

Bolts occur every:
  T Shape - every 30° (e.g. 30, 60, 90, 120, 150, 180, 210)
  H Shape - every 22.5° (e.g. 22.5, 45, 67.5, 90)
  Star Shape - every 15° (e.g. 15, 30, 45, 60, 75, 90)

T Shape 8 NumberMagnet
  150° + Angle = 210°

T Shape 12 NumberMagnet
  180° + (Angle / 2 / 2) = 190°
  150° + Angle = 190°

T Shape 16 NumberMagnet
  180° + Angle = 210°
  150° + 2 * Angle = 210°
  because 180° isn't in quadrant II

T Shape 20 NumberMagnet
  150° + 2 * Angle = 198°
  also 174° is 6° away from 180° and a bolt, where 198° is 12° away.


"2N MWT Hoverboard 20 pole SIM 9033_18_05_24":
"RotorDiskRadius": 102.96,
"MagnetLength": 25,
"MagnetWidth": 10,
"MagnetThickness": 8,
"MagnetMaterial": "Neodymium",
"NumberMagnet": 20,
"CoilType": 1,
"CoilLegWidth": 11.29,
"CoilInnerWidth1": 10,
"CoilInnerWidth2": 10,

The following has stator mounting holes which doesn't align between coils:

* H Shape, 270 RotorDiskRadius / 20 NumberMagnet
* Star Shape, 280 RotorDiskRadius / 24 NumberMagnet
* Star Shape, 315 RotorDiskRadius / 28 NumberMagnet
