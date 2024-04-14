import database

def getAnswer(question:str, type:str, min:int, max:int, content:str, enum:list=[], canBeNull:bool = False)->str:
    while True:
        try : 
            if type == "enum" and enum != []:#ENUM
                for i in range(len(enum)):
                    print(f"{i+1} : {enum[i]}")
            answer = input(question).strip()
            if answer == "" and canBeNull:
                return "Null"
            if type == "enum" and enum != []:#ENUM
                if answer.isdigit() and int(answer) >= 1 and int(answer) <= len(enum):
                    return enum[int(answer)-1]
                else:
                    print(f"Désolé, {content} doit être une valeur de la liste. Veuillez réessayer.")
            if type == "date":#DATE
                answer = answer.split('-').reverse()
                if len(answer) != 3 or not answer[0].isdigit() or not answer[1].isdigit() or not answer[2].isdigit():
                    print(f"Désolé, {content} doit être une date valide. Veuillez réessayer.")
                else :
                    return f"{answer[0]}-{answer[1]}-{answer[2]}"
            if type == "int":#INT
                if answer.isdigit() and int(answer) >= min and int(answer) <= max:
                    return int(answer)
                else:
                    print(f"Désolé, {content} doit être un nombre entier entre {str(min)} et {str(max) }. Veuillez réessayer.")
            elif type == "str":#STR
                while answer[0] == ' ':#enlève les espaces en début de chaîne
                    answer = answer[1:]
                while answer[-1] == ' ':#enlève les espaces en fin de chaîne
                    answer = answer[:-1]
                if len(answer) >= min and len(answer) <= max:
                    return answer
                else:
                    print(f"Désolé, {content} doit être une chaîne de caractères avec une taille comprise entre {str(min)} et {str(max)}. Veuillez réessayer.")
            elif type == "float":#FLOAT
                if answer.replace(".", "", 1).isdigit() and float(answer) >= min and float(answer) <= max:
                    return float(answer)
                else:
                    print(f"Désolé, {content} doit être un nombre réel entre {str(min)} et {str(max)}. Veuillez réessayer.")
        except KeyboardInterrupt:
            return None
        except :
            print("Désolé, le format de la réponse est incorrect. Veuillez réessayer.")

def searchAuteur(nomPrenomAlias:str, db:database.db, onlyOne:bool = False)->set:
    nomPrenomAlias = nomPrenomAlias.split(' ')
    result = set()
    requestdb = ["selectAuteurByPrenom", "selectAuteurByNom", "selectAuteurByAlias"]
    request = []
    for i in range(len(nomPrenomAlias)):
        request.append(requestdb[i])
    for i in range(len(request)):
        db.mkRequest(request[i], False, nomPrenomAlias[i])
        result.append(db.cursor.fetchall())
    if onlyOne:
        print(f"Résultat de la recherche pour {nomPrenomAlias}:\n")
        for i in request : 
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

def addLivre(db:database.db):
    try : 
        print("Ajout d'un nouveau livre :")
        ISBN = getAnswer("Entrez le code ISBN du livre : ", "str", 10, 13, "le code ISBN")
        if ISBN == None: return
        Titre = getAnswer("Entrez le titre du livre : ", "str", 1, 50, "le titre du livre")
        if Titre == None: return
        Auteur = getAnswer("Entrez le nom, prénom ou l'alias de l'auteur : ", "str", 1, 50, "l'auteur")
        if Auteur == None: return
        Auteur = searchAuteur(Auteur, db, True)[0]
        if Auteur == None: return
        Description = getAnswer("Entrez une description pour le livre : ", "str", 0, 1000, "la description")
        if Description == None: return
        Note = getAnswer("Entrez la note initiale du livre : ", "float", 0, 20, "la note")
        if Note == None: return
        DateDeParution = getAnswer("Entrez la date de parution du livre (attendu JJ-MM-AAAA): ", "date", "la date de parution")
        if DateDeParution == None: return
        Statut = getAnswer("Veuillez saisir le statut à attribuer", "enum", content="le statut",enum=["Disponible", "Emprunté", "hors stock"])
        if Statut == None: return
        print("Recapitulatif :")
        print(f"ISBN : {ISBN}\nTitre : {Titre}\nAuteur : {Auteur}\nDescription : {Description}\nNote : {Note}\nDate de parution : {DateDeParution}\nStatut : {Statut}")
    except Exception as e:
        print(f"Une erreur est survenue lors de l'ajout du livre :{e}, ligne : {e.__traceback__.tb_lineno}")
    


    

def addAuthor():
    return