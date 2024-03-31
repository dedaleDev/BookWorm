import pymysql

class db():
    def __init__(self, host:str ="localhost", user:str="root", passwd:str="1234") -> None:
        self.host = host
        self.user = user
        self.passwd = passwd
        #-----initialisation de la base de donnée-----
        try :
            self.db = pymysql.connect(host=self.host, charset="utf8mb4",user=self.user, passwd=self.passwd, db="BookWorm")
            self.cursor = self.db.cursor()
        except : 
            print("Base inexistante, tentative de création de la base de donnée...")
            try :
                self.create_db()
            except :
                print("Création de la base de donnée échouée ! Veillez verifier vos paramètres de connexion.")
                exit()

    def create_db(self) -> None:
        self.db = pymysql.connect(host=self.host, charset="utf8mb4", user=self.user, passwd=self.passwd)
        self.cursor = self.db.cursor()
        try:
            with open("BookWorm.sql") as f:
                sql = f.read()
                self.cursor.execute(sql)
                self.cursor.fetchall()
                self.db.commit()
        except:
            print("Impossible de créer la base de donnée ! Le fichier BookWorm.sql est introuvable.")
            exit()


        
        self.db = pymysql.connect(host=self.host, charset="utf8mb4", user=self.user, passwd=self.passwd, db=db)


    