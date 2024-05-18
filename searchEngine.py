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
        print("Le moteur de recherche à rencontré une erreur : ",e ,e.__traceback__.tb_lineno)

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

def getPointDeVenteNameByAddresse(db:database.db, addresse: str)->str:
    """This function return the name of the point of sale by his address
    Args :
        db : database object
        addresse : str, the address of the point of sale
    Return :
        str : the name of the point of sale"""
    try :
        db.mkRequest("selectPointDeVenteByAdresse", False, addresse)
        result = db.cursor.fetchall()
        if result == None or result == []: return "Nom du point de vente inconnu"
        return f"{result[0][1]}"
    except Exception as e:
        print(f"Une erreur est survenue lors de la recherche du point de vente :{e}, ligne : {e.__traceback__.tb_lineno}")


def searchAuteur(recherche:str, db:database.db, onlyOne:bool = False)->list:
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
        if onlyOne and len(result) > 1:
            print(f"Résultat de la recherche pour {' '.join(recherche)}:\n")
            for i in range(len(result)) : 
                if result[i][6] != None:
                    print(f"{i+1} : {result[i][2]} {result[i][1]},   {result[i][6]}")
                else :
                    print(f"{i+1} : {result[i][2]} {result[i][1]}")
            while True :
                try :
                    saisie = input("Veuillez saisir le numéro de l'auteur que vous souhaitez sélectionner : ")
                    if saisie.isdigit() and int(saisie) >= 1 and int(saisie) <= len(request):
                        return result[int(saisie)-1]
                    else:
                        print("Désolé, le format de la réponse est incorrect. Veuillez réessayer.")
                except KeyboardInterrupt:
                    return None
                except :
                    print("Désolé, le format de la réponse est incorrect. Veuillez réessayer.")
        if result == []:
            return None
        return result
    except Exception as e :
        print("Une erreur est survenue lors de la recherche d'auteur : ",e ,e.__traceback__.tb_lineno)

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
        
        print(result)
        temp = []
        for i in result:#enlève les doublons
            if i not in temp and i != None and i != ( ):
                temp.append(i)
        if temp == []:
            return None
        result = list(temp[0])
        if onlyOne and len(result) > 1:
            print(f"\nRésultat de la recherche pour {' '.join(recherche)}:\n")
            for i in range(len(result)) : 
                temp = result[i][0].split('\n')
                print(f"{i+1} : {temp},  {result[i][1]}")
            while True :
                try :
                    saisie = input("Veuillez saisir le numéro du point de vente que vous souhaitez sélectionner : ")
                    if saisie.isdigit() and int(saisie) >= 1 and int(saisie) <= len(result):
                        return result[int(saisie)-1]
                    else:
                        print("Désolé, le format de la réponse est incorrect. Veuillez réessayer.")
                except KeyboardInterrupt:
                    return None
                except :
                    print("Désolé, le format de la réponse est incorrect. Veuillez réessayer.")
        if result == []:
            return None
        return result
    except Exception as e :
        print("Une erreur est survenue lors de la recherche du point de vente : ",e ,e.__traceback__.tb_lineno)

def searchLivre(recherche:str, db:database.db, onlyOne:bool = False)->list:
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
                print("Recherche d'un code ISBN")
                request.insert(0, "selectLivreByISBN")
        result = searchEngine(recherche, request, db)
        result = [livre for elt in result for livre in elt]
        temp = []
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
        if onlyOne and len(result) > 1:#à enlever eventuellement si inutile
            print(f"\nRésultat de la recherche pour {' '.join(recherche)}:\n")
            for i in range(len(result)) : 
                print(f"{i+1} : {result[i][0]},  {result[i][1]},  {getAuteurNameByID(db,result[i][2])}")
            while True :
                try :
                    saisie = input("Veuillez saisir le numéro du livre que vous souhaitez sélectionner : ")
                    if saisie.isdigit() and int(saisie) >= 1 and int(saisie) <= len(result):
                        return result[int(saisie)-1]
                    else:
                        print("Désolé, le format de la réponse est incorrect. Veuillez réessayer.")
                except KeyboardInterrupt:
                    return None
                except :
                    print("Désolé, le format de la réponse est incorrect. Veuillez réessayer.")
        return result
    except Exception as e :
        print("Une erreur est survenue lors de la recherche du livre (searchLivre): ",e ,e.__traceback__.tb_lineno)

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
        if onlyOne and len(result) > 1:
            print(f"\nRésultat de la recherche pour {' '.join(recherche)}:\n")
            for i in range(len(result)) : 
                print(f"{i+1} :{result[i][0]},  {result[i][1]}")
            while True :
                try :
                    saisie = input("Veuillez saisir le numéro de l'editeur que vous souhaitez sélectionner : ")
                    if saisie.isdigit() and int(saisie) >= 1 and int(saisie) <= len(request):
                        return result[int(saisie)-1]
                    else:
                        print("Désolé, le format de la réponse est incorrect. Veuillez réessayer.")
                except KeyboardInterrupt:
                    return None
                except :
                    print("Désolé, le format de la réponse est incorrect. Veuillez réessayer.")
        if result == []:
            return None
        return result
    except Exception as e :
        print("Une erreur est survenue lors de la recherche d'editeur : ",e ,e.__traceback__.tb_lineno)


