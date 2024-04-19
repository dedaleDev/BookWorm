import pymysql
import os, csv

class db():
    _requetes = {
    "insertLivre" : "INSERT INTO `Livre` (`ISBN`, `Titre`, `Auteur`, `Description`, `Note`, `Date de parution`, `Statut`, `Genre`, `Format`, `Prix`, `Point de vente`, `Editeur`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
    "insertAuteur" : "INSERT INTO `Auteur` (`Nom`, `Prénom`, `Biographie`, `Date de naissance`, `Date de décès`,`Alias`) VALUES (%s,%s,%s,%s,%s,%s);",
    "insertEditeur" : "INSERT INTO `Editeur` (`Nom`, `Adresse`) VALUES (%s,%s);",
    "insertEmprunt" : "INSERT INTO `Emprunt` (`Livre`, `Date`, `Utilisateur`) VALUES (%s,%s,%s);",
    "insertPointDeVente" : "INSERT INTO `Point de vente` (`Adresse`, `Nom`, `Site web`, `Tel`) VALUES (%s,%s,%s,%s);",
    "insertUtilisateur" : "INSERT INTO `Utilisateur` (`email`, `mdp`, `Grade`, `Nom`, `Prénom`, `Adresse`, `Tel`) VALUES (%s,%s,%s,%s,%s,%s,%s);",
    "insertNote" : "INSERT INTO `Note` (`Note`, `Utilisateur`, `Livre`) values (%s,%s,%s);",
    "selectAuteurByNom" : "SELECT * FROM `Auteur` WHERE `Nom` Like %s ORDER BY `ID` ASC;",
    "selectAuteurByID" : "SELECT * FROM `Auteur` WHERE `ID` = %s;",
    "selectAuteurByPrenom" : "SELECT * FROM `Auteur` WHERE `Prénom` LIKE %s ORDER BY `ID` ASC;",
    "selectAuteurByAlias" : "SELECT * FROM `Auteur` WHERE `Alias` LIKE %s ORDER BY `ID` ASC;",
    "selectPointDeVenteByNom" : "SELECT * FROM `Point de vente` WHERE `Nom` LIKE %s;",
    "selectPointDeVenteByAdresse" : "SELECT * FROM `Point de vente` WHERE `Adresse` LIKE %s;",
    "selectLivreByISBN" : "SELECT * FROM `Livre` WHERE `ISBN` LIKE %s;",
    "selectLivreByTitre" : "SELECT * FROM `Livre` WHERE `Titre` LIKE %s;",
    "selectLivreByAuteurNom" : "SELECT * FROM Livre JOIN Auteur ON Livre.Auteur = Auteur.ID WHERE Auteur.Nom LIKE %s",
    "selectLivreByAuteurPrénom" : "SELECT * FROM Livre JOIN Auteur ON Livre.Auteur = Auteur.ID WHERE Auteur.Prénom LIKE %s",
    "selectLivreByAuteurAlias" : "SELECT * FROM Livre JOIN Auteur ON Livre.Auteur = Auteur.ID WHERE Auteur.Alias LIKE %s;",
    "selectLivreByDescription" : "SELECT * FROM `Livre` WHERE `Description` LIKE %s;",
    "selectLivreByGenre" : "SELECT * FROM `Livre` WHERE `Genre` LIKE %s;",
    "selectEditeurByNom" : "SELECT * FROM `Editeur` WHERE `Nom` LIKE %s;",
    "selectEditeurByAdresse" : "SELECT * FROM `Editeur` WHERE `Adresse` LIKE %s;",
    "deleteLivre" : "DELETE FROM `Livre` WHERE `ISBN` = %s;",
    "deleteLivreByAuteur" : "DELETE FROM `Livre` WHERE `Auteur` = %s;",
    "deleteAuteur" : "DELETE FROM `Auteur` WHERE `ID` = %s;",
    "deletePointDeVente" : "DELETE FROM `Point de vente` WHERE `Adresse` = %s;",
    "deleteEditeur" : "DELETE FROM `Editeur` WHERE `Nom` = %s;",
    "deleteLivreByEditeur" : "DELETE FROM `Livre` WHERE `Editeur` = %s;",
    "updateLivrePointDeVente" : "UPDATE `Livre` SET `Point de vente` = %s WHERE  `Point de vente`  = %s;",
    "updateLivre" : "UPDATE `Livre` SET `Titre` = %s, `Auteur` = %s, `Description` = %s, `Note` = %s, `Date de parution` = %s, `Statut` = %s, `Genre` = %s, `Format` = %s, `Prix` = %s, `Point de vente` = %s, `Editeur` = %s WHERE `ISBN` = %s;",
    "updateAuteur" : "UPDATE `Auteur` SET `Nom` = %s, `Prénom` = %s, `Biographie` = %s, `Date de naissance` = %s, `Date de décès` = %s, `Alias` = %s WHERE `ID` = %s;",
    "updatePointDeVente" : "UPDATE `Point de vente` SET `Nom` = %s, `Site web` = %s, `Tel` = %s WHERE `Adresse` = %s;",
    "updateEditeur" : "UPDATE `Editeur` SET `Adresse` = %s WHERE `Nom` = %s;"
    }

    def __init__(self, host:str ="localhost", user:str="root", passwd:str="1234", port:int=3306, debug:bool=False) -> None:
        """This function initializes the database object."""
        self.host = host
        self.user = user
        self.passwd = passwd
        self.port = port
        self.debug = debug
        self.needRestart = False
        #-----initialisation de la base de donnée-----
        try :
            self.db = pymysql.connect(host=self.host, charset="utf8mb4",user=self.user, passwd=self.passwd, port=self.port, db="BookWorm", init_command='SET sql_mode="NO_ZERO_IN_DATE,NO_ZERO_DATE"')
            if self.debug : 
                self.cursor = self.db.cursor()
                self.cursor.execute("DROP DATABASE IF EXISTS BookWorm")
                self.db.commit()
                print("Conformément au mode debug, la base de donnée à été effacé au démarrage. Veuillez relancer le programme.")
                self.needRestart = True
                return
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

    def mkRequest(self, request:str, verbose=False, *args) -> None:
        """This function executes a request on the database.
        Args:
            request : str : the request to execute on the database (must be in the _requetes dictionary)
            verbose : bool : if True, the request is displayed on the console
            *args : tuple : the arguments to pass to the request
        """
        try :
            # Convertir les arguments en chaînes de caractères, ajouter des guillemets autour des chaînes de caractères, et gérer les valeurs NULL
            args = list(args)
            for i in range(len(args)):
                if args[i] == "":
                    args[i] = None
            if verbose :
                print(f"#{self._requetes[request] % tuple(args)}")
            self.cursor.execute(self._requetes[request], tuple(args))
        except Exception as e:
            print(f" La requête à échouée : {self._requetes[request] % tuple(args)}\n---, Erreur : {e}, ligne : {e.__traceback__.tb_lineno}")
            print("Args : ", args)
            print(f"Nombre de placeholders : {self._requetes[request].count('%s')}")
            print(f"Nombre d'arguments : {len(args)}\n-------------------------------------------------- ")

    def __str__(self) -> str:
        return f"Database host : {self.host}, user : {self.user}, password : {self.passwd}, port : {self.port}, debug : {self.debug}"

    def create_db(self) -> int:
        """This function creates the database and the tables.
        Return :
            0 : if the database is created successfully
            1 : if an error occurs
        """
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
        
    def loadData(self) -> int:
        """This function loads the data from the data folder into the database.
        Return :
            0 : if the data is loaded successfully
            1 : if an error occurs
        """
        self.db = pymysql.connect(host=self.host, charset="utf8mb4", user=self.user, passwd=self.passwd, port=self.port, db="BookWorm",init_command='SET sql_mode="NO_ZERO_IN_DATE,NO_ZERO_DATE"')
        data= ["data/Auteur.csv","data/Editeur.csv","data/PointDeVente.csv","data/Livre.csv","data/Utilisateur.csv","data/Note.csv","data/Emprunt.csv"]
        for file in data:
            try :
                idTable = ["data/Auteur.csv","data/Note.csv","data/Emprunt.csv"]
                with open(file, 'r', encoding="utf-8") as f:
                    reader = csv.reader(f, delimiter=';')
                    id = False
                    next(reader)
                    self.cursor = self.db.cursor()
                    for row in reader:
                        if row == []:
                            continue
                        if file in idTable:
                            row.pop(0)
                        #if  ',' in row[-1]: #desativé pour le moment car inutile à priori à voir dans le temps #danger 
                            #row[-1] = row[-1].split(',')[0]
                        self.mkRequest("insert"+file.split("/")[-1].split(".")[0], False, *row)
                    self.db.commit()
            except FileNotFoundError or PermissionError as e:
                print(f"Erreur : Impossible de trouver le fichier {file}  dans le repertoire data ! Le fichier n'existe pas ou vous n'avez pas les droits pour le lire.",e)
                return 1
            except Exception as e:
                print(f"Erreur : Impossible de lire le fichier {file} ! Une erreur est survenue : ",e, "ligne : ", e.__traceback__.tb_lineno)
                return 1
        return 0
    