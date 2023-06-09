import sqlite3

class ConnectDB:
    
    __instance = None

    @staticmethod
    def getInstance():
        if ConnectDB.__instance == None:
            ConnectDB()
        return ConnectDB.__instance

    def __init__(self):
        if ConnectDB.__instance != None:
            raise Exception("Cannot be initialised multiple times!")
        else:
            ConnectDB.__instance = self

    def connect(self):

        conn = sqlite3.connect('db/shoppyBot.db', check_same_thread = False)
        if conn != None:
            print ("DB reached! Connection established!")
        else:
            print("Cannot reach the DB! Please check connection!")
        return conn