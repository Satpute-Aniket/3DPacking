from auxiliary_functions import set_to_decimal,intersect
from constants import RotationType
import pandas as pd
from operator import itemgetter
import collections

START_POSITION = [0,0,0]
DEFAULT_NUMBER_OF_DECIMALS = 3

class Item:
    def __init__(self,id,width,length,height,weight,stackable,availableDate,dueDate,origin,destination):
        self.id = id
        self.weight = weight
        self.width = width
        self.length = length
        self.height = height
        self.stackable = stackable
        self.availableDate = availableDate
        self.dueDate = dueDate
        self.origin = origin
        self.destination = destination
        self.rotation_type = 0
        self.position = START_POSITION
        self.is_packed = False
        self.status = "Unfit"
        self.number_of_decimals = DEFAULT_NUMBER_OF_DECIMALS

    # def format_numbers(self,number_of_decimals):
    #     self.width = set_to_decimal(self.width, number_of_decimals)
    #     self.height = set_to_decimal(self.height, number_of_decimals)
    #     self.length = set_to_decimal(self.length, number_of_decimals)
    #     self.weight = set_to_decimal(self.weight, number_of_decimals)
    #     self.number_of_decimals = number_of_decimals
    
    def get_volume(self):
        return self.width*self.height*self.length

    
    def get_surface_area(self):
        return self.width*self.length


    def string(self):
        return "%s(%sx%sx%s, weight: %s) pos(%s) rt(%s) vol(%s) surf_area(%s)" % (
            self.id, self.width, self.length, self.height, self.weight,
            self.position, self.rotation_type, self.get_volume(), self.get_surface_area()
        )
    
    def get_dimensions(self):
        if self.rotation_type == RotationType.RT_WLH:
            dimension = [self.width, self.length, self.height]
        elif self.rotation_type == RotationType.RT_HWL:
            dimension = [self.height, self.width, self.length]
        elif self.rotation_type == RotationType.RT_HLW:
            dimension = [self.height, self.length, self.width]
        elif self.rotation_type == RotationType.RT_LHW:
            dimension = [self.length, self.height, self.width]
        elif self.rotation_type == RotationType.RT_LWH:
            dimension = [self.length, self.width, self.height]
        elif self.rotation_type == RotationType.RT_WHL:
            dimension = [self.width, self.height, self.length]
        else:
            dimension = [0,0,0]

        return dimension
    
class Console:
    def __init__(self, id, type, max_weight, pivot_weight, rate_to_pivot_weight, rate_above_pivot_weight, fixed_rate, height, length, width, max_volume, origin, destination, departure, arrival):
        self.id = id
        self.type = type
        self.max_weight = max_weight
        self.pivot_weight = pivot_weight
        self.rate_to_pivot_weight = rate_to_pivot_weight
        self.rate_above_pivot_weight = rate_above_pivot_weight
        self.fixed_rate = fixed_rate
        self.height = height
        self.length = length
        self.width = width
        self.max_volume = max_volume
        self.origin = origin
        self.destination = destination
        self.departure = departure
        self.arrival = arrival
        self.items = []
        self.unfitted_items = []
        self.pivot = [START_POSITION]
        self.number_of_decimals = DEFAULT_NUMBER_OF_DECIMALS

    # def format_numbers(self, number_of_decimals):
    #     self.width = set_to_decimal(self.width, number_of_decimals)
    #     self.height = set_to_decimal(self.height, number_of_decimals)
    #     self.length = set_to_decimal(self.length, number_of_decimals)
    #     self.max_weight = set_to_decimal(self.max_weight, number_of_decimals)
    #     self.pivot_weight = set_to_decimal(self.pivot_weight, number_of_decimals)
    #     self.rate_to_pivot_weight = set_to_decimal(self.rate_to_pivot_weight, number_of_decimals)
    #     self.rate_above_pivot_weight = set_to_decimal(self.rate_above_pivot_weight, number_of_decimals)
    #     self.fixed_rate = set_to_decimal(self.fixed_rate, number_of_decimals)
    #     self.max_volume = set_to_decimal(self.max_volume, number_of_decimals)
    #     self.number_of_decimals = number_of_decimals
    
    def get_volume(self):
        return self.height*self.width*self.length

    
    def string(self):
        return "%s(%sx%sx%s, max weight: %s) vol(%s)" % (
            self.id,self.width,self.length,self.height,
            self.max_weight, self.get_volume()
        )
    
    def get_total_weight(self):
        total_weight = 0

        for item in self.items:
            total_weight += item.weight

        return (total_weight)
    
    def get_total_volume(self):
        total_volume = 0

        for item in self.items:
            total_volume += item.get_volume()

        return (total_volume)
    
    def put_item(self, item):
        fit = False
        valid_item_position = item.position
        for p in self.pivot:
            print(item.id,p)
            item.position = p
            # dimension = item.get_dimensions()

            for i in range(len(RotationType.ALL)):
                item.rotation_type = i
                dimension = item.get_dimensions()
                if (
                    self.width < (p[0] + dimension[0]) or
                    self.length < (p[1] + dimension[1]) or
                    self.height < (p[2] + dimension[2]) 
                ):
                    item.status = "out of bounds"
                    continue

                fit = True

                for current_item_in_console in self.items:
                    if intersect(current_item_in_console, item):
                        item.status = "intersects"
                        fit = False
                        break
                     

                if fit:
                    if self.get_total_weight() + item.weight > self.max_weight:
                        item.status = "overweight"
                        fit = False
                        return fit
                    if self.get_total_volume() + item.get_volume() > self.max_volume:
                        item.status = "overTheVolume"
                        fit = False
                        return fit
                    self.items.append(item)

                if fit:
                    item.status = "Fitted"
                    # print(p)
                    print(item.id,fit)
                    item.is_packed = True
                    self.pivot.remove(p)
                    p1 = [p[0] + dimension[0],p[1],p[2]]
                    p2 = [p[0],p[1] + dimension[1],p[2]]
                    p3 = [p[0],p[1],p[2] + dimension[2]]
                    duplicate = False
                    for a in [p1,p2,p3]:
                        if self.pivot:
                            if p == a:
                                duplicate = True
                            for b in self.pivot:
                                if b == a:
                                    duplicate = True
                        else:
                            if p == a:
                                duplicate = True
                        
                        if not (a[0] > self.width or a[1] > self.length or a[2] > self.height):
                            if not duplicate:
                                self.pivot.append(a)
                    self.pivot = sorted(self.pivot, key = itemgetter(1,2))
                    # print(self.pivot)

                if not fit:
                    item.position = valid_item_position
                    continue
                else:
                    return fit
                    

            if not fit:
                item.position = valid_item_position
                continue
            else:
                return fit
        
class Packer:
    def __init__(self):
        self.consoles = []
        self.items = []
        self.unfit_items = []
        self.total_items = 0

    def add_console(self, console):
        return self.consoles.append(console)
    
    def add_item(self, item):
        self.total_items = len(self.items) + 1

        return self.items.append(item)
    
    def pack_to_console(self, console, item):
        fitted = False

        if not console.items:
            response = console.put_item(item)

            if not response:
                console.unfitted_items.append(item)
            else:
                fitted = True
            return

        if console.put_item(item):
            fitted = True
            return
        else:
            console.unfitted_items.append(item)

    def pack(
            self, bigger_first = True, distribute_items = False,
            number_of_decimals = DEFAULT_NUMBER_OF_DECIMALS
    ):
        #for console in self.consoles:
            #console.format_numbers(number_of_decimals)
        
        #for item in self.items:
            #item.format_numbers(number_of_decimals)

        self.consoles.sort(
            key = lambda console: console.get_volume(), reverse=bigger_first
        )

        self.items.sort(
            key= lambda item: item.get_surface_area(), reverse=bigger_first
        )

        for console in self.consoles:
            for item in self.items:
                if item.is_packed == False:
                    self.pack_to_console(console, item)
            
            if distribute_items:
                for item in console.items:
                    self.items.remove(item)