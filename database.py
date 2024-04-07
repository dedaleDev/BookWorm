import pymysql
import os, csv

class db():

    _requetes = {
    "insertLivre" : "INSERT INTO Livre (`ISBN`, `Titre`, `Auteur`, `Description`, `Note`, `Date de parution`, `Statut`, `Genre`, `Format`, `Prix`, `Point de vente`, `Editeur`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
    "insertAuteur" : "INSERT INTO Auteur (`Nom`, `Prénom`, `Biographie`, `Date de naissance`, `Date de décès`, `Alias`) VALUES (%s,%s,%s,%s,%s,%s);",
    "insertEditeur" : "INSERT INTO Editeur (`Nom`, `Adresse`) VALUES (%s,%s);",
    "insertEmprunt" : "INSERT INTO Emprunt (`Livre`, `Date`, `Utilisateur`) VALUES (%s,%s,%s);",
    "insertPointDeVente" : "INSERT INTO Point de vente (`Adresse`, `Nom`, `Site web`, `Tel`) VALUES (%s,%s,%s,%s);",
    "insertUtilisateur" : "INSERT INTO Utilisateur (`email`, `mdp`, `Grade`, `Nom`, `Prénom`, `Adresse`, `Tel`) VALUES (%s,%s,%s,%s,%s,%s,%s);",
    "insertNote" : "INSERT INTO Note (`Note`, `Utilisateur`, `Livre`) values (%s,%s,%s);",
    }

    def __init__(self, host:str ="localhost", user:str="root", passwd:str="1234", debug=False) -> None:
        self.host = host
        self.user = user
        self.passwd = passwd
        self.debug = debug
        #-----initialisation de la base de donnée-----
        try :
            self.db = pymysql.connect(host=self.host, charset="utf8mb4",user=self.user, passwd=self.passwd, db="BookWorm", init_command='SET sql_mode="NO_ZERO_IN_DATE,NO_ZERO_DATE"')
            if self.debug : 
                self.cursor = self.db.cursor()
                self.cursor.execute("DROP DATABASE IF EXISTS BookWorm")
                self.db.commit()
                print("Conformément au mode debug, la base de donnée à été effacé au démarrage.")
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
        self.list_tables = ["Auteur","Editeur","Emprunt","Livre","Note","Point de vente", "Utilisateur"]
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
            # Convertir les arguments en chaînes de caractères, ajouter des guillemets autour des chaînes de caractères, et gérer les valeurs NULL
            args = [f"{arg.replace("'", "''")}" if arg is not None and arg != "None" else "NULL" for arg in args]
            for i in range(len(args)):
                if args[i] == "''":
                    print("--#-(remove)-#--")
                    args[i] = "NULL"
                if args[i] == '':
                    args.pop(i)
            print(args)
            # Supprimer la virgule après la dernière valeur
            args = args[:-1] + [args[-1].rstrip(",")]
            if verbose:
                print(f"# {self._requetes[request] % tuple(args)}")
            self.cursor.execute(self._requetes[request], tuple(args))
        except Exception as e:
            print(f" La requête à échouée : {self._requetes[request] % tuple(args)}\n---, Erreur : {e}, ligne : {e.__traceback__.tb_lineno}")
            print(f"Nombre de placeholders : {self._requetes[request].count('%s')}")
            print(f"Nombre d'arguments : {len(args)}\n-------------------------------------------------- ")

    def create_db(self) -> int:
        """This function creates the database and the tables if they don't exist. Returns 0 if the operation is successful, 1 otherwise."""
        try : 
            print(f"\t# mysql --host={self.host} --user={self.user} --password={self.passwd} -e\"CREATE DATABASE IF NOT EXISTS BookWorm;\"")#creation de la base de donnée
            if os.system(f"mysql --host={self.host} --user={self.user} --password={self.passwd} -e\"CREATE DATABASE IF NOT EXISTS BookWorm;\"")==0 :
                print(f"\t# mysql --host={self.host} --user={self.user} --password={self.passwd} BookWorm < template.sql")#importation des tables
                if os.system(f"mysql --host={self.host} --user={self.user} --password={self.passwd} BookWorm < template.sql")==0 : 
                    print("---Base de donnée créée avec succès !---")
                    if input("Voulez-vous ajouter des données d'exemple ? (Y/N) : ") == "Y" :
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
        self.db = pymysql.connect(host=self.host, charset="utf8mb4", user=self.user, passwd=self.passwd, db="BookWorm",init_command='SET sql_mode="NO_ZERO_IN_DATE,NO_ZERO_DATE"')
        data= ["data/Auteur.csv","data/Editeur.csv","data/Emprunt.csv","data/Livre.csv","data/Note.csv","data/Point de vente.csv","data/Utilisateur.csv"]
        for file in data:
            try :
                idTable = ["data/Auteur.csv","data/Note.csv","data/Emprunt.csv"]
                with open(file, 'r', encoding="utf-8") as f:
                    reader = csv.reader(f, delimiter=',')
                    id = False
                    next(reader)
                    self.cursor = self.db.cursor()
                    for row in reader:
                        print(len(row)-1)
                        if file in idTable:
                            row.pop(0)
                        if ',' in row[-1]:
                            row[-1] = row[-1].split(',')[0] 
                        print('-----ROW', row)
                        self.mkRequest("insert"+file.split("/")[-1].split(".")[0], False, *row)
                    self.db.commit()
            except FileNotFoundError or PermissionError as e:
                print(f"Erreur : Impossible de trouver le fichier {file}  dans le repertoire data ! Le fichier n'existe pas ou vous n'avez pas les droits pour le lire.",e)
                return 1
            except Exception as e:
                print(f"Erreur : Impossible de lire le fichier {file} ! Une erreur est survenue : ",e, e.__traceback__.tb_lineno)
                return 1