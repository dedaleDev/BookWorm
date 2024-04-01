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
            #test si les tables existent
            self.cursor.execute("SHOW TABLES")
            if self.cursor.fetchall() == () :
                print("Base de donnée vide, tentative de création des tables...")
                if self.create_db() == 0:
                    print("Tables créées avec succès !")
                else :
                    exit(1)
        except : 
            print("Base inexistante, tentative de création de la base de donnée...")
            try :
                if self.create_db() == 0:
                    print("Tables créées avec succès !")
                else :
                    exit(1)
            except :
                print("Création de la base de donnée échouée ! Veillez verifier vos paramètres de connexion.")
                exit(1)

    def create_db(self) -> int:
        """This function creates the database and the tables if they don't exist. Returns 0 if the operation is successful, 1 otherwise."""
        try : 
            print("Tentative de création de la base de donnée...")
            print(f"\t# mysql --host={self.host} --user={self.user} --password={self.passwd} -e\"CREATE DATABASE IF NOT EXISTS BookWorm;\"")#creation de la base de donnée
            if os.system(f"mysql --host={self.host} --user={self.user} --password={self.passwd} -e\"CREATE DATABASE IF NOT EXISTS BookWorm;\"")==0 :
                print(f"\t# mysql --host={self.host} --user={self.user} --password={self.passwd} BookWorm < BookWorm.sql")#importation des tables
                if os.system(f"mysql --host={self.host} --user={self.user} --password={self.passwd} BookWorm < BookWorm.sql")==0 : 
                    print("---Base de donnée créée avec succès !---")
                    input("Voulez-vous ajouter des données d'exemple ? (Y/N) : ")
                    if input() == "Y" :
                        if self.loadData() == 0:
                            print("Données ajoutées avec succès !")
                            return 0
                        else :
                            print("Erreur : Impossible d'ajouter le jeu de donnée.")
                    return 0
                else :
                    print("Erreur : Impossible de créer les tables.")
            else :
                    print("Erreur : Impossible de créer la base de donnée.")
        except Exception as e: 
            print("Erreur : Impossible de créer la base de donnée ! Une erreur est survenue : ",e)
        return 1
        
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


    