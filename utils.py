import os
import json, searchEngine, database, searchEngine


def cleanFileNameForLivre()->None :
    """This function renames the files in the ./www/img/livre folder to remove spaces and add the .jpg extension."""
    try :
        path= os.listdir('www/img/livres')
        for file in path :  
            try : 
                if file.split('.')[-1] != 'jpg' :
                    newFileName = file.split('.')[0]+'.jpg'
                    os.rename(f'./www/img/livres/{file}', f'./www/img/livres/{newFileName}')
            except Exception as e:
                print(f"Erreur lors de la modification des fichiers : {e} ligne : {e.__traceback__.tb_lineno}")
    except Exception as e:
        print(f"Erreur lors de la modification des fichiers : {e} ligne : {e.__traceback__.tb_lineno}")

def formatLivreToJsonOrdered(data:list[tuple], db:database.db)->json:
    """This function converts a list of tuples to a JSON object. The order of the keys is the same as the one in the database.
    Args : 
        data : list of tuples
        db : database object
    Returns :
        json object"""
    try:
        result = []
        for item in data:
            if len(item) != 12:
                item = item[:12]
            ISBN, titre, auteur, description, note, dateDeParution, status, genre, format, prix, pointDeVente, editeur = item
            result.append({
                'ISBN': ISBN,
                'titre': titre,
                'auteur': searchEngine.getAuteurNameByID(db, auteur),
                'description': description,
                'note': note,
                'dateDeParution': dateDeParution.strftime("%d/%m/%Y"),
                'status': status,
                'genre': genre,
                'format': format,
                'prix': prix,
                'pointDeVente': pointDeVente,
                'pointDeVenteName': searchEngine.getPointDeVenteNameByAddresse(db, pointDeVente),
                'editeur': editeur
            })
        json_result = json.dumps(result, indent=4)
        return json_result
    except Exception as e:
        print("\033[31mErreur lors de la conversion en JSON : ", e, e.__traceback__.tb_lineno, "\033[0m")
        return None

def formatAuteurToJson(data:list[tuple])->json:
    """This function converts a list of tuples to a JSON object.
    Args : 
        data : list of tuples
        db : database object
    Returns :
        json object"""
    try :
        result = {}
        for item in data:
            if len(item) != 7:
                item = item[:4]
            ID, nom, prenom,description, dateDeNaissance, dateDeDécès, alias = item
            result[ID] = {
                'nom':nom,
                'prenom':prenom,
                'description':description,
                'dateDeNaissance':dateDeNaissance.strftime("%d/%m/%Y"),
                'dateDeDeces': dateDeDécès.strftime("%d/%m/%Y") if dateDeDécès is not None and dateDeDécès != "0000-00-00" else None,
                'alias':alias if alias != '' else None
            }
        json_result = json.dumps(result, indent=4)
        return json_result
    except Exception as e:
        print("\033[31mErreur lors de la conversion en JSON : ",e, e.__traceback__.tb_lineno, "\033[0m")
        return None
    
def formatPointDeVenteToJson(data:list[tuple])->json: 
    try :
        result = {}
        print("DATA",data)
        for item in data:
            print("TEST",item)
            if len(item) != 4:
                item = item[:4]
            adresse, nom, url, tel = item
            result[adresse] = {
                'nom':nom,
                'url':url,
                'tel':tel
            }
        json_result = json.dumps(result, indent=4)
        return json_result
    except Exception as e:
        print("\033[31mErreur lors de la conversion en JSON : ",e, e.__traceback__.tb_lineno, "\033[0m")
        return None
    
def formatEditeurToJson(data:list[tuple])->json:
    try :
        result = {}
        for item in data:
            if len(item) != 2:
                item = item[:2]
            nom, adresse = item
            result[nom] = {
                'adresse':adresse
            }
        json_result = json.dumps(result, indent=4)
        return json_result
    except Exception as e:
        print("\033[31mErreur lors de la conversion en JSON : ",e, e.__traceback__.tb_lineno, "\033[0m")
        return None
    
def formatLivreToJson(data:list[tuple], db:database.db)->json:
    """This function converts a list of tuples to a JSON object.
    Args : 
        data : list of tuples
        db : database object
    Returns :
        json object"""
    try :
        result = {}
        for item in data:
            if len(item) != 12:
                item = item[:12]
            ISBN, titre, auteur, description, note, dateDeParution, status, genre, format, prix, pointDeVente, editeur = item
            result[ISBN] = {
                'titre':titre,
                'auteur':searchEngine.getAuteurNameByID(db, auteur),
                'description':description,
                'note':note,
                'dateDeParution':dateDeParution.strftime("%d/%m/%Y"),
                'status':status,
                'genre':genre,
                'format':format,
                'prix':prix,
                'pointDeVente':pointDeVente,
                'pointDeVenteName':searchEngine.getPointDeVenteNameByAddresse(db, pointDeVente),
                'editeur':editeur
            }
        print("NOM PDV",searchEngine.getPointDeVenteNameByAddresse(db, pointDeVente))
        json_result = json.dumps(result, indent=4)
        return json_result
    except Exception as e:
        print("\033[31mErreur lors de la conversion en JSON : ",e, e.__traceback__.tb_lineno, "\033[0m")
        return None
    
def formatUserToJson(data:list[tuple])->json:
    try :
        result = {}
        for item in data:
            if len(item) != 7:
                item = item[:7]
            email, mdp, grade, nom, prénom, adresse, tel = item
            result[email] = {
                'mdp':mdp,
                'grade':grade,
                'nom':nom,
                'prénom':prénom,
                'adresse':adresse,
                'tel':tel
            }
        json_result = json.dumps(result, indent=4)
        return json_result
    except Exception as e:
        print("\033[31mErreur lors de la conversion en JSON : ",e, e.__traceback__.tb_lineno, "\033[0m")
        return None