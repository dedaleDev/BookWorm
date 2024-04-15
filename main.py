import database, operationOnDataBase
import os

#---------------------Configuration---------------------
db_HOST = "localhost"
db_USER = "root"
db_PASSWD = "1234"
db_PORT = 3306

debug = False #Ne pas utiliser en usage normal cela supprime l'ensemble des données au démarrage.
#------------------------------------------------------


def addElement(db) -> None:
    choiceListAddElement = [
            ("Livre",operationOnDataBase.addLivre, db),
            ("Auteur",operationOnDataBase.addAuthor)]
    showMenu(choiceAction=choiceListAddElement, title= "Que souhaitez vous ajouter ?")


def search(db) -> None:
    while True :
        choiceListSearch = [
                ("Livre",operationOnDataBase.searchAuteur, db),
                ("Auteur",operationOnDataBase.searchAuteur, db),
                ("Point de vente",operationOnDataBase.searchPointDeVente, db),
                ("Editeur",operationOnDataBase.searchEditeur, db),
                ("Tout rechercher",operationOnDataBase.searchAll, db),]
        if showMenu(choiceAction=choiceListSearch, title= "Que souhaitez vous rechercher ?") == 0 :
            return

def showMenu(choiceAction : list, title = "Menu") :
    """Show main menu"""
    if title == "Menu" :
        print(f"\n------------------{title}------------------")
    else : 
        print(f'\n------------------------------------\n\n{title}')
    for ch  in choiceAction:
        print (f'\t{choiceAction.index(ch)+1} : {ch[0]}')
    print (f'\t{len(choiceAction)+1} : Quitter (Ctrl + C)\n')
    while True :
        try : 
            choice = int(input("Veuillez saisir une opération : ").strip().split(' ')[0])
            if choice == len(choiceAction)+1 :#Quitter
                return 2
            elif choice >= 1 and len(choiceAction) >= choice:
                if len(choiceAction[choice-1]) == 2 :
                    result = choiceAction[choice-1][1]()
                else :
                    result = choiceAction[choice-1][1](choiceAction[choice-1][2])
                if result is not None:  # Si la fonction retourne une valeur, retourner cette valeur
                    return result
                return 1
            else :
                print("Choix invalide, veuillez réessayer.")
        except KeyboardInterrupt : 
            return 0
        except :
            print("Choix invalide, veuillez réessayer.")



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
        print("Attention : Le mode de débuggage est activé, les résultats résultant pourraient être instable.")
    db = database.db(db_HOST,db_USER,db_PASSWD,db_PORT,debug)
    
    if db.needRestart == True : 
        exit(0)
    
    print("Connexion à la base de donnée réussie !")

    choiceList = [ 
             ("Ajouter un élément",addElement,db),
             ("Rechercher",search,db),
             ]
    while True : 
        result = showMenu(choiceList)
        if result == 2 or result == 0 : 
            print("\nAu revoir !")
            break
