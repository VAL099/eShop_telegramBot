
class Component():

    def decorate(self): pass

class ConcreteComponent(Component):

    def decorate(self, component):
        return component

class Decorator(Component):

    def __init__(self, advert):
        self._advert = advert

    def decorate(self):
        return self._advert.decorate()

class PriceDecor(Decorator):

    def __init__(self, status, pId):
        self._decorStatus = status
        self._pId = pId

    def decorate(self, cursor, conn):
        cursor.execute('update products set priceLabel = {} where prodId = {}'.format(self._decorStatus, self._pId))
        conn.commit()

class QualityDecor(Decorator):

    def __init__(self, status, pId):
        self._decorStatus = status
        self._pId = pId

    def decorate(self, cursor, conn):
        cursor.execute('update products set qualityLabel = {} where prodId = {}'.format(self._decorStatus, self._pId))
        conn.commit()