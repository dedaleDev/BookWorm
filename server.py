import operationOnDataBase, database, utils, searchEngine
import cherrypy, os, json, shutil, random

class Server(object):
    def __init__(self, db:database.db, conf:dict):
        self.db = db
        self.conf = conf
        self.bestLivres = []
        self.timeToRefresh = 0

    def makeResponse(self, is_error=False, content=None, error_message=None):
        """This function creates a JSON response for API.
        Args : 
            is_error : bool, True if an error occured
            content : any, content of the response
            error_message : str, error message
        Returns :
            dict, JSON response"""
        try : 
            response = cherrypy.response
            if not is_error:
                return {"status":"ok", "content":content}
            else:
                return {"status":"error", "message":error_message}
        except Exception as e:
            print(" \033[31mErreur lors de la création de la réponse : ",e, e.__traceback__.tb_lineno, content, error_message, "\033[0m")
            
    def cleanImageLivres(self) :
        """This function deletes all images who don't have a corresponding book in the database."""
        try : 
            self.db.mkRequest("selectAllISBN", False)
            isbn = self.db.cursor.fetchall()
            ISBN = []
            for i in isbn :
                ISBN.append(i[0])
            if ISBN != [] :
                for i in os.listdir("www/img/livres"):
                    if i.split('.')[0] not in ISBN and i.split('.')[1].endswith('jpg') :
                        os.remove(f"www/img/livres/{i}")
        except PermissionError as e:
            print("\033[31mErreur lors de la suppression des images vous n'avez pas les droits nécessaires.",e, e.__traceback__.tb_lineno, "\033[0m")
        except Exception as e:
            print("\033[31mErreur lors de la suppression des images : ",e, e.__traceback__.tb_lineno, "\033[0m")
    
    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def searchLivre(self, search:str, sort:str, auteur:str="all") -> str:
        """This API searches for a book in the database.
        Args :
            search : str, search query
            sort : str, sort method
            auteur : str, author name
        Returns :
            str, JSON response"""
        sortList = ["sortByPertinence","sortByAlpha", "sortByNote", "sortByDate", "sortByPrix"]
        if sort not in sortList:
            sort = "sortByPertinence"
        try : 
            searchResult = searchEngine.searchLivre(search,self.db)
            if searchResult == None : return None
            searchResult= operationOnDataBase.sortLivre(searchResult,sort)
            if auteur != "all":
                searchResult = operationOnDataBase.filterLivreByAuteur(searchResult, auteur, self.db)
            searchResult = utils.formatLivreToJsonOrdered(searchResult, self.db)
            return self.makeResponse(content=searchResult)
        except Exception as e:
            print("\033[31mErreur lors de la recherche : ",e, e.__traceback__.tb_lineno, searchResult, "\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue !")

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def searchAuteur(self, search:str) -> str:
        """This API searches for an author in the database.
        Args :
            search : str, search query
        Returns :
            str, JSON response"""
        try : 
            searchResult = searchEngine.searchAuteur(search, self.db)
            if searchResult == None : return None
            searchResult = utils.formatAuteurToJson(searchResult)
            return self.makeResponse(content=searchResult)
        except Exception as e:
            print("\033[31mErreur lors de la recherche : ",e, e.__traceback__.tb_lineno, "\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue ! ")

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def searchPointDeVente(self, search:str) -> str:
        """This API searches for a point of sale in the database.
        Args :
            search : str, search query
        Returns :
            str, JSON response"""
        try : 
            searchResult = searchEngine.searchPointDeVente(search, self.db)
            if searchResult == None : return None
            searchResult = utils.formatPointDeVenteToJson(searchResult)
            return self.makeResponse(content=searchResult)
        except Exception as e:
            print("\033[31mErreur lors de la recherche : ",e, e.__traceback__.tb_lineno, "\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue : "+ str(e))

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def searchEditeur(self, search:str) -> str:
        """This API searches for an editor in the database.
        Args :
            search : str, search query
        Returns :
            str, JSON response"""
        try : 
            searchResult = searchEngine.searchEditeur(search, self.db)
            if searchResult == None : return None
            searchResult = utils.formatEditeurToJson(searchResult)
            return self.makeResponse(content=searchResult)
        except Exception as e:
            print("\033[31mErreur lors de la recherche : ",e, e.__traceback__.tb_lineno, "\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue : "+ str(e))

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getLivre(self, isbn:str) -> str:
        """This API searches for a book in the database.
        Args :
            isbn : str, ISBN of the book
        Returns :
            str, JSON response"""
        try : 
            self.db.mkRequest("selectLivreByISBN",False, isbn)
            livre = self.db.cursor.fetchall()
            if livre is not None:
                livre = utils.formatLivreToJson(livre, self.db)
                return self.makeResponse(content=livre)
            else:
                return self.makeResponse(is_error=True, error_message="Livre introuvable")
        except Exception as e:
            print("\033[31mErreur lors de la recherche : ",e, e.__traceback__.tb_lineno,livre, "\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue")

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def checkLogin(self, email:str, password:str) -> str:
        """This API checks if the login is correct.
        Args :
            email : str, email of the user
            password : str, password of the user
        Returns :
            str, JSON response"""
        try : 
            self.db.mkRequest("selectUserByEmail", False, email)
            user = self.db.cursor.fetchall()
            if user is not None and user != () and user != []:
                if user[0][1] == password:
                    return self.makeResponse(content="success")
                else:
                    return self.makeResponse(is_error=True, error_message="Mot de passe incorrect")
            else:
                return self.makeResponse(is_error=True, error_message="Utilisateur introuvable")
        except Exception as e:
            print("\033[31mErreur lors de la tentative de conneion : ",e, e.__traceback__.tb_lineno, user, "\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez réessayer ultérieurement")

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def isAdmin(self, email:str, password:str) -> str:
        """This API checks if the user is an admin.
        Args :
            email : str, email of the user
            password : str, password of the user
        Returns :
            str, JSON response"""
        try : 
            self.db.mkRequest("selectUserByEmail", False, email)
            user = self.db.cursor.fetchall()
            if user is not None and user != () and user != []:
                if user[0][1] == password:
                    if user[0][2] == "admin":
                        return self.makeResponse(content="success")
                    else:
                        return self.makeResponse(is_error=True, error_message="Vous n'êtes pas administrateur")
                else:
                    return self.makeResponse(is_error=True, error_message="Mot de passe incorrect")
            else:
                return self.makeResponse(is_error=True, error_message="Utilisateur introuvable")
        except Exception as e:
            print("\033[31mErreur lors de la tentative de conneion : ",e, e.__traceback__.tb_lineno, user, "\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez réessayer ultérieurement")

    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getUserInfo(self, email:str, password:str) -> str:
        """This API gets the user information.
        Args :
            email : str, email of the user
            password : str, password of the user
        Returns :
            str, JSON response"""
        try : 
            self.db.mkRequest("selectUserByEmail", False, email)
            user = self.db.cursor.fetchall()
            if user is not None and user != () and user != []:
                if user[0][1] == password :
                    user = utils.formatUserToJson(user)
                    return self.makeResponse(content=user)
                else:
                    return self.makeResponse(is_error=True, error_message="Mot de passe incorrect")
            else:
                return self.makeResponse(is_error=True, error_message="Utilisateur introuvable")
        except Exception as e:
            print("\033[31mErreur lors de la tentative de conneion : ",e, e.__traceback__.tb_lineno, user, "\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez réessayer ultérieurement")
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def deleteLivre(self, email:str, password:str, isbn:str) -> str:
        """This API deletes a book from the database.
        Args :
            email : str, email of the user
            password : str, password of the user
            isbn : str, ISBN of the book
        Returns :
            str, JSON response"""
        try : 
            self.db.mkRequest("selectUserByEmail", False, email)
            user = self.db.cursor.fetchall()
            if user is not None and user != () and user != []:
                if user[0][1] == password:
                    if user[0][2] == "admin":
                        self.db.mkRequest("deleteNoteByISBN", False, isbn)
                        self.db.mkRequest("deleteEmpruntByISBN", False, isbn)
                        self.db.mkRequest("deleteLivre", False, isbn)
                        self.db.db.commit()
                        try : 
                            os.remove(f"www/img/livres/{isbn}.jpg")
                        except Exception as e:
                            print("\033[31mErreur lors de la suppression de l'image : ",e, e.__traceback__.tb_lineno, "\033[0m")
                        return self.makeResponse(content="success")
                    else:
                        return self.makeResponse(is_error=True, error_message="Vous n'êtes pas administrateur")
                else:
                    return self.makeResponse(is_error=True, error_message="Mot de passe incorrect")
            else:
                return self.makeResponse(is_error=True, error_message="Utilisateur introuvable")
        except Exception as e:
            print("\033[31mErreur lors de la suppression du livre : ",e, e.__traceback__.tb_lineno, "\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez réessayer ultérieurement")
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def deleteAuteur(self, email:str, password:str, id:int) -> str:
        """This API deletes an author from the database.
        Args :
            email : str, email of the user
            password : str, password of the user
            id : int, ID of the author
        Returns :
            str, JSON response"""
        try : 
            self.db.mkRequest("selectUserByEmail", False, email)
            user = self.db.cursor.fetchall()
            if user is not None and user != () and user != []:
                if user[0][1] == password:
                    if user[0][2] == "admin":
                        self.db.mkRequest("deleteEmpruntByAuteurID", False, id)
                        self.db.mkRequest("deleteLivreByAuteur", False, id)#delete all books from this author first
                        self.db.mkRequest("deleteAuteur", False, id)
                        self.db.db.commit()
                        self.cleanImageLivres()
                        return self.makeResponse(content="success")
                    else:
                        return self.makeResponse(is_error=True, error_message="Vous n'êtes pas administrateur")
                else:
                    return self.makeResponse(is_error=True, error_message="Mot de passe incorrect")
            else:
                return self.makeResponse(is_error=True, error_message="Utilisateur introuvable")
        except Exception as e:
            print("\033[31mErreur lors de la suppression de l'auteur : ",e, e.__traceback__.tb_lineno, "\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez réessayer ultérieurement")
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getPointDeVenteReplacement(self, replacementName):
        """This API gets the replacement point of sale.
        Args :
            replacementName : str, name of the replacement point of sale
        Returns :
            str, JSON response"""
        try : 
            replacementPointDeVente = searchEngine.searchPointDeVente(replacementName, self.db, onlyOne=True)
            if replacementPointDeVente == None: 
                return self.makeResponse(is_error=True, error_message="Point de vente de remplacement introuvable")
            return self.makeResponse(content=replacementPointDeVente[0][0])
        except Exception as e:
            print("\033[31mErreur lors de la recherche du point de vente de remplacement : ",e, e.__traceback__.tb_lineno, "\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez réessayer ultérieurement")
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def deletePointDeVente(self, email:str, password:str, adresse:str, adresseReplacement: str) -> str:
        """This API deletes a point of sale from the database.
        Args :
            email : str, email of the user
            password : str, password of the user
            adresse : str, address of the point of sale
            adresseReplacement : str, address of the replacement point of sale
        Returns :
            str, JSON response"""
        try : 
            self.db.mkRequest("selectUserByEmail", False, email)
            user = self.db.cursor.fetchall()
            if user is not None and user != () and user != []:
                if user[0][1] == password:
                    if user[0][2] == "admin":
                        self.db.mkRequest("updateLivrePointDeVente", False, operationOnDataBase.convertPointDeVenteToAcceptablePointDeVente(adresseReplacement,self.db), operationOnDataBase.convertPointDeVenteToAcceptablePointDeVente(adresse,self.db))
                        self.db.mkRequest("deletePointDeVente", False, operationOnDataBase.convertPointDeVenteToAcceptablePointDeVente(adresse,self.db))
                        self.db.db.commit()
                        return self.makeResponse(content="success")
                    else:
                        return self.makeResponse(is_error=True, error_message="Vous n'êtes pas administrateur")
                else:
                    return self.makeResponse(is_error=True, error_message="Mot de passe incorrect")
            else:
                return self.makeResponse(is_error=True, error_message="Utilisateur introuvable")
        except Exception as e:
            print("\033[31mErreur lors de la suppression du point de vente : ",e, e.__traceback__.tb_lineno, "\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez réessayer ultérieurement")
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def deleteEditeur(self, email:str, password:str, nom:str) -> str:
        """This API deletes an editor from the database.
        Args :
            email : str, email of the user
            password : str, password of the user
            nom : str, name of the editor
        Returns :
            str, JSON response"""
        try : 
            self.db.mkRequest("selectUserByEmail", False, email)
            user = self.db.cursor.fetchall()
            if user is not None and user != () and user != []:
                if user[0][1] == password:
                    if user[0][2] == "admin":
                        self.db.mkRequest("deleteLivreByEditeur", False, nom)#delete all books from this editor first
                        self.db.mkRequest("deleteEditeur", False, nom)
                        self.db.db.commit()
                        self.cleanImageLivres()
                        return self.makeResponse(content="success")
                    else:
                        return self.makeResponse(is_error=True, error_message="Vous n'êtes pas administrateur")
                else:
                    return self.makeResponse(is_error=True, error_message="Mot de passe incorrect")
            else:
                return self.makeResponse(is_error=True, error_message="Utilisateur introuvable")
        except Exception as e:
            print("\033[31mErreur lors de la suppression de l'éditeur : ",e, e.__traceback__.tb_lineno, "\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez réessayer ultérieurement")
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def deleteUser(self, email:str, password:str, emailToDelete:str) -> str:
        """This API deletes a user from the database.
        Args :
            email : str, email of the user
            password : str, password of the user
            emailToDelete : str, email of the user to delete
        Returns :
            str, JSON response"""
        try : 
            self.db.mkRequest("selectUserByEmail", False, email)
            user = self.db.cursor.fetchall()
            if user is not None and user != () and user != []:
                if user[0][1] == password:
                    if user[0][2] == "admin":
                        #check if the user to delete is admin, if so, refuse
                        self.db.mkRequest("selectUserByEmail", False, emailToDelete)
                        userToDelete = self.db.cursor.fetchall()
                        if userToDelete is not None and userToDelete != () and userToDelete != []:
                            if userToDelete[0][2] == "admin":
                                return self.makeResponse(is_error=True, error_message="Vous ne pouvez pas supprimer un administrateur")
                        self.db.mkRequest("deleteEmpruntByUser", False, emailToDelete)
                        self.db.mkRequest("deleteUser", False, emailToDelete)
                        self.db.db.commit()
                        return self.makeResponse(content="success")
                    else:
                        return self.makeResponse(is_error=True, error_message="Vous n'êtes pas administrateur")
                else:
                    return self.makeResponse(is_error=True, error_message="Mot de passe incorrect")
            else:
                return self.makeResponse(is_error=True, error_message="Utilisateur introuvable")
        except Exception as e:
            print("\033[31mErreur lors de la suppression de l'utilisateur : ",e, e.__traceback__.tb_lineno, "\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez réessayer ultérieurement")

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def deleteEmprunt(self, email:str, password:str, id:int) -> str:
        """This API deletes a reservation from the database.
        Args :
            email : str, email of the user
            password : str, password of the user
            id : int, ID of the reservation
        Returns :
            str, JSON response"""
        try : 
            self.db.mkRequest("selectUserByEmail", False, email)
            user = self.db.cursor.fetchall()
            if user is not None and user != () and user != []:
                if user[0][1] == password:
                    self.db.mkRequest("deleteEmprunt", False, id)
                    self.db.db.commit()
                    return self.makeResponse(content="success")
                else:
                    return self.makeResponse(is_error=True, error_message="Mot de passe incorrect")
            else:
                return self.makeResponse(is_error=True, error_message="Utilisateur introuvable")
        except Exception as e:
            print("\033[31mErreur lors de la suppression de l'emprunt : ",e, e.__traceback__.tb_lineno, "\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez réessayer ultérieurement")
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getEmprunt(self, email:str, password:str)->str:
        """This API gets the reservations of a user.
        Args :
            email : str, email of the user
            password : str, password of the user
        Returns :
            str, JSON response"""
        try : 
            self.db.mkRequest("selectUserByEmail", True, email)
            user = self.db.cursor.fetchall()
            if user is not None and user != () and user != []:
                if user[0][1] == password:
                    self.db.mkRequest("selectEmpruntByUser", True, email)
                    emprunts = self.db.cursor.fetchall()
                    if emprunts is not None and emprunts != () and emprunts != []:
                        emprunts = utils.formatEmpruntsToJson(emprunts)
                        return self.makeResponse(content=emprunts)
                    else:
                        return self.makeResponse(is_error=True, error_message="Aucun emprunt trouvé")
                else:
                    return self.makeResponse(is_error=True, error_message="Mot de passe incorrect")
        except Exception as e:
            print("\033[31mErreur lors de la récupération des réservations : ",e, e.__traceback__.tb_lineno, emprunts, "\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez réessayer ultérieurement")
    
    @cherrypy.expose
    def index(self) -> str :
        """This function expose the index page to internet."""
        return open('www/html/index.html', encoding="utf-8")

    @cherrypy.expose
    def search(self, search:str, type:str="livre", sort="default", auteur="all") -> str :
        """This function expose the search page to internet."""
        return open('www/html/search.html', encoding="utf-8")

    @cherrypy.expose
    def livre(self, isbn) -> str :
        return open('www/html/livre.html', encoding="utf-8")

    @cherrypy.expose
    def login(self) -> str :
        """This function expose the login page to internet."""
        return open('www/html/login.html', encoding="utf-8")

    @cherrypy.expose
    def account(self) -> str :
        """This function expose the account page to internet."""
        return open('www/html/account.html', encoding="utf-8")
    
    @cherrypy.expose
    def config(self) -> str :
        """This function expose the config page to internet."""
        return open('www/html/config.html', encoding="utf-8")
    
    @cherrypy.expose
    def addLivre(self) -> str :
        """This function expose the add book page to internet."""
        return open('www/html/addLivre.html', encoding="utf-8")
    
    @cherrypy.expose
    def addAuteur(self) -> str :
        """This function expose the add author page to internet."""
        return open('www/html/addAuteur.html', encoding="utf-8")

    @cherrypy.expose
    def addPointDeVente(self) -> str :
        """This function expose the add point of sale page to internet."""
        return open('www/html/addPointDeVente.html', encoding="utf-8")
    
    @cherrypy.expose
    def addEditeur(self) -> str :
        """This function expose the add editor page to internet."""
        return open('www/html/addEditeur.html', encoding="utf-8")
    
    @cherrypy.expose
    def createAccount(self) -> str :
        """This function expose the create account page to internet."""
        return open('www/html/createAccount.html', encoding="utf-8")

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def updateBestLivres(self) -> str :
        """This function updates the trending books of the home page."""
        if self.timeToRefresh != 0:
            self.timeToRefresh -= 1
            return
        self.timeToRefresh = 5
        try :
            self.db.mkRequest("selectISBNAllLivres")
            selected = []
            isbns = list(self.db.cursor.fetchall())
            for i in range(9):
                choice = random.choice(isbns)
                selected.append(choice[0])
                if os.path.exists(f"www/img/bestLivres/{i+1}.jpg"):
                    os.remove(f"www/img/bestLivres/{i+1}.jpg")
                isbns.remove(choice)
            for i in range(len(selected)):
                shutil.copy(f"www/img/livres/{selected[i]}.jpg", f"www/img/bestLivres/{i+1}.jpg")
            return self.makeResponse(content='ok')
        except Exception as e:
            print("\033[31mErreur lors de la mise à jour des livres de la page d'accueil", e, e.__traceback__.tb_lineno, "\033[0m")
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getAllLivre(self) -> str:
        """This API gets all the books in the database."""
        try : 
            self.db.mkRequest("selectAllLivre")
            livres = self.db.cursor.fetchall()
            if livres is not None and livres != () and livres != []:
                livres = utils.formatLivreToJson(livres, self.db)
                return self.makeResponse(content=livres)
            else:
                return self.makeResponse(is_error=True, error_message="Aucun livre trouvé")
        except Exception as e:
            print("\033[31mErreur lors de la récupération des livres : ",e, e.__traceback__.tb_lineno, "\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez réessayer ultérieurement")
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getAllAuteur(self) -> str:
        """This API gets all the authors in the database."""
        try : 
            self.db.mkRequest("selectAllAuteur")
            auteurs = self.db.cursor.fetchall()
            if auteurs is not None and auteurs != () and auteurs != []:
                auteurs = utils.formatAuteurToJson(auteurs)
                return self.makeResponse(content=auteurs)
            else:
                return self.makeResponse(is_error=True, error_message="Aucun auteur trouvé")
        except Exception as e:
            print("\033[31mErreur lors de la récupération des auteurs : ",e, e.__traceback__.tb_lineno, "\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez réessayer ultérieurement")
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getAllNomAuteur(self) -> str:
        """This API gets all the authors in the database."""
        try : 
            self.db.mkRequest("selectAllNomAuteur")
            auteurs = self.db.cursor.fetchall()
            if auteurs is not None and auteurs != () and auteurs != []:
                auteurs = utils.formatAuteurNomToJson(auteurs)
                return self.makeResponse(content=auteurs)
            else:
                return None
        except Exception as e:
            print("\033[31mErreur lors de la récupération des auteurs : ",e, e.__traceback__.tb_lineno, "\033[0m")
            return None
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getAllPointDeVentes(self)->str:
        """This API gets all the points of sale in the database."""
        try : 
            self.db.mkRequest("selectAllPointDeVente")
            adresses = self.db.cursor.fetchall()
            if adresses is not None and adresses != () and adresses != []:
                adresses = utils.formatPointDeVenteToJson(adresses)
                return self.makeResponse(content=adresses)
            else:
                return self.makeResponse(is_error=True, error_message="Aucun point de vente trouvé")
        except Exception as e:
            print("\033[31mErreur lors de la récupération des points de vente : ",e, e.__traceback__.tb_lineno, "\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez réessayer ultérieurement")
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getAllEditeurs(self)->str:
        """This API gets all the editors in the database."""
        try : 
            self.db.mkRequest("selectAllEditeur")
            editeurs = self.db.cursor.fetchall()
            if editeurs is not None and editeurs != () and editeurs != []:
                editeurs = utils.formatEditeurToJson(editeurs)
                return self.makeResponse(content=editeurs)
            else:
                return self.makeResponse(is_error=True, error_message="Aucun éditeur trouvé")
        except Exception as e:
            print("\033[31mErreur lors de la récupération des éditeurs : ",e, e.__traceback__.tb_lineno, "\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez réessayer ultérieurement")

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getAllEmprunts(self, email:str, password:str) -> str:
        """This API gets all the reservations in the database. Only the admin can use this API.
        Args :
            email : str, email of the user
            password : str, password of the user
        Returns :
            str, JSON response"""
        try : 
            self.db.mkRequest("selectUserByEmail", True, email)
            user = self.db.cursor.fetchall()
            if user is not None and user != () and user != []:
                if user[0][1] == password:
                    if user[0][2] == "admin":
                        self.db.mkRequest("selectAllEmprunt")
                        emprunts = self.db.cursor.fetchall()
                        if emprunts is not None and emprunts != () and emprunts != []:
                            emprunts = utils.formatEmpruntsToJson(emprunts)
                            return self.makeResponse(content=emprunts)
                        else:
                            return self.makeResponse(is_error=True, error_message="Aucun emprunt trouvé")
                    else:
                        return self.makeResponse(is_error=True, error_message="Vous n'êtes pas administrateur")
                else:
                    return self.makeResponse(is_error=True, error_message="Mot de passe incorrect")
        except Exception as e:
            print("\033[31mErreur lors de la récupération des réservations : ",e, e.__traceback__.tb_lineno, "\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez réessayer ultérieurement")
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getAllUtilisateurs(self, email:str, password:str) -> str:
        """This API gets all the users in the database. Only the admin can use this API.
        Args :
            email : str, email of the user
            password : str, password of the user
        Returns :
            str, JSON response"""
        try : 
            self.db.mkRequest("selectUserByEmail", False, email)
            user = self.db.cursor.fetchall()
            if user is not None and user != () and user != []:
                if user[0][1] == password:
                    if user[0][2] == "admin":
                        self.db.mkRequest("selectAllUser")
                        users = self.db.cursor.fetchall()
                        if users is not None and users != () and users != []:
                            users = utils.formatUserToJson(users)
                            return self.makeResponse(content=users)
                        else:
                            return self.makeResponse(is_error=True, error_message="Aucun utilisateur trouvé")
                    else:
                        return self.makeResponse(is_error=True, error_message="Vous n'êtes pas administrateur")
                else:
                    return self.makeResponse(is_error=True, error_message="Mot de passe incorrect")
            else:
                return self.makeResponse(is_error=True, error_message="Utilisateur introuvable")
        except Exception as e:
            print("\033[31mErreur lors de la récupération des utilisateurs : ",e, e.__traceback__.tb_lineno, "\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez réessayer ultérieurement")
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def reserveLivre(self, email:str, password:str, isbn:str) -> str:
        """This API reserves a book.
        Args :
            email : str, email of the user
            password : str, password of the user
            isbn : str, ISBN of the book
        Returns :
            str, JSON response"""
        try : 
            self.db.mkRequest("selectUserByEmail", True, email)
            user = self.db.cursor.fetchall()
            if user is not None and user != () and user != []:
                if user[0][1] == password:
                    self.db.mkRequest("selectLivreByISBN", False, isbn)
                    livre = self.db.cursor.fetchall()
                    if livre is not None and livre != () and livre != []:
                        self.db.mkRequest("selectEmpruntByUser", True, email)
                        emprunts = self.db.cursor.fetchall()
                        if emprunts is not None and emprunts != () and emprunts != []:
                            for emprunt in emprunts:
                                if emprunt[0] == isbn:
                                    return self.makeResponse(is_error=True, error_message="Ce livre est déjà réservé")
                        self.db.mkRequest("insertEmprunt", False, isbn,email)
                        self.db.db.commit()
                        return self.makeResponse(content="success")
                    else:
                        return self.makeResponse(is_error=True, error_message="Livre introuvable")
                else:
                    return self.makeResponse(is_error=True, error_message="Mot de passe incorrect")
            else:
                return self.makeResponse(is_error=True, error_message="Utilisateur introuvable")
        except Exception as e:
            print("\033[31mErreur lors de la réservation : ",e, e.__traceback__.tb_lineno, "\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez réessayer ultérieurement")
    
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def updateLivres(self):
        """This API updates the books in the database. Takes a JSON object as input. Only the admin can use this API."""
        try:
            data = cherrypy.request.json
            email = data.get("email")
            password = data.get("password")
            if not email or not password:
                return self.makeResponse(is_error=True, error_message="Email et mot de passe requis")
            self.db.mkRequest("selectUserByEmail", False, email)
            user = self.db.cursor.fetchone()
            if user and user[1] == password and user[2] == "admin":
                livres = data.get("livres", [])
                if not livres:
                    return self.makeResponse(is_error=True, error_message="Aucun livre à mettre à jour")
                for livre in livres:
                    try:
                        self.db.mkRequest("updateLivre", False,livre["titre"], livre["auteur"], livre["description"], livre["dateDeParution"],livre["status"], livre["genre"], livre["format"], livre["prix"], livre["pointDeVente"], livre["editeur"], livre["isbn"])
                        self.db.db.commit()
                    except Exception as e:
                        print(f"\033[31mErreur lors de la mise à jour du livre ISBN {livre['isbn']} : {e}\033[0m")
                        return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez vérifier les données envoyées")
                return self.makeResponse(content="success")
            else:
                return self.makeResponse(is_error=True, error_message="Accès refusé ou mot de passe incorrect")
        except Exception as e:
            print(f"\033[31mErreur lors de la mise à jour des livres : {e}, ligne {e.__traceback__.tb_lineno}\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez vérifier les données envoyées")
    
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def updateAuteurs(self):
        """This API updates the authors in the database. Takes a JSON object as input with in content : email, password, auteurs. Only the admin can use this API."""
        try:
            data = cherrypy.request.json
            email = data.get("email")
            password = data.get("password")
            if not email or not password:
                return self.makeResponse(is_error=True, error_message="Email et mot de passe requis")
            self.db.mkRequest("selectUserByEmail", False, email)
            user = self.db.cursor.fetchone()
            if user and user[1] == password and user[2] == "admin":
                auteurs = data.get("auteurs", [])
                if not auteurs:
                    return self.makeResponse(is_error=True, error_message="Aucun auteur à mettre à jour")
                for auteur in auteurs:
                    try:
                        date_de_naissance = auteur.get("dateDeNaissance")
                        date_de_deces = auteur.get("dateDeDeces")
                        if date_de_naissance:
                            day, month, year = date_de_naissance.split("/")
                            date_de_naissance = f"{year}-{month}-{day}"
                        if date_de_deces:
                            day, month, year = date_de_deces.split("/")
                            date_de_deces = f"{year}-{month}-{day}"
                        self.db.mkRequest("updateAuteur", False,auteur["nom"], auteur["prénom"], auteur["biographie"],date_de_naissance, date_de_deces, auteur["alias"],auteur["id"])
                        self.db.db.commit()
                    except Exception as e:
                        print(f"\033[31mErreur lors de la mise à jour de l'auteur ID {auteur['id']} : {e}\033[0m")
                        return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez vérifier les données envoyées")
                return self.makeResponse(content="success")
            else:
                return self.makeResponse(is_error=True, error_message="Accès refusé ou mot de passe incorrect")
        except Exception as e:
            print(f"\033[31mErreur lors de la mise à jour des auteurs : {e}, ligne {e.__traceback__.tb_lineno}\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez vérifier les données envoyées")
    
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def updatePointDeVentes(self):
        """This API updates the points of sale in the database. Takes a JSON object as input with email, password, pointDeVentes. Only the admin can use this API."""
        try:
            data = cherrypy.request.json
            email = data.get("email")
            password = data.get("password")
            if not email or not password:
                return self.makeResponse(is_error=True, error_message="Email et mot de passe requis")
            self.db.mkRequest("selectUserByEmail", False, email)
            user = self.db.cursor.fetchone()
            if user and user[1] == password and user[2] == "admin":
                pointDeVentes = data.get("pointDeVentes", [])
                if not pointDeVentes:
                    return self.makeResponse(is_error=True, error_message="Aucun point de vente à mettre à jour")
                for pointDeVente in pointDeVentes:
                    try:
                        tel = pointDeVente.get("tel") or None
                        self.db.mkRequest("updatePointDeVente", False,pointDeVente["nom"], pointDeVente["url"], tel, pointDeVente["adresse"])
                        self.db.db.commit()
                    except Exception as e:
                        print(f"\033[31mErreur lors de la mise à jour du point de vente {pointDeVente['nom']} : {e}\033[0m")
                        return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez vérifier les données envoyées")
                return self.makeResponse(content="success")
            else:
                return self.makeResponse(is_error=True, error_message="Accès refusé ou mot de passe incorrect")
        except Exception as e:
            print(f"\033[31mErreur lors de la mise à jour des points de vente : {e}, ligne {e.__traceback__.tb_lineno}\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez vérifier les données envoyées")

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def updateEditeurs(self):
        """This API updates the publishers in the database. Takes a JSON object as input with email, password, editeurs. Only the admin can use this API."""
        try:
            data = cherrypy.request.json
            email = data.get("email")
            password = data.get("password")
            if not email or not password:
                return self.makeResponse(is_error=True, error_message="Email et mot de passe requis")
            self.db.mkRequest("selectUserByEmail", False, email)
            user = self.db.cursor.fetchone()
            if user and user[1] == password and user[2] == "admin":
                editeurs = data.get("editeurs", [])
                if not editeurs:
                    return self.makeResponse(is_error=True, error_message="Aucun éditeur à mettre à jour")
                for editeur in editeurs:
                    try:
                        self.db.mkRequest("updateEditeur", False,editeur["adresse"], editeur["nom"])
                        self.db.db.commit()
                    except Exception as e:
                        print(f"\033[31mErreur lors de la mise à jour de l'éditeur {editeur['nom']} : {e}\033[0m")
                        return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez vérifier les données envoyées")
                return self.makeResponse(content="success")
            else:
                return self.makeResponse(is_error=True, error_message="Accès refusé ou mot de passe incorrect")
        except Exception as e:
            print(f"\033[31mErreur lors de la mise à jour des éditeurs : {e}, ligne {e.__traceback__.tb_lineno}\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez vérifier les données envoyées")
        
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def updateUtilisateurs(self):
        """This API updates the users in the database. Takes a JSON object as input with email, password, users. Only the admin can use this API."""
        try:
            data = cherrypy.request.json
            email = data.get("email")
            password = data.get("password")
            if not email or not password:
                return self.makeResponse(is_error=True, error_message="Email et mot de passe requis")
            self.db.mkRequest("selectUserByEmail", False, email)
            user = self.db.cursor.fetchone()
            if user and user[1] == password and user[2] == "admin":
                users = data.get("users", [])
                if not users:
                    return self.makeResponse(is_error=True, error_message="Aucun utilisateur à mettre à jour")
                for user_data in users:
                    try:
                        self.db.mkRequest("updateUtilisateur", False,user_data["mdp"], user_data["grade"], user_data["nom"],user_data["prénom"], user_data["adresse"], user_data["tel"], user_data["email"])
                        self.db.db.commit()
                    except Exception as e:
                        print(f"\033[31mErreur lors de la mise à jour de l'utilisateur {user_data['email']} : {e}\033[0m")
                        return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez vérifier les données envoyées")
                return self.makeResponse(content="success")
            else:
                return self.makeResponse(is_error=True, error_message="Accès refusé ou mot de passe incorrect")
        except Exception as e:
            print(f"\033[31mErreur lors de la mise à jour des utilisateurs : {e}, ligne {e.__traceback__.tb_lineno}\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez vérifier les données envoyées")
        
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def updateEmprunts(self):
        """This API updates the borrowings in the database. Takes a JSON object as input with email, password, emprunts. Only the admin can use this API."""
        try:
            data = cherrypy.request.json
            email = data.get("email")
            password = data.get("password")
            if not email or not password:
                return self.makeResponse(is_error=True, error_message="Email et mot de passe requis")
            self.db.mkRequest("selectUserByEmail", False, email)
            user = self.db.cursor.fetchone()
            if user and user[1] == password and user[2] == "admin":
                emprunts = data.get("emprunts", [])
                if not emprunts:
                    return self.makeResponse(is_error=True, error_message="Aucun emprunt à mettre à jour")
                for emprunt in emprunts:
                    try:
                        date_parts = emprunt["date"].split("/")
                        formatted_date = f"{date_parts[2]}-{date_parts[1]}-{date_parts[0]}"
                        self.db.mkRequest("updateEmprunt", False,emprunt["livre"], formatted_date, emprunt["utilisateur"], emprunt["id"])
                        self.db.db.commit()
                    except Exception as e:
                        print(f"\033[31mErreur lors de la mise à jour de l'emprunt {emprunt['id']} : {e}\033[0m")
                        continue
                return self.makeResponse(content="success")
            else:
                return self.makeResponse(is_error=True, error_message="Accès refusé ou mot de passe incorrect")
        except Exception as e:
            print(f"\033[31mErreur lors de la mise à jour des emprunts : {e}, ligne {e.__traceback__.tb_lineno}\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez vérifier les données envoyées")
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def newLivre(self, **params):
        """This API adds a new book to the database. Only the admin can use this API."""
        try:
            email = params.get("email")
            password = params.get("password")
            if not email or not password:
                return self.makeResponse(is_error=True, error_message="Email et mot de passe requis")
            self.db.mkRequest("selectUserByEmail", False, email)
            user = self.db.cursor.fetchone()
            if user and user[1] == password:
                if user[2] == "admin":
                    isbn = params.get("isbn")
                    titre = params.get("titre")
                    auteur = params.get("auteur")
                    description = params.get("description")
                    dateDeParution = params.get("dateParution")
                    note = params.get("note")
                    statut = params.get("statut")
                    genre = params.get("genre")
                    format = params.get("format")
                    prix = params.get("prix")
                    pointDeVente = params.get("pointDeVente", "").strip()  # Remove leading/trailing whitespace
                    editeur = params.get("editeur")
                    image = params.get("image")
                    # Check if all required fields are provided
                    if all([isbn, titre, auteur, description, dateDeParution, statut, genre, format, prix, pointDeVente, editeur]):
                        self.db.mkRequest("selectLivreByISBN", False, isbn)
                        checkISBN = self.db.cursor.fetchone()
                        if checkISBN:
                            return self.makeResponse(is_error=True, error_message="Un livre avec cet ISBN existe déjà")
                        pointDeVente = operationOnDataBase.convertPointDeVenteToAcceptablePointDeVente(pointDeVente, self.db)
                        self.db.mkRequest("insertLivre", False, isbn, titre, auteur, description, note, dateDeParution, statut, genre, format, prix, pointDeVente, editeur)
                        self.db.db.commit()
                        try:
                            upload_filename = f"{isbn}.jpg"
                            upload_file_path = os.path.join("./www/img/livres", upload_filename)
                            # Check if file exists to avoid overwriting
                            if os.path.exists(upload_file_path):
                                return self.makeResponse(is_error=True, error_message="Une image avec ce nom existe déjà")
                            with open(upload_file_path, 'wb') as out:
                                while True:
                                    data = image.file.read(8192)
                                    if not data:
                                        break
                                    out.write(data)
                        except Exception as e:
                            print(f"\033[31mErreur lors de l'ajout de l'image : {e}, ligne {e.__traceback__.tb_lineno}\033[0m")
                        return self.makeResponse(content="success")
                    else:
                        return self.makeResponse(is_error=True, error_message="Les données envoyées sont incorrectes")
                else:
                    return self.makeResponse(is_error=True, error_message="Vous n'êtes pas administrateur")
            else:
                return self.makeResponse(is_error=True, error_message="Mot de passe incorrect")
        except Exception as e:
            print(f"Erreur : {e}")
            return self.makeResponse(is_error=True, error_message=str(e))
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def newAuteur(self, **params):
        """This API adds a new author to the database. Only the admin can use this API."""
        try:
            email = params.get("email")
            password = params.get("password")
            if not email or not password:
                return self.makeResponse(is_error=True, error_message="Email et mot de passe sont requis")
            self.db.mkRequest("selectUserByEmail", False, email)
            user = self.db.cursor.fetchall()
            if not user or user[0][1] != password:
                return self.makeResponse(is_error=True, error_message="Email ou mot de passe incorrect")
            if user[0][2] != "admin":
                return self.makeResponse(is_error=True, error_message="Vous n'êtes pas administrateur")
            nom = params.get("nom")
            prenom = params.get("prenom")
            alias = params.get("alias") or None
            biographie = params.get("biographie")
            dateDeNaissance = params.get("dateNaissance")
            dateDeDeces = params.get("dateDeces") or None
            if all([nom, prenom, biographie, dateDeNaissance]):
                self.db.mkRequest("insertAuteur", False, nom, prenom, biographie, dateDeNaissance, dateDeDeces, alias)
                self.db.db.commit()
                return self.makeResponse(content="success")
            return self.makeResponse(is_error=True, error_message="Les données envoyées sont incorrectes")
        except Exception as e:
            print(f"Erreur : {e}")
            return self.makeResponse(is_error=True, error_message="Une erreur est survenue")
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def newPointDeVente(self, **params):
        try:
            email = params.get("email")
            password = params.get("password")
            if not email or not password:
                return self.makeResponse(is_error=True, error_message="Email et mot de passe sont requis")
            self.db.mkRequest("selectUserByEmail", False, email)
            user = self.db.cursor.fetchall()
            if not user or user[0][1] != password:
                return self.makeResponse(is_error=True, error_message="Email ou mot de passe incorrect")
            if user[0][2] != "admin":
                return self.makeResponse(is_error=True, error_message="Vous n'êtes pas administrateur")
            nom = params.get("nom")
            adresse = params.get("adresse")
            url = params.get("url")
            tel = params.get("tel")
            if all([nom, adresse]):
                self.db.mkRequest("insertPointDeVente", False, adresse, nom, url, tel)
                self.db.db.commit()
                return self.makeResponse(content="success")
            return self.makeResponse(is_error=True, error_message="Les données envoyées sont incorrectes")
        except Exception as e:
            cherrypy.log(f"Erreur : {e}", traceback=True)
            return self.makeResponse(is_error=True, error_message="Une erreur est survenue")
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def newEditeur(self, **params):
        try:
            email = params.get("email")
            password = params.get("password")
            if not email or not password:
                return self.makeResponse(is_error=True, error_message="Email et mot de passe sont requis")
            self.db.mkRequest("selectUserByEmail", False, email)
            user = self.db.cursor.fetchall()
            if not user or user[0][1] != password:
                return self.makeResponse(is_error=True, error_message="Email ou mot de passe incorrect")
            if user[0][2] != "admin":
                return self.makeResponse(is_error=True, error_message="Vous n'êtes pas administrateur")
            nom = params.get("nom")
            adresse = params.get("adresse")
            if nom:
                self.db.mkRequest("insertEditeur", False, nom, adresse)
                self.db.db.commit()
                return self.makeResponse(content="success")
            return self.makeResponse(is_error=True, error_message="Les données envoyées sont incorrectes")
        except Exception as e:
            cherrypy.log(f"Erreur : {e}", traceback=True)
            return self.makeResponse(is_error=True, error_message="Une erreur est survenue")

        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def newUser(self, **params):
        try:
            email = params.get("email")
            mdp = params.get("mdp")
            nom = params.get("nom")
            prenom = params.get("prenom")
            adresse = params.get("adresse")
            tel = params.get("tel")
            if all([email, mdp, nom, prenom, adresse, tel]):
                self.db.mkRequest("insertUtilisateur", False, email, mdp, "user", nom, prenom, adresse, tel)
                self.db.db.commit()
                return self.makeResponse(content="success")
            return self.makeResponse(is_error=True, error_message="Les données envoyées sont incorrectes")
        except Exception as e:
            cherrypy.log(f"Erreur : {e}", traceback=True)
            return self.makeResponse(is_error=True, error_message="Une erreur est survenue")
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def addNote(self, email:str, password:str, isbn:str, note:str) -> str:
        try : 
            self.db.mkRequest("selectUserByEmail", True, email)
            user = self.db.cursor.fetchall()
            if user is not None and user != () and user != []:
                if user[0][1] == password:
                    if isbn.isdigit() and float(note) >= 0 and float(note) <= 10:
                        self.db.mkRequest("selectLivreByISBN", False, isbn)
                        livre = self.db.cursor.fetchall()
                        if livre is not None and livre != () and livre != []:
                            self.db.mkRequest("selectNoteByUserAndLivre", False, email, isbn)
                            tmp = self.db.cursor.fetchall()
                            if tmp == ():
                                self.db.mkRequest("addNote", False, note, email, isbn)
                                self.db.db.commit()
                                return self.makeResponse(content="success")
                            else : 
                                self.db.mkRequest("updateNote", False, note, email, isbn)
                                return self.makeResponse(content="success")
                        else:
                            return self.makeResponse(is_error=True, error_message="Livre introuvable")
                    else :
                        return self.makeResponse(is_error=True, error_message="Les données envoyées sont incorrectes")
                else:
                    return self.makeResponse(is_error=True, error_message="Mot de passe incorrect")
            else:
                return self.makeResponse(is_error=True, error_message="Utilisateur introuvable")
        except Exception as e:
            print("\033[31mErreur lors de l'ajout de la note : ",e, e.__traceback__.tb_lineno, "\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez réessayer ultérieurement")
    
def jsonify_error(status, message, traceback, version):
    try :
        response = cherrypy.response
        response.headers['Content-Type'] = 'application/json'
        return json.dumps(
            {
                'status': 'error', 
                'http_status': status,
                'error_message': message
            }
        )
    except Exception as e:
        print("Erreur lors de la création de la réponse : ",e, e.__traceback__.tb_lineno, status, message)