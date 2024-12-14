from enum import Enum
class Offer:
    _id = 0
    def __init__(self,_type,image_path,name,price):
        self.id = Offer._id + 1
        self.image_path = image_path
        self.type = _type
        self.name = name
        self.price = price


class Type(Enum):
    SERVICE = "SERVICE"
    PART = "PART"
