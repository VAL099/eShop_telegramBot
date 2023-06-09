from abc import ABC

from handlers import observerHandler
from proxyDB import *

class Subject(ABC):
    def attach_obv(self): pass
    def detach_obv(self): pass
    def notify(self): pass

class featuredGenerator(Subject):

    observers = []
    def __init__(self, observer):
        self._observer = observer

    def attach_obv(self, observer):
        self.observers.append(observer)
        print('{} attached to me!'.format(observer))
        
    def detach_obv(self):
        self.observers.remove(self._observer)

    def notify(self, username, cat, subcat):
        for eachObserver in self.observers:
            eachObserver.react(cat, subcat)
            print('{} just make a search on {},{}'.format(username, cat, subcat))

class Observer(ABC):
    def react(self):
        pass

class searchObserver(Observer):

    def react(self, cursor, conn, uuId, cat, subcat):
        controlReq = observerHandler(cursor, uuId)
        print('Status =',controlReq)
        if controlReq == True:
            cursor.execute('update searchHistory set reqCat = ?, reqSubcat = ? where userId = {}'.format(uuId), (cat, subcat))
            conn.commit()
            print('Updated!')
        elif controlReq == False:
            cursor.execute('insert into searchHistory(userId, reqCat, reqSubcat) values (?,?,?)', (uuId, cat, subcat))
            conn.commit()
            print('Registered!')