#Defines the Rotation types and assigns it some values for ease of use
class RotationType:
    RT_WLH = 0
    RT_HWL = 1
    RT_HLW = 2
    RT_LHW = 3
    RT_LWH = 4
    RT_WHL = 5

    ALL = [RT_WHL, RT_HWL, RT_HLW, RT_LHW, RT_LWH, RT_WLH]

#Defines the axis and assigns values to them
class Axis:
    WIDTH = 0
    LENGTH = 2
    HEIGHT = 1

    ALL = [WIDTH, LENGTH, HEIGHT]
