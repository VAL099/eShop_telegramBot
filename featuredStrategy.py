from abc import ABC, abstractmethod
from random import randint

class Strategy(ABC):
    @abstractmethod
    def execute_alg(self): pass

class PromoteByPriceLabel(Strategy):
    def execute_alg(self, cursor, uuid):
        print('By_Price')
        adverts = []
        out = cursor.execute('select * from products where priceLabel = 1').fetchall()
        for data in out:
            adverts.append(data)
        return adverts

class PromoteByQualityLabel(Strategy):
    def execute_alg(self, cursor, uuid):
        print('By_Quality')
        adverts = []
        out = cursor.execute('select * from products where qualityLabel = 1').fetchall()
        for data in out:
            adverts.append(data)
        return adverts

class PromoteByHistory(Strategy):
    def execute_alg(self, cursor, uuId):
        print('By_History')
        data = cursor.execute('select reqCat, reqSubcat from SearchHistory where userId = ?', (uuId,)).fetchall()[0]
        cat, subcat = data
        adverts = []
        out = cursor.execute('select * from products where category = ? and subcategory = ? and qualityLabel = 1 UNION select * from products where category = ? and subcategory = ? and priceLabel = 1', (cat, subcat, cat, subcat)).fetchall()
        for data in out:
            adverts.append(data)
        return adverts

class Context():
    def __init__(self, strategy):
        self._strategy = strategy

    @property
    def strateg(self):
        return self._strategy
    
    @strateg.setter
    def strateg(self, strategy: Strategy):
        self._strategy = strategy

    def select_alg(self, cursor, uuId):
        response = self._strategy.execute_alg(self, cursor, uuId)
        return response
