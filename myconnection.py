from pymysql import *

class myconnection:
    def connect(self):
        conn=connect('localhost','root','','bestprice')
        return conn

