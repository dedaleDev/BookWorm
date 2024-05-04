import json
from types import MethodType
from urllib.error import HTTPError
from json import JSONEncoder
import operationOnDataBase, database
import cherrypy, datetime, os, os.path

class API(object):
    def __init__(self, db:database.db):
        db = db

    def makeResponse(self, is_error=False, content=None, error_message=None):
        response = cherrypy.response
        if not is_error:
            return {"status":"ok", "content":content}
        else:
            return {"status":"error", "message":error_message}
    
    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def search(self):
        search = cherrypy.request.params['search']
        search = operationOnDataBase.searchLivre(self.db, search)
        if search == None:
            raise cherrypy.HTTPError(status=404, message="Oups, nous n'avons rien trouvé pour votre recherche... Veuillez réessayer")
        return self.makeResponse(content=search)

def jsonify_error(status, message, traceback, version):
    response = cherrypy.response
    response.headers['Content-Type'] = 'application/json'
    return json.dumps(
        {
            'status': 'error', 
            'http_status': status,
            'error_message': message
        }
)