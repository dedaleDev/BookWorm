import database

def searchAuteur(nom_prenom_alias:str, db:database.db, onlyOne:bool = False)->list:
    try: 
        nom_prenom_alias = nom_prenom_alias.split()
        request_db = ["selectAuteurByPrenom", "selectAuteurByNom", "selectAuteurByAlias"]
        request = request_db[:len(nom_prenom_alias)]
        result = []
        for permutation in [nom_prenom_alias, list(reversed(nom_prenom_alias))]:
            for i in range(len(permutation)):
                db.mkRequest(request[i], False, '%'+nom_prenom_alias[i]+'%')
                result.append(db.cursor.fetchall())
        result = [list(i[0]) for i in result if i]
        temp = []
        for i in result:
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
        nom = '%'+nom+'%'
        db.mkRequest("selectPointDeVenteByName", False, nom)
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
        print("Une erreur est survenue lors de la recherche d'un point de vente : ",e ,e.__traceback__.tb_lineno)