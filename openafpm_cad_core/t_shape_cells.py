from .cell import Cell, Style

t_shape_cells = [
    # Inputs
    # ------
    [
        Cell('Inputs', styles=[Style.UNDERLINE])
    ],
    [
        Cell('RotorDiskRadius'), Cell('=Spreadsheet.RotorDiskRadius',
                                      alias='RotorDiskRadius')
    ],
    [
        Cell('Offset'), Cell('=Spreadsheet.Offset',
                             alias='Offset')
    ],
    [
        Cell('YawPipeRadius'), Cell('=Spreadsheet.YawPipeRadius',
                                    alias='YawPipeRadius')
    ],
    [
        Cell('MetalThicknessL'), Cell('=Spreadsheet.MetalThicknessL',
                                      alias='MetalThicknessL')
    ],
    [
        Cell('MetalLengthL'), Cell('=Spreadsheet.MetalLengthL',
                                   alias='MetalLengthL')
    ],
    [
        Cell('ResineStatorOuterRadius'), Cell('=Spreadsheet.ResineStatorOuterRadius',
                                              alias='ResineStatorOuterRadius')
    ],
    [
        Cell('Holes'), Cell('=Spreadsheet.Holes',
                            alias='Holes')
    ],

    # Yaw Bearing to Frame Junction
    # -----------------------------
    [
        Cell('Yaw Bearing to Frame Junction', styles=[Style.UNDERLINE])
    ],
    [
        Cell('I'), Cell('=1 / 70 * (sqrt(77280 * RotorDiskRadius - 9503975) + 235)',
                        alias='I')
    ],
    [
        Cell('j'), Cell('=0.32 * RotorDiskRadius - 3',
                        alias='j')
    ],
    [
        Cell('k'), Cell('=0.2 * RotorDiskRadius - 5',
                        alias='k')
    ],

    # Frame
    # -----
    [
        Cell('Frame', styles=[Style.UNDERLINE])
    ],
    [
        Cell('X'), Cell('=Offset - (I + YawPipeRadius)',
                        alias='X')
    ],
    # 30 degrees because 360 / 3 = 120 - 90 = 30.
    # Divide by 3 for because the T Shape has 3 holes.
    # cos(30) * ResineStatorOuterRadius = bottom of right triangle
    # * 2 to get both sides.
    # 40 = 2 * margin. margin is the distance from the hole to the edge of the metal.
    # Add the radius for holes on each side, + Spreadsheet.Holes * 2.
    [
        Cell('a'), Cell(
            '=cos(30) * ResineStatorOuterRadius * 2 + 40 + Holes * 2',
            alias='a')
    ],
    # Total vertical distance of T Shape from bottom hole to two top holes.
    # This is the opposite, or vertical left side of the right triangle plus,
    # the stator resin cast radius.
    [
        Cell('TShapeVerticalDistance'), Cell('=(sin(30) * ResineStatorOuterRadius) + ResineStatorOuterRadius',
                                             alias='TShapeVerticalDistance')
    ],
    # Subtract MetalLengthL as the top holes and bottom hole are centered in the brackets.
    # MetalLengthL is the length of the brackets.
    [
        Cell('BC'), Cell('=TShapeVerticalDistance - MetalLengthL',
                         alias='BC')
    ],
    [
        Cell('D'), Cell('=MetalLengthL * 2',
                        alias='D')
    ]
]
