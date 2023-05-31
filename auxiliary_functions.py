from decimal import Decimal
from constants import Axis

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

def set_to_decimal(value,number_of_decimals):
    number_of_decimals = Decimal('1.{}'.format('0' * number_of_decimals))

    return Decimal(value).quantize(number_of_decimals)

def rect_intersect(item_1,item_2,x,y):
    a = item_1.get_dimensions()
    b = item_2.get_dimensions()
    l1 = Point(item_1.position[x] + a[x],item_1.position[y])  
    r1 = Point(item_1.position[x],item_1.position[y] + a[y])
    l2 = Point(item_2.position[x] + b[x],item_2.position[y])
    r2 = Point(item_2.position[x],item_2.position[y] + b[y])

    #if rectangle has area 0, no overlap
    if l1.x == r1.x or l1.y == r1.y or r2.x == l2.x or l2.y == r2.y:
        return False
    
    if l1.x >= r2.x or l2.x >= r1.x:
        return False
    
    if r1.y >= l2.y or r2.y>= l1.y:
        return False
    
    return True


def intersect(item_1,item_2):
    intersects = (rect_intersect(item_1,item_2,Axis.WIDTH,Axis.LENGTH) and 
                  rect_intersect(item_1,item_2,Axis.LENGTH,Axis.HEIGHT) and 
                  rect_intersect(item_1,item_2,Axis.WIDTH,Axis.HEIGHT))
    return intersects