import operationOnDataBase, database, utils, searchEngine
import cherrypy, os, json, shutil, random

class Server(object):
    def __init__(self, db:database.db, conf:dict):
        self.db = db
        self.conf = conf
        self.bestLivres = []
        self.timeToRefresh = 0

    def makeResponse(self, is_error=False, content=None, error_message=None):
        try : 
            response = cherrypy.response
            if not is_error:
                return {"status":"ok", "content":content}
            else:
                return {"status":"error", "message":error_message}
        except Exception as e:
            print("Erreur lors de la création de la réponse : ",e, e.__traceback__.tb_lineno, content, error_message)
    
    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def searchLivre(self, search:str, sort:str, auteur:str="Tous") -> str:
        sortList = ["sortByAlpha", "sortByNote", "sortByDate", "sortByPrix"]
        if sort not in sortList:
            sort = "sortByAlpha"
        try : 
            searchResult = searchEngine.searchLivre(search,self.db)
            if searchResult == None : return None
            searchResult= operationOnDataBase.sortLivre(searchResult,sort)
            if auteur != "Tous":
                searchResult = operationOnDataBase.filterLivreByAuteur(searchResult, auteur, self.db)
            searchResult = utils.formatLivreToJsonOrdered(searchResult, self.db)
           
            return self.makeResponse(content=searchResult)
        except Exception as e:
            print("\033[31mErreur lors de la recherche : ",e, e.__traceback__.tb_lineno, searchResult, "\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue : "+ str(e))

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def searchAuteur(self, search:str) -> str:
        try : 
            searchResult = searchEngine.searchAuteur(search, self.db)
            if searchResult == None : return None
            searchResult = utils.formatAuteurToJson(searchResult)
            return self.makeResponse(content=searchResult)
        except Exception as e:
            print("\033[31mErreur lors de la recherche : ",e, e.__traceback__.tb_lineno, "\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue : "+ str(e))

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def searchPointDeVente(self, search:str) -> str:
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
        try : 
            self.db.mkRequest("selectUserByEmail", False, email)
            user = self.db.cursor.fetchall()
            if user is not None and user != () and user != []:
                if user[0][1] == password:
                    if user[0][2] == "admin":
                        self.db.mkRequest("deleteEmpruntByISBN", False, isbn)
                        self.db.mkRequest("deleteLivre", False, isbn)
                        self.db.db.commit()
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
        try : 
            self.db.mkRequest("selectUserByEmail", False, email)
            user = self.db.cursor.fetchall()
            if user is not None and user != () and user != []:
                if user[0][1] == password:
                    if user[0][2] == "admin":
                        print("ID DELECTION READY",id)
                        self.db.mkRequest("deleteEmpruntByAuteurID", False, id)
                        self.db.mkRequest("deleteLivreByAuteur", False, id)#delete all books from this author first
                        self.db.mkRequest("deleteAuteur", False, id)
                        print("OK")
                        self.db.db.commit()
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
    def getEmprunt(self, email:str, password:str)->str:
        try : 
            #check password before 
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
        return open('www/html/index.html', encoding="utf-8")

    @cherrypy.expose
    def search(self, search:str, type:str="livre", sort="default", auteur="Tous") -> str :
        return open('www/html/search.html', encoding="utf-8")

    @cherrypy.expose
    def livre(self, isbn) -> str :
        return open('www/html/livre.html', encoding="utf-8")

    @cherrypy.expose
    def login(self) -> str :
        return open('www/html/login.html', encoding="utf-8")

    @cherrypy.expose
    def account(self) -> str :
        return open('www/html/account.html', encoding="utf-8")
    
    @cherrypy.expose
    def config(self) -> str :
        return open('www/html/config.html', encoding="utf-8")
    
    @cherrypy.expose
    def addLivre(self) -> str :
        return open('www/html/addLivre.html', encoding="utf-8")
    
    @cherrypy.expose
    def addAuteur(self) -> str :
        return open('www/html/addAuteur.html', encoding="utf-8")

    @cherrypy.expose
    def addPointDeVente(self) -> str :
        return open('www/html/addPointDeVente.html', encoding="utf-8")
    
    @cherrypy.expose
    def addEditeur(self) -> str :
        return open('www/html/addEditeur.html', encoding="utf-8")
    
    @cherrypy.expose
    def createAccount(self) -> str :
        return open('www/html/createAccount.html', encoding="utf-8")

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def updateBestLivres(self) -> str :
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
            print("Erreur lors de la mise à jour des livres de la page d'accueil", e, e.__traceback__.tb_lineno)
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getAllLivre(self) -> str:
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
    
    #Emprunts = ID, Livre (isbn), Date, Utilisateur (email)
      
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getAllEmprunts(self, email:str, password:str) -> str:
        try : 
            self.db.mkRequest("selectUserByEmail", True, email)
            user = self.db.cursor.fetchall()
            if user is not None and user != () and user != []:
                if user[0][1] == password:
                    if user[0][2] == "admin":
                        self.db.mkRequest("selectAllEmprunt")
                        emprunts = self.db.cursor.fetchall()
                        print("EMPRUNTS",emprunts)
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
        try : 
            #check password before
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
    def updateLivres(self) :
        try : 
            data = cherrypy.request.json
            email = data.get("email")
            password = data.get("password")
            self.db.mkRequest("selectUserByEmail", False, email)
            user = self.db.cursor.fetchall()
            if user is not None and user != () and user != []:
                if user[0][1] == password:
                    if user[0][2] == "admin":
                        livres = data.get("livres")
                        if livres is not None and livres != {}:
                            for livre in livres:
                                self.db.mkRequest("updateLivre", False, livre["titre"], livre["auteur"], livre["description"], livre["dateDeParution"], livre["status"], livre["genre"], livre["format"], livre["prix"], livre["pointDeVente"], livre["editeur"], livre["isbn"])
                                self.db.db.commit()
                        return self.makeResponse(content="success")
                    else:
                        return self.makeResponse(is_error=True, error_message="Vous n'êtes pas administrateur")
                else:
                    return self.makeResponse(is_error=True, error_message="Mot de passe incorrect")
        except Exception as e:
            print("\033[31mErreur lors de la mise à jour des livres : ",e, e.__traceback__.tb_lineno, "\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez vérifier les données envoyées")
    
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def updateAuteurs(self) :
        try :
            data = cherrypy.request.json
            email = data.get("email")
            password = data.get("password")
            self.db.mkRequest("selectUserByEmail", False, email)
            user = self.db.cursor.fetchall()
            if user is not None and user != () and user != []:
                if user[0][1] == password:
                    if user[0][2] == "admin":
                        auteurs = data.get("auteurs")
                        if auteurs is not None and auteurs != {}:
                            for auteur in auteurs:
                                print("AUTEUR MODIFIED :",auteur)
                                if auteur["dateDeNaissance"] == "":
                                    auteur["dateDeNaissance"] = None
                                if auteur["dateDeDeces"] == "":
                                    auteur["dateDeDeces"] = None
                                if auteur["dateDeNaissance"] != None:
                                    auteur["dateDeNaissance"] = auteur["dateDeNaissance"].split("/")
                                    auteur["dateDeNaissance"] = auteur["dateDeNaissance"][2]+"-"+auteur["dateDeNaissance"][1]+"-"+auteur["dateDeNaissance"][0]
                                if auteur["dateDeDeces"] != None:
                                    auteur["dateDeDeces"] = auteur["dateDeDeces"].split("/")
                                    auteur["dateDeDeces"] = auteur["dateDeDeces"][2]+"-"+auteur["dateDeDeces"][1]+"-"+auteur["dateDeDeces"][0]
                                if auteur["alias"] == "":
                                    auteur["alias"] = None
                                self.db.mkRequest("updateAuteur", False, auteur["nom"], auteur["prénom"], auteur["biographie"], auteur["dateDeNaissance"], auteur["dateDeDeces"],auteur["alias"], auteur["id"])
                                self.db.db.commit()
                        return self.makeResponse(content="success")
                    else:
                        return self.makeResponse(is_error=True, error_message="Vous n'êtes pas administrateur")
                else:
                    return self.makeResponse(is_error=True, error_message="Mot de passe incorrect")
        except Exception as e:
            print("\033[31mErreur lors de la mise à jour des auteurs : ",e, e.__traceback__.tb_lineno, "\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez vérifier les données envoyées")
    
    #adress, nom, url, tel (can be null)
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def updatePointDeVentes(self) :
        try :
            data = cherrypy.request.json
            email = data.get("email")
            password = data.get("password")
            self.db.mkRequest("selectUserByEmail", False, email)
            user = self.db.cursor.fetchall()
            if user is not None and user != () and user != []:
                if user[0][1] == password:
                    if user[0][2] == "admin":
                        pointDeVentes = data.get("pointDeVentes")
                        if pointDeVentes is not None and pointDeVentes != {}:
                            for pointDeVente in pointDeVentes:
                                if pointDeVente["tel"] == "":
                                    pointDeVente["tel"] = None
                                self.db.mkRequest("updatePointDeVente", False, pointDeVente["nom"], pointDeVente["url"], pointDeVente["tel"],  pointDeVente["adresse"])
                                self.db.db.commit()
                        return self.makeResponse(content="success")
                    else:
                        return self.makeResponse(is_error=True, error_message="Vous n'êtes pas administrateur")
                else:
                    return self.makeResponse(is_error=True, error_message="Mot de passe incorrect")
        except Exception as e:
            print("\033[31mErreur lors de la mise à jour des auteurs : ",e, e.__traceback__.tb_lineno, "\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez vérifier les données envoyées")
    
    #Editeur : nom (can be changed), addres: 
    
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def updateEditeurs(self) :
        try :
            data = cherrypy.request.json
            email = data.get("email")
            password = data.get("password")
            self.db.mkRequest("selectUserByEmail", False, email)
            user = self.db.cursor.fetchall()
            if user is not None and user != () and user != []:
                if user[0][1] == password:
                    if user[0][2] == "admin":
                        editeurs = data.get("editeurs")
                        if editeurs is not None and editeurs != {}:
                            for editeur in editeurs:
                                self.db.mkRequest("updateEditeur", False, editeur["adresse"], editeur["nom"])
                                self.db.db.commit()
                        return self.makeResponse(content="success")
                    else:
                        return self.makeResponse(is_error=True, error_message="Vous n'êtes pas administrateur")
                else:
                    return self.makeResponse(is_error=True, error_message="Mot de passe incorrect")
        except Exception as e:
            print("\033[31mErreur lors de la mise à jour des editeurs : ",e, e.__traceback__.tb_lineno, "\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez vérifier les données envoyées")
        
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def updateUtilisateurs(self) :
        print("REQUEST UPDATE USER RECEIVED")
        try :
            data = cherrypy.request.json
            email = data.get("email")
            password = data.get("password")
            self.db.mkRequest("selectUserByEmail", False, email)
            user = self.db.cursor.fetchall()
            if user is not None and user != () and user != []:
                if user[0][1] == password:
                    if user[0][2] == "admin":
                        print("ADMIN CONNECTED")
                        users = data.get("users")
                        if users is not None and users != {}:
                            for user in users:
                                self.db.mkRequest("updateUtilisateur", False, user["mdp"], user["grade"], user["nom"], user["prénom"], user["adresse"], user["tel"], user["email"])
                                self.db.db.commit()
                        return self.makeResponse(content="success")
                    else:
                        return self.makeResponse(is_error=True, error_message="Vous n'êtes pas administrateur")
                else:
                    return self.makeResponse(is_error=True, error_message="Mot de passe incorrect")
        except Exception as e:
            print("\033[31mErreur lors de la mise à jour des utilisateurs : ",e, e.__traceback__.tb_lineno, "\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez vérifier les données envoyées")
        
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def updateEmprunts(self) :
        try :
            data = cherrypy.request.json
            email = data.get("email")
            password = data.get("password")
            self.db.mkRequest("selectUserByEmail", True, email)
            user = self.db.cursor.fetchall()
            if user is not None and user != () and user != []:
                if user[0][1] == password:
                    if user[0][2] == "admin":
                        emprunts = data.get("emprunts")
                        if emprunts is not None and emprunts != {}:
                            for emprunt in emprunts:
                                date = emprunt["date"].split("/")
                                date = date[2]+"-"+date[1]+"-"+date[0]
                                self.db.mkRequest("updateEmprunt", False, emprunt["livre"], date, emprunt["utilisateur"], emprunt["id"])
                                self.db.db.commit()
                        return self.makeResponse(content="success")
                    else:
                        return self.makeResponse(is_error=True, error_message="Vous n'êtes pas administrateur")
                else:
                    return self.makeResponse(is_error=True, error_message="Mot de passe incorrect")
        except Exception as e:
            print("\033[31mErreur lors de la mise à jour des réservations : ",e, e.__traceback__.tb_lineno, "\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue, veuillez vérifier les données envoyées")
        
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def newLivre(self, **params):
        try:
            email = params.get("email")
            password = params.get("password")
            self.db.mkRequest("selectUserByEmail", False, email)
            user = self.db.cursor.fetchall()
            if user and user[0][1] == password:
                if user[0][2] == "admin":
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
                    pointDeVente = params.get("pointDeVente").strip()  # Remove leading/trailing whitespace
                    editeur = params.get("editeur")
                    image = params.get("image")
                    
                    # Check if all required fields are provided
                    if all([isbn, titre, auteur, description, dateDeParution, statut, genre, format, prix, pointDeVente, editeur]):
                        self.db.mkRequest("selectLivreByISBN", False, isbn)
                        checkISBN = self.db.cursor.fetchall()
                        if checkISBN:
                            return self.makeResponse(is_error=True, error_message="Un livre avec cet ISBN existe déjà")
                        print('.'+str(pointDeVente)+'.')
                        pointDeVente = operationOnDataBase.convertPointDeVenteToAcceptablePointDeVente(pointDeVente, self.db)
                        self.db.mkRequest("insertLivre", False, isbn, titre, auteur, description, note, dateDeParution, statut, genre, format, prix, pointDeVente, editeur)
                        self.db.db.commit()
                        try : 
                            upload_filename = isbn+".jpg"
                            upload_file_path = os.path.join("./www/img/livres", upload_filename)
                            print("UPLOADING IMAGE", upload_file_path)
                            #check if file exists if yes no upload security
                            if os.path.exists(upload_file_path) != False:
                                print("REFUSED UPLOAD, FILE EXISTS")
                                return self.makeResponse(is_error=True, error_message="Une image avec ce nom existe déjà")
                            with open(upload_file_path, 'wb') as out:
                                while True:
                                    data = image.file.read(8192)
                                    if not data:
                                        break
                                    out.write(data)
                        except Exception as e:
                            print("\033[31mErreur lors de l'ajout de l'image : ", e, e.__traceback__.tb_lineno, "\033[0m")
                        
                        return self.makeResponse(content="success")
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
        try:
            email = params.get("email")
            password = params.get("password")
            self.db.mkRequest("selectUserByEmail", False, email)
            user = self.db.cursor.fetchall()
            if user and user[0][1] == password:
                if user[0][2] == "admin":
                    print('New auteurs, connected')
                    nom = params.get("nom")
                    prenom = params.get("prenom")
                    alias = params.get("alias")
                    biographie = params.get("biographie")
                    dateDeNaissance = params.get("dateNaissance")
                    dateDeDeces = params.get("dateDeces")
                    if dateDeDeces == "":
                        dateDeDeces = None
                    if alias == "":
                        alias = None
                    if all([nom, prenom, biographie, dateDeNaissance]):
                        self.db.mkRequest("insertAuteur", False, nom, prenom, biographie, dateDeNaissance, dateDeDeces, alias)
                        self.db.db.commit()
                        return self.makeResponse(content="success")
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
    def newPointDeVente(self, **params):
        try:
            email = params.get("email")
            password = params.get("password")
            self.db.mkRequest("selectUserByEmail", False, email)
            user = self.db.cursor.fetchall()
            if user and user[0][1] == password:
                if user[0][2] == "admin":
                    nom = params.get("nom")
                    adresse = params.get("adresse")
                    url = params.get("url")
                    tel = params.get("tel")
                    if all([nom, adresse]):
                        self.db.mkRequest("insertPointDeVente", False, adresse, nom, url, tel)
                        self.db.db.commit()
                        return self.makeResponse(content="success")
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
    def newEditeur(self, **params):
        try:
            email = params.get("email")
            password = params.get("password")
            self.db.mkRequest("selectUserByEmail", False, email)
            user = self.db.cursor.fetchall()
            if user and user[0][1] == password:
                if user[0][2] == "admin":
                    nom = params.get("nom")
                    adresse = params.get("adresse")
                    if nom:
                        self.db.mkRequest("insertEditeur", False, nom, adresse)
                        self.db.db.commit()
                        return self.makeResponse(content="success")
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
    def newUser(self, **params):
        try :
            email = params.get("email")
            mdp = params.get("mdp")
            nom = params.get("nom")
            prenom = params.get("prenom")
            adresse = params.get("adresse")
            tel = params.get("tel")
            print("REQUEST RECEIVED", email, mdp, nom, prenom, adresse, tel)
            if all([mdp, nom, prenom, adresse, email, tel]):
                print("INSERTING USER")
                self.db.mkRequest("insertUtilisateur", False, email, mdp, "user", nom, prenom, adresse, tel)
                self.db.db.commit()
                return self.makeResponse(content="success")
            return self.makeResponse(is_error=True, error_message="Les données envoyées sont incorrectes")
        except Exception as e:
            print(f"Erreur : {e}")
            return self.makeResponse(is_error=True, error_message=str(e))
    
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