import mysql.connector

class MysqlDatabase:
    def __init__(self, host, user, password, database):
        self.host = host

    def getHost(self):
        return self.host