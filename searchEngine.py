import database

def formatResult(result:list)->list:
    print(result)
    temp = []
    for i in result:#enlève les doublons
        if i not in temp and i != None and i != ( ):
            temp.append(i)
    temp = list(temp[0])
    print("SORTIE", result)
    return temp



def searchAuteur(recherche:str, db:database.db, onlyOne:bool = False)->list:
    try: 
        recherche = recherche.split()
        request = ["selectAuteurByPrenom", "selectAuteurByNom", "selectAuteurByAlias"]
        result = []
        for i in range(len(recherche)):
            for j in range(len(request)):
                db.mkRequest(request[j], False, '%'+recherche[i]+'%')#recherche dans la base de donnée
                result.append(db.cursor.fetchall())
        result = [list(i[0]) for i in result if i]#format les résultats
        temp = []
        for i in result:#enlève les doublons
            if i not in temp:
                temp.append(i)
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
        for i in range(len(recherche)):
            for j in range(len(request)):
                db.mkRequest(request[j], False, '%'+recherche[i]+'%')#recherche dans la base de donnée
                result.append(db.cursor.fetchall())
        temp = []
        for i in result:#enlève les doublons
            if i not in temp and i != None and i != ( ):
                temp.append(i)
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



def searchLivre():
    pass