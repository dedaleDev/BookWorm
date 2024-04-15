import database

def searchAuteur(nom_prenom_alias:str, db:database.db, onlyOne:bool = False)->list:
    try: 
        nom_prenom_alias = nom_prenom_alias.split()
        request = ["selectAuteurByPrenom", "selectAuteurByNom", "selectAuteurByAlias"]
        result = []
        for i in range(len(nom_prenom_alias)):
            for j in range(len(request)):
                db.mkRequest(request[j], False, '%'+nom_prenom_alias[i]+'%')#recherche dans la base de donnée
                result.append(db.cursor.fetchall())
        result = [list(i[0]) for i in result if i]#format les résultats
        temp = []
        for i in result:#enlève les doublons
            if i not in temp:
                temp.append(i)
        result = temp
        if onlyOne and len(result) > 1:
            print(f"Résultat de la recherche pour {' '.join(nom_prenom_alias)}:\n")
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

def searchPointDeVente(nom:str, db:database.db, onlyOne:bool = False)->list:
    try: 
        db.mkRequest("selectPointDeVenteByNom", False, '%'+nom+'%')#recherche dans la base de donnée
        result = db.cursor.fetchall()
        if onlyOne and len(result) > 1:
            print(f"Résultat de la recherche pour {nom}:\n")
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