from auxiliary_functions import set_to_decimal,intersect
from constants import RotationType
import pandas as pd

#Define the default position
START_POSITION = [0,0,0]

#define the class for all the items and functions related to it
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
        self.number_of_decimals = DEFAULT_NUMBER_OF_DECIMALS
    
    #function to get volume of a item
    def get_volume(self):
        return self.width*self.height*self.length

    #function to get the largest surface area of a item
    def get_surface_area(self):
        return self.width*self.length

    #function to print all the important attributes of an item
    def string(self):
        return "%s(%sx%sx%s, weight: %s) pos(%s) rt(%s) vol(%s) surf_area(%s)" % (
            self.id, self.width, self.length, self.height, self.weight,
            self.position, self.rotation_type, self.get_volume(), self.get_surface_area()
        )
    
    #function to get the dimensions of an item according to the rotation type
    def get_dimensions(self):
        if self.rotation_type == RotationType.RT_WHL:
            dimension = [self.width, self.height, self.length]
        elif self.rotation_type == RotationType.RT_HWL:
            dimension = [self.height, self.width, self.length]
        elif self.rotation_type == RotationType.RT_HLW:
            dimension = [self.height, self.length, self.width]
        elif self.rotation_type == RotationType.RT_LHW:
            dimension = [self.length, self.height, self.width]
        elif self.rotation_type == RotationType.RT_LWH:
            dimension = [self.length, self.width, self.height]
        elif self.rotation_type == RotationType.RT_WLH:
            dimension = [self.width, self.length, self.height]
        else:
            dimension = [0,0,0]

        return dimension

#Class for the consoles and its function
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
    
    #Function to get volume of the console
    def get_volume(self):
        return self.height*self.width*self.length

    #function to print all the important attributes of the console
    def string(self):
        return "%s(%sx%sx%s, max weight: %s) vol(%s)" % (
            self.id,self.width,self.length,self.height,
            self.max_weight, self.get_volume()
        )
    
    #function to get the total weight of the console at all points
    def get_total_weight(self):
        total_weight = 0
        
        for item in self.items:
            total_weight += item.weight

        return (total_weight)
    
    #function to get the utilised volume of the cosole at all given points
    def get_total_volume(self):
        total_volume = 0

        for item in self.items:
            total_volume += item.get_volume()

        return (total_volume)
    
    #function to check if the item fits into a container or not
    def put_item(self, item):
        fit = False
        valid_item_position = item.position
        for p in self.pivot:
            item.position = p
            dimension = item.get_dimensions()

            for i in range(0, len(RotationType.ALL)):
                item.rotation_type = i
                dimension = item.get_dimensions()
                if (
                    self.width < (p[0] + dimension[0]) or
                    self.height < (p[1] + dimension[1]) or
                    self.length < (p[2] + dimension[2])
                ):
                    continue

                fit = True

                for current_item_in_console in self.items:
                    if intersect(current_item_in_console, item):
                        fit = False
                        break

                if fit:
                    if self.get_total_weight() + item.weight > self.max_weight:
                        fit = False
                        return fit
                    if self.get_total_volume() + item.get_volume() > self.max_volume:
                        fit = False
                        return fit
                    self.items.append(item)

                if fit:
                    item.is_packed = True
                    self.pivot.remove(p)
                    p1,p2,p3 = p
                    p1 = [p[0] + dimension[0],p[1],p[2]]
                    p2 = [p[0],p[1] + dimension[1],p[2]]
                    p3 = [p[0],p[1],p[2] + dimension[2]]
                    self.pivot.extend([p1,p2,p3])

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

#Define the class packer, contains list of all the items and consoles and the functions to pack the given item and add consoles and items
class Packer:
    def __init__(self):
        self.consoles = []
        self.items = []
        self.unfit_items = []
        self.total_items = 0
    
    #function to add console to class Console
    def add_console(self, console):
        return self.consoles.append(console)
    
    #function to add item to class Item
    def add_item(self, item):
        self.total_items = len(self.items) + 1

        return self.items.append(item)
    
    #function to check if a console is empty or not and add item accordingly
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

    #function to sort the items and console and pack items to consoles respectively
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
