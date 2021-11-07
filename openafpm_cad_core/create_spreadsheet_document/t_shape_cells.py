from typing import List

from .cell import Cell, Style

__all__ = ['t_shape_cells']

#: Cells defining the T Shape spreadsheet.
t_shape_cells: List[List[Cell]] = [
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
        Cell('ResineStatorOuterRadius'), Cell('=Alternator.ResineStatorOuterRadius',
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
    # The formula for I comes from solving a system of equations for I as a function of RotorDiskRadius.
    # The function should produce the following outputs, where f(RotorDiskRadius) = I:
    # * RotorDiskRadius = 125, I = 9
    # * RotorDiskRadius = 150, I = 24
    # * RotorDiskRadius = 175, I = 32
    # See A Wind Turbine Recipe Book (2014 edition), page 28.
    # Alternator Frame to Yaw Tube Sizes mm table for recommended values of I.
    # WolframAlpha was used to solve this system of equations automatically.
    #   See: https://www.wolframalpha.com/input/?i=systems+of+equations+calculator&assumption=%7B%22F%22%2C+%22SolveSystemOf3EquationsCalculator%22%2C+%22equation1%22%7D+-%3E%22125+%3D+a*%289%5E2%29+%2B+b*9+%2B+c%22&assumption=%22FSelect%22+-%3E+%7B%7B%22SolveSystemOf3EquationsCalculator%22%7D%7D&assumption=%7B%22F%22%2C+%22SolveSystemOf3EquationsCalculator%22%2C+%22equation2%22%7D+-%3E%22150+%3D+a*%2824%5E2%29+%2B+b*24+%2B+c%22&assumption=%7B%22F%22%2C+%22SolveSystemOf3EquationsCalculator%22%2C+%22equation3%22%7D+-%3E%22175+%3D+a*%2832%5E2%29+%2B+b*32+%2B+c%22
    # We contrain the system of equations to produce a horizontal parabola opening right,
    # in order to avoid negative numbers that break the model when RotorDiskRadius is large.
    # The general form of a horizontal parabola opening right, where x is RotorDiskRadius and y is I:
    #   x = a*(y^2) + b*y + c
    #
    #   125 = a*(9^2) + b*9 + c
    #   150 = a*(24^2) + b*24 + c
    #   175 = a*(32^2) + b*32 +
    #
    # Solving for a, b, and c:
    #   a = 32/552
    #   b = -(235/552)
    #   c = 2845/23
    # Then we use WolframAlpha to solve "x = (35/552)*y^2 + (-235/552)*y + 2845/23 in terms of y"
    #   See: https://www.wolframalpha.com/input/?i=x+%3D+%2835%2F552%29*y%5E2+%2B+%28-235%2F552%29*y+%2B+2845%2F23+in+terms+of+y
    # This results in two equations, and we choose the positive half of the parabola as negative values break the model:
    #   y = 1 / 70 * (sqrt(77280 * x - 9503975) + 235)
    [
        Cell('ParabolicEquationForI'), Cell('=1 / 70 * (sqrt(77280 * RotorDiskRadius - 9503975) + 235)',
                                            alias='ParabolicEquationForI'),
    ],
    # Find the vertex of the above parabola:
    #   See: https://www.wolframalpha.com/input/?i=x+%3D+%2835%2F552%29*y%5E2+%2B+%28-235%2F552%29*y+%2B+2845%2F23+find+vertex
    # (x, y) = (1900795/15456, 47/14)
    # Then solve for y = m * x + b, where b is 0 (since we want this to cross the y-axis at 0).
    # (47/14) = m * (1900795/15456) + 0
    # m = (51888/1900795)
    #   See: https://www.wolframalpha.com/input/?i=%2847%2F14%29+%3D+m+*+%281900795%2F15456%29,
    [
        Cell('LinearEquationForI'), Cell('=RotorDiskRadius * (51888/1900795)',
                                         alias='LinearEquationForI'),
    ],
    # If x is less than the vertex of the parabola,
    # then we choose a linear equation that crosses through
    # the vertex of the parabola and the origin (0, 0).
    # This ensures I is always a positive value, for any positive value of RotorDiskRadius.
    [
        Cell('I'), Cell('=RotorDiskRadius < (1900795/15456) ? LinearEquationForI : ParabolicEquationForI',
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
        Cell('X'), Cell('=Offset - (I + YawPipeRadius + MetalThicknessL)',
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
        Cell('BC'), Cell('=TShapeVerticalDistance - MetalLengthL - MetalThicknessL',
                         alias='BC')
    ],
    [
        Cell('D'), Cell('=MetalLengthL * 2',
                        alias='D')
    ]
]
