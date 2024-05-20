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
                if user[0][1] == password:
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
            addresses = self.db.cursor.fetchall()
            if addresses is not None and addresses != () and addresses != []:
                addresses = utils.formatPointDeVenteToJson(addresses)
                return self.makeResponse(content=addresses)
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