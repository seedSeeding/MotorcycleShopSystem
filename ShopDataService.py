from operator import index

from User import User,Role
from Transaction import Transaction,Cart,Billing
from Offer import Offer,Type

class DataService:
    _users = [User("rgrrgr","a","a",Role.USER.value,"./assets/Images/black-bg.jpg"),User("rgrgrg","b","b",Role.ADMIN.value,"./assets/Images/black-bg.jpg")]
    _carts = []
    _transactions = []
    _offers = [Offer(Type.PART.value,"./assets/Images/black-bg.jpg","grwgrw",234),Offer(Type.PART.value,"./assets/Images/black-bg.jpg","jsjs",234)
               ,Offer(Type.PART.value,"./assets/Images/black-bg.jpg","jsgrgrwgrwgjs",234),Offer(Type.PART.value,"./assets/Images/black-bg.jpg","jsjs",234),Offer(Type.PART.value,"./assets/Images/black-bg.jpg","jsjs",234)
               ,Offer(Type.PART.value,"./assets/Images/black-bg.jpg","jsjrgrs",234),Offer(Type.PART.value,"./assets/Images/black-bg.jpg","jsjs",234),Offer(Type.PART.value,"./assets/Images/black-bg.jpg","jsjs",234)]
    def users(self):
        return DataService._users
    def carts(self):
        return DataService._carts
    def transactions(self):
        return DataService._transactions

    def offers(self):
        return DataService._offers
    def delete_offer(self,offer_id):
        for index in 0, len(self.offers()):
            if offer_id == self.offers()[index].id:
                offer = self.offers().pop(index)
                return True
        return False
    def update_offer(self,offer):
        for index in 0, len(self.offers()):
            if offer.id == self.offers()[index].id:
                self.offers()[index] = offer
                return True
        return False
    def create_offer(self,_type,image_path,name,price):
        offer = Offer(_type,image_path,name,price)
        self.offers().append(offer)


    def register_user(self,name,username,password,role,image):
        user = User(name,username,password,role,image)
        self.users().append(user)
        return user

    def user_login(self,username,password):
        for user in self.users():
            if user.username == username and user.password == password:
                return user
        return True

    def get_user_cart(self,user_id):
        user_cart = []
        for cart in self.carts():
            if cart.user_id == user_id:
                user_cart.append(cart)
        return user_cart or []

    def get_transactions(self):
        return self._transactions
    def get_user_orders(self,user_id):
        user_tran = []
        for tran in self.transactions():
            if tran.user_id == user_id:
                user_tran.append(tran)
        return user_tran or []

    def cancel_order(self,_id):
        for index in 0,len(self.transactions()):
            if _id == self.transactions()[index].id:
                tran = self.transactions().pop(index)
                return True
        return False

    def add_transaction(self,_id,user_name,offer_name,billing_type,payment):
        tran = Transaction(_id,user_name,offer_name,billing_type,payment)
        self.transactions().append(tran)
        return tran

    def add_to_cart(self,user_id, offer):
        cart = Cart(user_id, offer)
        self.carts().append(cart)
        return True

    def remove_to_cart(self,_id):
        for index in range(0,len(self.carts())):
            if _id == self.carts()[index].id:
                cart = self.carts().pop(index)

                return True
        return False