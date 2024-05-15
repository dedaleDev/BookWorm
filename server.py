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
            #print("SEARCH RESULT", searchResult)
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
    def index(self) -> str :
        return open('www/html/index.html', encoding="utf-8")
    
    @cherrypy.expose
    def search(self, search:str, type:str="livre", sort="default", auteur="Tous") -> str :
        return open('www/html/search.html', encoding="utf-8")

    @cherrypy.expose
    def livre(self, isbn) -> str :
        return open('www/html/livre.html', encoding="utf-8")
        
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