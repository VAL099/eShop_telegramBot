import os
from abc import ABC, abstractmethod
import sqlite3

class Product(ABC):

    @abstractmethod
    def push2DB(self):
        pass

class Builder(ABC):

    @abstractmethod
    def build(self):
       pass

class Advert(Product):
    
    def __init__(self, name, price, category, subCategory, seller, sellerPhone, description, photo):
        self._name = name
        self._price = price
        self._category = category
        self._subCategory = subCategory
        self._seller = seller
        self._sellerPhone = sellerPhone
        self._description = description
        self._photo = photo

    def push2DB(self, cursor, conn):
        cursor.execute('insert into Products(prodName, price, category, subcategory, seller, sellerPhone, descript, photo) values (?, ?, ?, ?, ?, ?, ?, ?)', 
            (self._name, self._price, self._category, self._subCategory, self._seller, self._sellerPhone, self._description, self._photo))
        conn.commit()
        print('>>New item has been uploaded by {}'.format(self._seller))

class ADV_Build(Builder, Advert):

    def __init__(self):
        self._name = None
        self._price = None
        self._category = None
        self._subCategory = None
        self._seller = None
        self._sellerPhone = None
        self._description = None
        self._photo = ''
    
    def getName(self, name):
        self._name = name
        return self

    def getPrice(self, price):
        self._price = price
        return self

    def getCategory(self, category):
        self._category = category
        return self

    def getSubCategory(self, subCategory):
        self._subCategory = subCategory
        return self

    def getSeller(self, seller):
        self._seller = seller
        return self

    def getSellerPhone(self, cursor, conn, uId):
        req = cursor.execute('select phoneNum from sellers where sellers.userId = ?', (uId,)).fetchall()[0]
        self._sellerPhone, = req
        return self

    def getDescription(self, description):
        self._description = description
        return self

    def getPhoto(self, photo: bytes):
        self._photo = photo
        return self

    def build(self):
        return Advert(self._name, self._price, self._category, self._subCategory, self._seller, self._sellerPhone, self._description, self._photo)