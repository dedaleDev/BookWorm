import database,searchEngine

def getAnswer(question:str, type:str, content:str, min_int:int=0, max_int:int=5, enum:list=[], canBeNull:bool = False)->str:
    while True:
        try : 
            if type == "enum" and enum != []:  # ENUM
                print(f"Définir {content.lower()} :")
                try :
                    max_length = max(len(str(e)) for e in enum)
                    if len(enum) < 10:
                        for i in range(len(enum)):
                            print(f"{i+1} : {enum[i]}")
                    else:
                        for i in range(len(enum)):
                            print(f"\t{i+1} : {str(enum[i]).ljust(max_length)}", end=" ")
                            if (i+1) % 3 == 0:
                                print()
                    print()
                except Exception as e :
                    print(e, e.__traceback__.tb_lineno)
            answer = input(question).strip()
            if answer == "" and canBeNull:
                return "Null"
            if type == "enum" and enum != []:#ENUM
                if answer.isdigit() and int(answer) >= 1 and int(answer) <= len(enum):
                    return enum[int(answer)-1]
                else:
                    print(f"{content} doit être une valeur de la liste. Veuillez réessayer.")
            if type == "date":#DATE
                if '/' in answer:
                    answer = answer.replace('/', '-')
                answer = answer.split('-')
                answer.reverse()
                print(answer)
                if len(answer) != 3 or not answer[0].isdigit() or not answer[1].isdigit() or not answer[2].isdigit():
                    print(f"{content} doit être une date valide. Veuillez réessayer.")
                else :
                    return f"{answer[0]}-{answer[1]}-{answer[2]}"
            if type == "int":#INT
                if answer.isdigit() and int(answer) >= min_int and int(answer) <= max_int:
                    return int(answer)
                else:
                    print(f"{content} doit être un nombre entier entre {str(min_int)} et {str(max_int) }. Veuillez réessayer.")
            elif type == "str":#STR
                while answer[0] == ' ':#enlève les espaces en début de chaîne
                    answer = answer[1:]
                while answer[-1] == ' ':#enlève les espaces en fin de chaîne
                    answer = answer[:-1]
                if " ISBN" in content and (not answer.isdigit()  or not len(answer) >= min_int or not len(answer) <= max_int):
                    print(f"{content} doit être une chaîne de caractères numériques de taille comprise entre {str(min_int)} et {str(max_int)} chiffres. Veuillez réessayer.")
                    continue
                if len(answer) >= min_int and len(answer) <= max_int:
                    return answer
                else:
                    print(f"{content} doit être une chaîne de caractères avec une taille comprise entre {str(min_int)} et {str(max_int)}. Veuillez réessayer.")
            elif type == "float":#FLOAT
                if answer.replace(".", "", 1).isdigit() and float(answer) >= min_int and float(answer) <= max_int:
                    return float(answer)
                else:
                    print(f"{content} doit être un nombre réel entre {str(min_int)} et {str(max_int)}. Veuillez réessayer.")
        except KeyboardInterrupt:
            return None
        except Exception as e:
            print("Désolé, le format de la réponse est incorrect. Veuillez réessayer.", answer, e, e.__traceback__.tb_lineno)



def addLivre(db:database.db):
    try : 
        print("\n------------Nouveau livre-----------\n")
        ISBN = getAnswer("Entrez le code ISBN du livre : ", "str","Le code ISBN", 10, 13,)
        if ISBN == None: return
        Titre = getAnswer("Entrez le titre du livre : ", "str","Le titre du livre", 1, 50)
        if Titre == None: return
        Auteur = getAnswer("Entrez le nom, prénom ou l'alias de l'auteur : ", "str", "L'auteur", 1, 50)
        if Auteur == None: return
        try :
            Auteur = searchEngine.searchAuteur(Auteur, db, True)[0]
        except : Auteur = None
        if Auteur == None: 
            print("Désolé, mais aucun auteur n'a été trouvé pour ce livre.")#proposer d'en ajouter
            return
        print(f"Vous avez selectionné l'auteur : {Auteur[2]} {Auteur[1]}")
        Description = getAnswer("Entrez une description pour le livre : ", "str", "La description", 0, 1000)
        if Description == None: return
        Note = getAnswer("Entrez la note initiale du livre (attendu 0-10) : ", "float", "la note", 0, 10)
        if Note == None: return
        DateDeParution = getAnswer("Entrez la date de parution du livre (attendu JJ/MM/AAAA): ", "date", "La date de parution")
        if DateDeParution == None: return
        Statut = getAnswer("Veuillez choisir le statut à attribuer : ", "enum", content="Le statut",enum=["Disponible", "Emprunté", "hors stock"])
        if Statut == None: return
        Genre = getAnswer("Veuillez choisir le genre du livre : ", "enum", content="Le genre",enum=["Historique","Romantique","Policier","Science-fiction","Fantastique","Aventure","Biographique","Autobiographique","Épistolaire","Thriller","Tragédie","Drame","Absurde","Philosophique","Politique","Légendes & Mythes","Lettres personnelles","Voyages","Journal intime","Bandes dessinées","Documentaires","Religieux"])
        if Genre == None: return
        Format = getAnswer("Veuillez choisir le format du livre : ", "enum", content="Le format",enum=["Poche","Grand Format","E-book & numérique","Manga","Bande Dessinée","Magazine","CD","DVD & Blu-ray"])
        if Format == None: return
        Prix = getAnswer("Entrez le prix moyen du livre en librairie : ", "float", "Le prix", 0, 1000)
        if Prix == None: return
        PointDeVente = getAnswer("Entrez le nom du point de vente du livre : ", "str", "Le point de vente", 1, 50)
        try :
            PointDeVente = searchEngine.searchPointDeVente(PointDeVente, db, True)[0]
        except : PointDeVente = None
        if PointDeVente == None: return
        print("\n------------Recapitulatif-----------\n")
        if Auteur[3] == None : 
            print(f"ISBN : {ISBN}\nTitre : {Titre}\nAuteur : {Auteur[2]}{Auteur[1]}\nDescription : {Description}\nNote : {Note}\nDate de parution : {DateDeParution}\nStatut : {Statut}")
        else :
            print(f"ISBN : {ISBN}\nTitre : {Titre}\nAuteur : {Auteur[3]}\nDescription : {Description}\nNote : {Note}\nDate de parution : {DateDeParution}\nStatut : {Statut}")
        if input("Voulez-vous ajouter ce livre ? (Y/N) : ") == "Y":
            db.mkRequest("insertLivre", False, ISBN, Titre, Auteur[0], Description, Note, DateDeParution, Statut)
            db.db.commit()
            print("Livre ajouté avec succès !")
        else :
            print("Opération annulée.")
    except Exception as e:
        print(f"Une erreur est survenue lors de l'ajout du livre :{e}, ligne : {e.__traceback__.tb_lineno}")
    


    

def addAuthor():
    return