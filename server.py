import operationOnDataBase, database
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
    def search(self, search):
        print("Recherche d'un livre...")
        if cherrypy.request.method == 'POST':
            search = operationOnDataBase.searchLivre(self.db, search)
            if search == None:
                raise cherrypy.HTTPError(status=404, message="Oups, nous n'avons rien trouvé pour votre recherche... Veuillez réessayer")
            return self.makeResponse(content=search)
    
    @cherrypy.expose
    def index(self) -> str :
        return open('www/html/index.html', encoding="utf-8")


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