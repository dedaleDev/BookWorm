import os
import json, searchEngine, database


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
                'editeur':editeur
            }
        json_result = json.dumps(result, indent=4)
        return json_result
    except Exception as e:
        print("\033[31mErreur lors de la conversion en JSON : ",e, e.__traceback__.tb_lineno, "\033[0m")
        return None

