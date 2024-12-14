from datetime import datetime
from enum import Enum

class Transaction:
    _id = 0
    def __init__(self,user_id,user_name,offer_name,billing_type,payment):
        self.id = Transaction._id + 1
        self.user_id = user_id
        self.user_name = user_name
        self.offer_name = offer_name
        self.billing_type = billing_type
        self.payment = payment #float
        self.date = datetime.now()


class Cart:
    _id = 0

    def __init__(self, user_id, offer):
        Cart._id += 1
        self.id = Cart._id
        self.user_id = user_id
        self.offer = offer

class Billing(Enum):
    BANK = "BANK"
    COD = 'COD'

