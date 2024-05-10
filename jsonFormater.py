import json, searchEngine, database

def formatLivreToJson(data:list[tuple], db:database.db)->json:
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

