from enum import Enum



class Category(Enum):
    Unknown = 0
    Vehicle = 1
    Pedestrian = 2
    Cyclist = 3
    TrafficCone = 4
    Trailer = 5
    Other = 6


class SubCategory(Enum):
    Unknown = 0
    Car = 1
    Van = 2
    Bus = 3
    Truck = 4
    Motorcycle = 5


SUBCATEGORY_RELATIONS = {c:[SubCategory.Unknown] for c in Category}

SUBCATEGORY_RELATIONS[Category.Vehicle] += [
    SubCategory.Car, 
    SubCategory.Van, 
    SubCategory.Bus, 
    SubCategory.Truck, 
    SubCategory.Motorcycle,
]