from abc import ABC
from handlers import *

class IDataBase(ABC):

    def storeList(self): pass

class DataBase(IDataBase):

    def getList4Customer(self, cursor, cat, subcat):
        goods = []
        out = cursor.execute('select * from products where category = ? and subcategory = ?',(cat, subcat,)).fetchall()
        for data in out:
            goods.append(data)
        return goods

    def getList4Seller(self, cursor, username):
        goods = []
        out = cursor.execute('select * from products where seller = ? ',(username,)).fetchall()
        for data in out:
            goods.append(data)
        return goods    

class ProxyDB(IDataBase):

    def __init__(self):
        self.DB = DataBase()
        self.goodsList = None

    def storeList4Customer(self, cursor, cat, subcat):
        self.goodsList = self.DB.getList4Customer(cursor, cat, subcat)
        return self

    def storeList4Seller(self, cursor, username):
        self.goodsList = self.DB.getList4Seller(cursor, username)
        return self