
class Carousel():

    def __init__(self): 
        self.counter = 0

    def up(self):
        self.counter += 1
        return self.counter

    def down(self):
        self.counter = self.counter - 1
        return self.counter

    def current(self):
        return self.counter

def userReg(cursor, conn, user_id: int, user_name: str, username: str, phoneNum: str):

    cursor.execute('INSERT INTO sellers (userId, namee, username, phoneNum) VALUES (?, ?, ?, ?)', (user_id, user_name, username, phoneNum))
    conn.commit()

def img2bin(fileDir):
    with open(fileDir, 'rb') as file:
        data = file.read()
    return data

def handleUserRequest(cursor, cat, subcat):
    goods = []
    out = cursor.execute('select * from products where category = ? and subcategory = ?',(cat, subcat,)).fetchall()
    for data in out:
        goods.append(data)
    return goods

def reqSellersADV(cursor, username):
    goods = []
    out = cursor.execute('select * from products where seller = ?',(username,)).fetchall()
    for data in out:
        goods.append(data)
    return goods

def rmADV(cursor, conn, aId):

    cursor.execute('delete from products where prodId = {}'.format(aId))
    conn.commit()

def observerHandler(cursor, uuid):
    users = []
    out = cursor.execute('select userId from SearchHistory').fetchall()
    for user in out:
        users.append(user)
    res = False
    for i in range(len(users)):
        u, = users[i]
        if u == uuid:
            res = True
        
    return res