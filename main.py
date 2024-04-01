import database
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
    db = database.db()
    print("Connexion à la base de donnée réussie !")