import pymysql

class db():
    def __init__(self, host:str ="localhost", user:str="root", passwd:str="1234", db:str="BookWorm") -> None:
        self.host = host
        self.user = user
        self.passwd = passwd
        #-----initialisation de la base de donnée-----
        self.db = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db)