from decimal import Decimal
from constants import Axis

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

def set_to_decimal(value,number_of_decimals):
    number_of_decimals = Decimal('1.{}'.format('0' * number_of_decimals))

    return Decimal(value).quantize(number_of_decimals)

# def rect_intersect(item_1,item_2,x,y):
#     a = item_1.get_dimensions()
#     b = item_2.get_dimensions()
#     l1 = Point(item_1.position[x] + a[x],item_1.position[y])
#     r1 = Point(item_1.position[x],item_1.position[y] + a[y])
#     l2 = Point(item_2.position[x] + b[x],item_2.position[y])
#     r2 = Point(item_2.position[x],item_2.position[y] + b[y])

#     #if rectangle has area 0, no overlap
#     if l1.x >= r2.x or r1.x <= l2.x or r1.y <= l2.y or l1.y >= r2.y:
#         return False
#     else:
#         return True


# def intersect(item_1,item_2):
#     intersects = (rect_intersect(item_1,item_2,Axis.WIDTH,Axis.LENGTH) and 
#                   rect_intersect(item_1,item_2,Axis.LENGTH,Axis.HEIGHT) and 
#                   rect_intersect(item_1,item_2,Axis.WIDTH,Axis.HEIGHT))
#     return intersects

def do_cuboids_overlap(cuboid1, cuboid2):
    for i in range(3): # check for x, y and z axis
        if cuboid1[0][i] >= cuboid2[1][i] or cuboid2[0][i] >= cuboid1[1][i]:
            return False
    return True

def intersect(item_1, item_2):
    a = item_1.get_dimensions()
    b = item_2.get_dimensions()
    a1,b1,c1 = item_1.position
    x1,y1,z1 = [a1 + a[0],b1 + a[1],c1 + a[2]]
    a2,b2,c2 = item_2.position
    x2,y2,z2 = [a2 + b[0],b2 + b[1],c2 + b[2]]

    cuboid1 = [(a1,b1,c1),(x1,y1,z1)]
    cuboid2 = [(a2,b2,c2),(x2,y2,z2)]
    return do_cuboids_overlap(cuboid1,cuboid2)