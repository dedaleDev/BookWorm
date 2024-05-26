import database

def searchEngine(recherche:list,requests:list, db:database.db)->tuple:
    """This function is the search engine of the program. 
    Args :
        recherche : list of str, the words to search
        requests : list of str, the requests to make in the database
        db : database object
    Return :
        result : list of tuple, the result of the search
    """
    try : 
        result = []
        blacklistword = ["le", "la", "les", "de", "du", "des", "un","moi", "une", "dans", "sur", "avec", "c'est","pour", "par", "et", "ou", "mais", "donc", "or", "ni", "car", "que","a", "the","an","of","in","on","with","for","by","and","or","but","so","yet","nor","because","that","to"]
        if len(recherche) > 30:#tronque la recherche si elle est trop longue pour éviter max recursion depth
            recherche = recherche[:30]
        for i in range(len(recherche)):
            if recherche[i].lower() in blacklistword:
                continue
            for j in range(len(requests)):
                db.mkRequest(requests[j], False, '%'+recherche[i]+'%')#recherche dans la base de donnée
                result.append(db.cursor.fetchall())
        return result
    except Exception as e :
        print("\033[31mLe moteur de recherche à rencontré une erreur : ",e ,e.__traceback__.tb_lineno,"\033[0m")

def getAuteurNameByID(db:database.db, id:int)->str:
    """This function return the name of the author by his ID
    Args :
        db : database object
        id : int, the ID of the author
    Return :
        str : the name of the author"""
    try :
        db.mkRequest("selectAuteurByID", False, id)
        result = db.cursor.fetchall()
        if result == None or result == []: return "Auteur inconnu"
        if result[0][6] != None:
            return f"{result[0][6]}"
        return f"{result[0][2]} {result[0][1]}"
    except Exception as e:
        print(f"Une erreur est survenue lors de la recherche de l'auteur :{e}, ligne : {e.__traceback__.tb_lineno}")

def getAuteurAliasByID(db:database, id:int)->str:
    """This function return the alias of the author by his ID
    Args :
        db : database object
        id : int, the ID of the author
    Return :
        str : the alias of the author"""
    try :
        db.mkRequest("selectAuteurByID", False, id)
        result = db.cursor.fetchall()
        if result == None or result == []: return "Auteur inconnu"
        return f"{result[0][6]}"
    except Exception as e:
        print(f"\033[31mUne erreur est survenue lors de la recherche de l'auteur :{e}, ligne : {e.__traceback__.tb_lineno}\033[0m")
        
def getAuteurIDByNomPrénom(db:database.db, nom:str, prenom:str)->int:
    """This function return the ID of the author by his name and first name
    Args :
        db : database object
        nom : str, the name of the author
        prenom : str, the first name of the author
    Return :
        int : the ID of the author"""
    try :
        db.mkRequest("selectAuteurByNomPrenom", False, nom, prenom)
        result = db.cursor.fetchall()
        if result == None or result == []: return "Auteur inconnu"
        return f"{result[0][0]}"
    except Exception as e:
        print(f"\033[31mUne erreur est survenue lors de la recherche de l'auteur :{e}, ligne : {e.__traceback__.tb_lineno}\033[0m")

def getPointDeVenteNameByAddresse(db:database.db, adresse: str)->str:
    """This function return the name of the point of sale by his adresse
    Args :
        db : database object
        adresse : str, the adresse of the point of sale
    Return :
        str : the name of the point of sale"""
    try :
        db.mkRequest("selectPointDeVenteByAdresse", False, adresse)
        result = db.cursor.fetchall()
        if result == None or result == []: return "Nom du point de vente inconnu"
        return f"{result[0][1]}"
    except Exception as e:
        print(f"\033[31mUne erreur est survenue lors de la recherche du point de vente :{e}, ligne : {e.__traceback__.tb_lineno}\033[0m")


def searchAuteur(recherche:str, db:database.db)->list:
    """This function search an author in the database
    Args :
        recherche : str, the name of the author
        db : database object
        onlyOne : bool, if True, the function return only one result
    Return :
        result : list of tuple, the result of the search"""
    try: 
        recherche = recherche.strip().split()
        request = ["selectAuteurByPrenom", "selectAuteurByNom", "selectAuteurByAlias"]
        result = searchEngine(recherche, request, db)
        result = [list(i[0]) for i in result if i]#format les résultats
        temp = []
        for i in result:#enlève les doublons
            if i not in temp:
                temp.append(i)
        if temp == []:
            return None
        result = temp
        if result == []:
            return None
        return result
    except Exception as e :
        print("\033[31mUne erreur est survenue lors de la recherche d'auteur : ",e ,e.__traceback__.tb_lineno,"\033[0m")

def searchPointDeVente(recherche:str, db:database.db, onlyOne:bool = False)->list:
    """This function search a point of sale in the database
    Args :
        recherche : str, the name of the point of sale
        db : database object
        onlyOne : bool, if True, the function return only one result
    Return :
        result : list of tuple, the result of the search"""
    try: 
        result = []
        recherche = recherche.strip().split()
        request = ["selectPointDeVenteByNom", "selectPointDeVenteByAdresse"]
        result = searchEngine(recherche, request, db)
        temp = []
        for i in result:#enlève les doublons
            if i not in temp and i != None and i != ( ):
                temp.append(i)
        if temp == []:
            return None
        result = list(temp[0])
        if onlyOne and len(result) > 1:
            return result[0]
        if result == []:
            return None
        return result
    except Exception as e :
        print("\033[31mUne erreur est survenue lors de la recherche du point de vente : ",e ,e.__traceback__.tb_lineno,"\033[0m")

def searchLivre(recherche:str, db:database.db)->list:
    """This function search a book in the database
    Args :
        recherche : str, the name of the book
        db : database object
        onlyOne : bool, if True, the function return only one result
    Return :
        result : list of tuple, the result of the search"""
    try: 
        result = []
        recherche = recherche.strip().split()
        request = ["selectLivreByTitre", "selectLivreByDescription","selectLivreByAuteurPrénom","selectLivreByAuteurNom","selectLivreByAuteurAlias","selectLivreByGenre"]
        for i in recherche: #evite les recherches de type ISBN si la recherche ne contient pas suffisament de chiffres
            if len(i) > 4 and i.isdigit():
                request.insert(0, "selectLivreByISBN")
        result = searchEngine(recherche, request, db)
        result = [livre for elt in result for livre in elt]
        temp = []
        sortOrder = []
        #tri par ordre de pertinence : plus les elements sont duppliqués, plus ils sont pertinents
        for i in result:
            max = 0
            for j in result : 
                if j[0] == i[0]:
                    max += 1
            sortOrder.append((i,max))
        sortOrder.sort(key=lambda x: x[1], reverse=True)
        result = [i[0] for i in sortOrder]
        for i in result:#enlève les doublons
            if i not in temp and i != None and i != ( ):
                doublon = False
                for j in temp : 
                    if i[0] == j[0]:
                        doublon = True
                        break
                if not doublon:
                    temp.append(i)
        if temp == []:
            return None
        result = temp
        return result
    except Exception as e :
        print("\033[31mUne erreur est survenue lors de la recherche du livre (searchLivre): ",e ,e.__traceback__.tb_lineno,"\033[0m")

def searchEditeur(recherche:str, db:database.db, onlyOne:bool = False)->list:
    """This function search a publisher in the database
    Args :
        recherche : str, the name of the publisher
        db : database object
        onlyOne : bool, if True, the function return only one result
    Return :
        result : list of tuple, the result of the search"""
    try :
        recherche = recherche.split()
        request = ["selectEditeurByNom", "selectEditeurByAdresse"]
        result = searchEngine(recherche, request, db)
        result = [list(i[0]) for i in result if i]#format les résultats
        temp = []
        for i in result:#enlève les doublons
            if i not in temp:
                temp.append(i)
        result = temp
        if result == []:
            return None
        return result
    except Exception as e :
        print("\033[31mUne erreur est survenue lors de la recherche d'editeur : ",e ,e.__traceback__.tb_lineno,"\033[0m")