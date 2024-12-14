from enum import Enum
class User:
    _id = 0
    def __init__(self,name,username,password,role,image_path):
        self.id = User._id + 1
        self.image_path = image_path
        self.name = name
        self.username = username
        self.password = password
        self.role = role


class Role(Enum):
    USER = "USER"
    ADMIN = "ADMIN"