import database

debug = False #Permet de faciliter le débugage. Ne pas utiliser en usage normal.

if __name__ == '__main__':
    print("""
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
        print("Attention : Le mode de débuggage est activé, les résultats résultant pourraient être instable.")
    db = database.db(debug=debug)
    print("Connexion à la base de donnée réussie !")