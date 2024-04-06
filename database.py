import pymysql
import os, csv

class db():

    _requetes = {
    "insertLivre" : "insert into Livre (ISBN, Titre, Auteur, Description, Note, Date de parution, Statut, Genre, Format, Prix, Point de vente, Editeur) values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');",
    "insertAuteur" : "insert into Auteur (Nom, Prénom, Biographie, Date de naissance, Date de décès, Alias) values ('{}','{}','{}','{}','{}','{}');",
    "insertEditeur" : "insert into Editeur (Nom, Adresse) values ('{}','{}');",
    "insertEmprunt" : "insert into Emprunt (Livre, Date, Utilisateur) values ('{}','{}','{}');",
    "insertPointDeVente" : "insert into Point de vente (Adresse, Nome, Site web, Tel) values ('{}','{}','{}','{}');",
    "insertUtilisateur" : "insert into Utilisateur (email, mdp, Grade, Nom, Prénom, Adresse, Tel) values ('{}','{}','{}','{}','{}','{}');",
    "insertNote" : "insert into Note (Note, Utilisateur, Livre) values ('{}','{}','{}');",}

    def __init__(self, host:str ="localhost", user:str="root", passwd:str="1234") -> None:
        self.host = host
        self.user = user
        self.passwd = passwd
        #-----initialisation de la base de donnée-----
        try :
            self.db = pymysql.connect(host=self.host, charset="utf8mb4",user=self.user, passwd=self.passwd, db="BookWorm")
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
        self.cursor = self.db.cursor()
        #test si les tables existent
        self.cursor.execute("SHOW TABLES")
        tablesLoad = []
        for table in self.cursor.fetchall():
            tablesLoad.append(table[0])
        self.list_tables = ["Auteur","Editeur","Emprunt","Livre","Point de vente", "Utilisateur"]
        if tablesLoad == () :
            print("Base de donnée vide, tentative de création des tables...")
            if self.create_db() == 0:
                print("Tables créées avec succès !")
            else :
                exit(1)
        if tablesLoad != self.list_tables:
            print("Erreur : Base de donnée corrompue ! Les tables ne correspondent pas avec le modèle UML attendu, veuillez vérifier vos tables.")
            print("Tables attendues : ",self.list_tables)
            print("Tables trouvées : ",tablesLoad)
            if input("Voulez-vous réinitialiser la base de donnée ? (Y/N) : ") == "Y":
                try :
                    self.cursor.execute("DROP DATABASE BookWorm")
                    if self.create_db() == 0:
                        print("Tables créées avec succès !")
                    else :
                        exit(1)
                except :
                    print("Erreur : Impossible de supprimer la base de donnée !")
                    exit(1)

    def mkRequest(self, request:str, verbose=True, *args) -> None:
        """This function executes a request with the given arguments. Warning, this function not commit the request."""
        try :
            if verbose:
                print(f"# {self._requetes[request].format(*args)}")
            self.cursor.execute(self._requetes[request].format(*args))
        except Exception as e:
            print("Erreur : Impossible de créer la requête ! Une erreur est survenue : ",e)

    def create_db(self) -> int:
        """This function creates the database and the tables if they don't exist. Returns 0 if the operation is successful, 1 otherwise."""
        try : 
            print(f"\t# mysql --host={self.host} --user={self.user} --password={self.passwd} -e\"CREATE DATABASE IF NOT EXISTS BookWorm;\"")#creation de la base de donnée
            if os.system(f"mysql --host={self.host} --user={self.user} --password={self.passwd} -e\"CREATE DATABASE IF NOT EXISTS BookWorm;\"")==0 :
                print(f"\t# mysql --host={self.host} --user={self.user} --password={self.passwd} BookWorm < template.sql")#importation des tables
                if os.system(f"mysql --host={self.host} --user={self.user} --password={self.passwd} BookWorm < template.sql")==0 : 
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
        """This function loads the data from the data folder into the database."""
        self.db = pymysql.connect(host=self.host, charset="utf8mb4", user=self.user, passwd=self.passwd, db="BookWorm")
        data= ["data/Auteur.csv","data/Editeur.csv","data/Emprunt.csv","data/Livre.csv","data/Note.csv","data/Point de vente.csv","data/Utilisateur.csv"]
        for file in data:
            try :
                with open(file, 'r', encoding="utf-8") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        self.mkRequest("insert"+file.split("/")[-1].split(".")[0], False, *row)
                    self.db.commit()
            except FileNotFoundError or PermissionError as e:
                print(f"Erreur : Impossible de trouver le fichier {file}  dans le repertoire data ! Le fichier n'existe pas ou vous n'avez pas les droits pour le lire.",e)
                return 1
            except Exception as e:
                print(f"Erreur : Impossible de lire le fichier {file} ! Une erreur est survenue : ",e)
                return 1