import database, server, utils
import os, cherrypy

#---------------------Configuration---------------------
db_HOST = "localhost"#changer si nécessaire
db_USER = "root"#changer
db_PASSWD = "1234"#changer
db_PORT = 3306

debug = False #Rénitialise l'ensemble des données au démarrage. En cas de problème, essayez d'activer ce mode.

www_dir = os.path.abspath('./www')
print(os.path.join(www_dir, 'css'))
serverConf = {
    'global': {
        'server.socket_host': '127.0.0.1',#si nécessaire, changez l'adresse IP du site web
        'server.socket_port': 8080,
        'error_page.default': server.jsonify_error,
    },
    '/': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': www_dir
    },
    '/html': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(www_dir, 'html')
    },
    '/css': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(www_dir, 'css')
    },
    '/img': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(www_dir, 'img')
    },
    '/frameworks': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(www_dir, 'frameworks')
    },
    '/js': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(www_dir, 'js'),
    },
    '/api': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.response_headers.on': True,
        'tools.response_headers.headers': [
            ('Content-Type', 'application/json'),
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', 'POST, GET'),
            ('Access-Control-Allow-Headers', 'Content-Type'),
        ],
    },
    '/favicon.ico': {
        'tools.staticfile.on': True,
        'tools.staticfile.filename': os.path.join(www_dir, 'img/favicon.ico')
    }
}

#------------------------------------------------------

def updateJS(conf: dict):
    """This function updates the API_URL in js files. 
    Args : 
        conf : dict, configuration of the server cherrypy"""
    try :
        api_url = f"http://{conf['global']['server.socket_host']}:{conf['global']['server.socket_port']}"
        files = ['www/js/index.js', 'www/js/search.js', 'www/js/livre.js', 'www/js/login.js','www/js/account.js','www/js/config.js','www/js/addLivre.js','www/js/addAuteur.js','www/js/addPointDeVente.js', 'www/js/addEditeur.js', 'www/js/createAccount.js', ]
        for file in files :
            with open(file, 'r', encoding='utf-8') as f:
                code = f.readlines()
                with open(file, 'w', encoding='utf-8') as newFile : 
                    for line in code :
                        if line.startswith("const API_URL ="):
                            line = f"const API_URL = '{api_url}'\n"
                        newFile.write(line)
    except Exception as e: 
        print(f"\033[91mErreur : Impossible de modifier correctement les urls d'API. {e} ligne : {e.__traceback__.tb_lineno}\033[0m")



if __name__ == '__main__':
    print("\033[35m")
    print(r"""
        ______             _      _    _                      
        | ___ \           | |    | |  | |                     
        | |_/ / ___   ___ | | __ | |  | | ___  _ __ _ __ ___  
        | ___ \/ _ \ / _ \| |/ / | |/\| |/ _ \| '__| '_ ` _ \ 
        | |_/ / (_) | (_) |   <  \  /\  / (_) | |  | | | | | |
        \____/ \___/ \___/|_|\_\  \/  \/ \___/|_|  |_| |_| |_|
        """                            
    )
    print("\033[0m")
    print("Initialisation...")
    if debug : 
        print("Attention : Le mode debug est activé. Toutes les données vont être réinitialisées.")
    db = database.db(db_HOST,db_USER,db_PASSWD,db_PORT,debug)
    if db.needRestart == True : 
        exit(0)
    print("\033[32mConnexion à la base de donnée réussie !\033[0m")
    print("Démarrage du site web...")
    utils.cleanFileNameForLivre()
    try : 
        updateJS(serverConf)
        cherrypy.quickstart(server.Server(db,serverConf ), '/', serverConf)
    except Exception as e:
        print(f"\033[91mErreur : Impossible de démarrer le serveur web. Veuillez vérifier que le port du site web est disponible (defaut 8080). {e} ligne : {e.__traceback__.tb_lineno}\033[0m")
