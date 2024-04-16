import database

def searchEngine(recherche:list,requests:list, db:database.db)->tuple:
    result = []
    for i in range(len(recherche)):
        for j in range(len(requests)):
            db.mkRequest(requests[j], False, '%'+recherche[i]+'%')#recherche dans la base de donnée
            result.append(db.cursor.fetchall())
    return result


def searchAuteur(recherche:str, db:database.db, onlyOne:bool = False)->list:
    try: 
        recherche = recherche.split()
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
                print(f"{i} : {result[i]}")
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
        return result
    except Exception as e :
        print("Une erreur est survenue lors de la recherche d'auteur : ",e ,e.__traceback__.tb_lineno)

def searchPointDeVente(recherche:str, db:database.db, onlyOne:bool = False)->list:
    try: 
        result = []
        recherche = recherche.split()
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
            print(f"Résultat de la recherche pour {recherche}:\n")
            for i in range(len(result)) : 
                print(f"{i} : {result[i]}")
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
        return result
    except Exception as e :
        print("Une erreur est survenue lors de la recherche du point de vente : ",e ,e.__traceback__.tb_lineno)



def searchLivre(recherche:str, db:database.db, onlyOne:bool = False)->list:
    try: 
        result = []
        recherche = recherche.split()
        request = ["selectLivreByTitre", "selectLivreByDescription","selectLivreByAuteurPrénom","selectLivreByAuteurNom","selectLivreByAuteurAlias","selectLivreByGenre"]
        for i in recherche: #evite les recherches de type ISBN si la recherche ne contient pas suffisament de chiffres
            if len(i) > 4 and i.isdigit():
                print("Recherche d'un code ISBN")
                request.insert(0, "selectLivreByISBN")
        result = searchEngine(recherche, request, db)
        temp = []
        for i in result:#enlève les doublons
            if i not in temp and i != None and i != ( ):
                temp.append(i)
        if temp == []:
            return None
        result = list(temp[0])
        if onlyOne and len(result) > 1:
            print(f"Résultat de la recherche pour {recherche}:\n")
            for i in range(len(result)) : 
                print(f"{i} : {result[i]}")
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
            print(f"Résultat de la recherche pour {recherche}:\n")
            for i in range(len(result)) : 
                print(f"{i} : {result[i]}")
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
        return result
    except Exception as e :
        print("Une erreur est survenue lors de la recherche d'editeur : ",e ,e.__traceback__.tb_lineno)