import pymysql
import os

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
        try : 
            os.system(f"mysql --host={self.host} --user={self.user} --password={self.passwd} -e\"CREATE DATABASE IF NOT EXISTS BookWorm;\"")#creation de la base de donnée
            os.system(f"mysql --host={self.host} --user={self.user} --password={self.host} BookWorm < BookWorm.sql")#importation des tables
            print("Base de donnée créée avec succès !")
            input("Voulez-vous ajouter des données d'exemple ? (Y/N) : ")
            if input() == "Y" :
                self.loadData()
                print("Données ajoutées avec succès !")
        except : 
            print("Impossible de créer la base de donnée !")
            return
        
    def loadData(self) -> None:
        self.db = pymysql.connect(host=self.host, charset="utf8mb4", user=self.user, passwd=self.passwd, db="BookWorm")
        table= [False for i in range(6)]
        with open('data.csv', 'r') as file:
            for line in file:
                if line == """"ID","Nom","Prénom","Biographie","Date de naissance","Date de décès""""" :#à optimiser car pour le moment c'est dégeulasse
                    table= [False for i in range(6)]
                    table[0] = True
                elif line == """"Nom","Adresse""""":
                    table= [False for i in range(6)]
                    table[1] = True
                elif line == """"Nom","Adresse""""":
                    table= [False for i in range(6)]
                    table[1] = True
                else :
                    print(line)
                data = line.split(',')
                
                self.cursor.execute(f"INSERT INTO books (title, author, year, isbn) VALUES ('{data[0]}', '{data[1]}', {data[2]}, {data[3]})")
                self.db.commit()


    