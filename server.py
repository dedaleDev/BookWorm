import operationOnDataBase, database, jsonFormater
import cherrypy, os, json

class Server(object):
    def __init__(self, db:database.db, conf:dict):
        self.db = db
        self.conf = conf

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
    def searchLivre(self, search):
        try : 
            searchResult = operationOnDataBase.searchLivre(self.db, search)
            searchResult = jsonFormater.formatLivreToJson(searchResult, self.db)
            print(f"\033[91mRecherche effectuée :  {searchResult}\033[0m")
            print(f"\033[91mreponse :  {self.makeResponse(content=searchResult)}\033[0m")
            return self.makeResponse(content=searchResult)
        except Exception as e:
            print("\033[31mErreur lors de la recherche : ",e, e.__traceback__.tb_lineno, searchResult, "\033[0m")
            return self.makeResponse(is_error=True, error_message="Oups, une erreur est survenue : "+ str(e))
    
    
    @cherrypy.expose
    def index(self) -> str :
        return open('www/html/index.html', encoding="utf-8")
    
    @cherrypy.expose
    def search(self, search) -> str :
        return open('www/html/search.html', encoding="utf-8")


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