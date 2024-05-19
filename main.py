import database, operationOnDataBase, server, utils
import os, cherrypy, shutil

#---------------------Configuration---------------------
db_HOST = "localhost"
db_USER = "root"
db_PASSWD = "1234"
db_PORT = 3306

debug = False #Ne pas utiliser en usage normal, cela supprime l'ensemble des données au démarrage. En cas de problème, essayez d'activer ce mode.

www_dir = os.path.abspath('./www')
print(os.path.join(www_dir, 'css'))
serverConf = {
    'global': {
        'server.socket_host': '192.168.1.20',#si necessaire, changez l'adresse IP du site web
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
    }
}

#------------------------------------------------------

def search(db:database.db) -> None:
    """This function creates a search menu and calls the search function from operationOnDataBase.py. Take the database object as a parameter."""
    while True :
        choiceListSearch = [
                ("Livre",operationOnDataBase.searchLivre, db),
                ("Auteur",operationOnDataBase.searchAuteur, db),
                ("Point de vente",operationOnDataBase.searchPointDeVente, db),
                ("Editeur",operationOnDataBase.searchEditeur, db)]
        if showMenu(choiceAction=choiceListSearch, title= "Que souhaitez-vous rechercher ?", defaultChoice=True, question="Veuillez saisir l'objet de votre recherche ou rechercher un livre : " ) == 2 :
            return

def addElement(db:database.db) -> None:
    """This function creates a menu to add an element to the database. Take the database object as a parameter."""
    choiceListAddElement = [
            ("Livre",operationOnDataBase.addLivre, db),
            ("Auteur",operationOnDataBase.addAuteur,db),
            ("Point de vente",operationOnDataBase.addPointDeVente,db),
            ("Editeur",operationOnDataBase.addEditeur,db)]
    showMenu(choiceAction=choiceListAddElement, title= "Que souhaitez-vous ajouter ?")

def deleteElement(db:database.db) -> None:
    """This function creates a menu to delete an element from the database."""
    choiceListDeleteElement = [
            ("Livre",operationOnDataBase.deleteLivre, db),
            ("Auteur",operationOnDataBase.deleteAuteur,db),
            ("Point de vente",operationOnDataBase.deletePointDeVente,db),
            ("Editeur",operationOnDataBase.deleteEditeur,db)]
    showMenu(choiceAction=choiceListDeleteElement, title= "Que souhaitez-vous supprimer ?")

def editElement(db:database.db) -> None:
    """This function creates a menu to edit an element from the database."""
    choiceListEditElement = [
            ("Livre",operationOnDataBase.editLivre, db),
            ("Auteur",operationOnDataBase.editAuteur,db),
            ("Point de vente",operationOnDataBase.editPointDeVente,db),
            ("Editeur",operationOnDataBase.editEditeur,db)]
    showMenu(choiceAction=choiceListEditElement, title= "Que souhaitez-vous editer ?")

def config(db:database.db):
    """This function creates a configuration menu."""
    while True :
        choiceListConfig = [
                ("Ajouter un livre, auteur...",addElement, db),
                ("Editer un livre, auteur...",editElement, db),
                ("Supprimer un livre, auteur...",deleteElement, db)]
        if showMenu(choiceAction=choiceListConfig, title= "Menu de configuration") == 2 :
            return


def showMenu(choiceAction : list, title = "Menu", defaultChoice:bool = False, question:str="Veuillez saisir une opération : "):
    """This function creates a menu with the choiceAction list.
        Args :
            choiceAction : list of tuple with the following format : (str, function, *args)
            title : str, title of the menu
            defaultChoice : bool, if True, the user can enter a string to select the first choice
            question : str, question to ask the user
        Return :
            1 : if the function returns None
            2 : if the user wants to quit
    """
    if title == "Menu" :
        print(f"\n---------------{title}---------------")
    else : 
        print(f'\n------------------------------------\n\n{title}')
    for ch  in choiceAction:
        print (f'\t{choiceAction.index(ch)+1} : {ch[0]}')
    print (f'\t{len(choiceAction)+1} : Quitter (Ctrl + C)\n')
    while True :
        try : 
            if not defaultChoice :
                operation = input(question).strip().split(' ')[0]
            else :
                operation = input(question).strip()
            if operation.isdigit() :
                choice = int(operation)
            elif operation :
                choice = -1
            else :
                print("Choix invalide, veuillez réessayer.")
                continue
            if choice == len(choiceAction)+1 :#Quitter
                return 2
            elif choice >= 1 and len(choiceAction) >= choice :
                if len(choiceAction[choice-1]) == 2 :
                    result = choiceAction[choice-1][1]()
                else :
                    result = choiceAction[choice-1][1](choiceAction[choice-1][2])
                if result is not None:  # Si la fonction retourne une valeur, retourner cette valeur
                    return result
                return 1
            elif defaultChoice and choice == -1:
                result = choiceAction[0][1](choiceAction[choice-1][2],operation)
                if result is not None: 
                    return result
                return 1
            else :
                print("Choix invalide, veuillez réessayer.")
        except KeyboardInterrupt : 
            return 2
        except Exception as e:
            print("Choix invalide, veuillez réessayer.",e, e.__traceback__.tb_lineno)
            
def updateJS(conf: dict):
    """This function updates the API_URL in js files. 
    Args : 
        conf : dict, configuration of the server cherrypy"""
    try :
        api_url = f"http://{conf['global']['server.socket_host']}:{conf['global']['server.socket_port']}"
        files = ['www/js/index.js', 'www/js/search.js', 'www/js/livre.js', 'www/js/login.js','www/js/account.js','www/js/config.js']
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
    print(r"""
        ______             _      _    _                      
        | ___ \           | |    | |  | |                     
        | |_/ / ___   ___ | | __ | |  | | ___  _ __ _ __ ___  
        | ___ \/ _ \ / _ \| |/ / | |/\| |/ _ \| '__| '_ ` _ \ 
        | |_/ / (_) | (_) |   <  \  /\  / (_) | |  | | | | | |
        \____/ \___/ \___/|_|\_\  \/  \/ \___/|_|  |_| |_| |_|
        """                            
    )
    print("Initialisation...")
    if debug : 
        print("Attention : le mode de débogage est activé, les résultats résultants pourraient être instables.")
    db = database.db(db_HOST,db_USER,db_PASSWD,db_PORT,debug)
    
    if db.needRestart == True : 
        exit(0)
    print("Connexion à la base de donnée réussie !")
    print("Démarrage du site web...")
    utils.cleanFileNameForLivre()
    try : 
        updateJS(serverConf)
        cherrypy.quickstart(server.Server(db,serverConf ), '/', serverConf)
    except Exception as e:
        print(f"\033[91mErreur : Impossible de démarrer le serveur web. Veuillez vérifier que le port 8080 et 8092 sont disponibles. {e} ligne : {e.__traceback__.tb_lineno}\033[0m")
