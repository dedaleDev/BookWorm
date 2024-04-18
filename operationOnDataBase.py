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
                return None
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
                try : 
                    if len(answer) !=3 or int(answer[2]) < 0 or int(answer[2]) > 31 or int(answer[1]) < 0 or int(answer[1]) > 12 or int(answer[0]) < 0 or int(answer[0]) > 2100:
                        print(f"{content} doit être une date valide. Veuillez réessayer.")
                    else :
                        return f"{answer[0]}-{answer[1]}-{answer[2]}"
                except :
                    print(f"{content} doit être une date valide attendu JJ/MM/AAAA. Veuillez réessayer.") 
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
            print("Désolé, l'entrée saisie est incorrect. Veuillez réessayer.")
            #print("Désolé, le format de la réponse est incorrect. Veuillez réessayer.", answer, e, e.__traceback__.tb_lineno)

def addAuteur(db:database.db):
    try :
        print("\n------------Nouvel auteur-----------\n")
        Nom = getAnswer("Entrez le nom de l'auteur : ", "str", "Le nom de l'auteur", 1, 20)
        if Nom == None: return
        Prenom = getAnswer("Entrez le prénom de l'auteur : ", "str", "Le prénom de l'auteur", 1, 20)
        if Prenom == None: return
        Alias = getAnswer("Entrez l'alias de l'auteur (facultatif) : ", "str", "L'alias de l'auteur", 0, 20, canBeNull=True)
        Biographie = getAnswer("Entrez la biographie de l'auteur : ", "str", "La biographie de l'auteur", 0, 1000)
        if Biographie == None: return
        DateDeNaissance = getAnswer("Entrez la date de naissance de l'auteur (attendu JJ/MM/AAAA): ", "date", "La date de naissance de l'auteur")
        if DateDeNaissance == None: return
        DateDeDeces = getAnswer("Entrez la date de décès de l'auteur (facultatif, attendu JJ/MM/AAAA): ", "date", "La date de décès de l'auteur", canBeNull=True)
        print("\n------------Recapitulatif-----------\n")
        if Alias == "Null":
            print(f"Nom : {Nom}\nPrenom : {Prenom}\nBiographie : {Biographie}\nDate de naissance : {DateDeNaissance}\nDate de décès : {DateDeDeces}")
        else :
            print(f"Nom : {Nom}\nPrenom : {Prenom}\nAlias : {Alias}\nBiographie : {Biographie}\nDate de naissance : {DateDeNaissance}\nDate de décès : {DateDeDeces}")
        if input("Voulez-vous ajouter cet auteur ? (Y/N) : ") == "Y":
            db.mkRequest("insertAuteur", False, Nom, Prenom, Biographie, DateDeNaissance, DateDeDeces,Alias)
            db.db.commit()
            print("Auteur ajouté avec succès !")
    except Exception as e:
        print(f"Une erreur est survenue lors de l'ajout de l'auteur :{e}, ligne : {e.__traceback__.tb_lineno}")

def addEditeur(db:database.db):
    try :
        print("\n------------Nouvel éditeur-----------\n")
        while True :
            Nom = getAnswer("Entrez le nom de l'éditeur : ", "str", "Le nom de l'éditeur", 1, 20)
            db.mkRequest("selectEditeurByNom", False, Nom)
            if db.cursor.fetchall() == ():
                break
            print("Désolé, mais un éditeur avec ce nom existe déjà. Veuillez réessayer.")
        if Nom == None: return
        Adresse = getAnswer("Entrez l'adresse de l'éditeur : ", "str", "L'adresse de l'éditeur", 1, 120)
        if Adresse == None: return
        print("\n------------Recapitulatif-----------\n")
        print(f"Nom : {Nom}\nAdresse : {Adresse}")
        if input("Voulez-vous ajouter cet éditeur ? (Y/N) : ") == "Y":
            db.mkRequest("insertEditeur", False, Nom, Adresse)
            db.db.commit()
            print("Editeur ajouté avec succès !")
    except Exception as e:
        print(f"Une erreur est survenue lors de l'ajout de l'éditeur :{e}, ligne : {e.__traceback__.tb_lineno}")

def addPointDeVente(db:database.db):
    try :
        print("\n------------Nouveau point de vente-----------\n")
        while True :
            Adresse = getAnswer("Entrez l'adresse du point de vente : ", "str", "L'adresse du point de vente", 1, 120)
            db.mkRequest("selectPointDeVenteByAdresse", False, Adresse)
            if db.cursor.fetchall() == ():
                break
            print("Désolé, mais un point de vente avec cette adresse existe déjà. Veuillez réessayer.")
        if Adresse == None: return
        Nom = getAnswer("Entrez le nom du point de vente : ", "str", "Le nom du point de vente", 1, 20)
        if Nom == None: return
        SiteWeb = getAnswer("Entrez le site web du point de vente : ", "str", "Le site web du point de vente", 1, 50)
        if SiteWeb == None: return
        Telephone = getAnswer("Entrez le numéro de téléphone du point de vente : ", "str", "Le numéro de téléphone du point de vente", 10, 10)
        if Telephone == None: return
        print("\n------------Recapitulatif-----------\n")
        print(f"Nom : {Nom}\nAdresse : {Adresse}\nSite web : {SiteWeb}\nTéléphone : {Telephone}")
        if input("Voulez-vous ajouter ce point de vente ? (Y/N) : ") == "Y":
            db.mkRequest("insertPointDeVente", False, Adresse, Nom, SiteWeb, Telephone)
            db.db.commit()
            print("Point de vente ajouté avec succès !")
    except Exception as e:
        print(f"Une erreur est survenue lors de l'ajout du point de vente :{e}, ligne : {e.__traceback__.tb_lineno}")


def addLivre(db:database.db):
    try : 
        print("\n------------Nouveau livre-----------\n")
        while True :
            ISBN = getAnswer("Entrez le code ISBN du livre : ", "str","Le code ISBN", 10, 13,)
            #verification de la clé primaire :
            db.mkRequest("selectLivreByISBN", False, ISBN)
            if db.cursor.fetchall() == ():
                break
            print("Désolé, mais un livre avec ce code ISBN existe déjà. Veuillez réessayer.")
        if ISBN == None: return
        Titre = getAnswer("Entrez le titre du livre : ", "str","Le titre du livre", 1, 50)
        if Titre == None: return
        while True :
            Auteur = getAnswer("Entrez le nom, prénom ou l'alias de l'auteur : ", "str", "L'auteur", 1, 50)
            if Auteur == None: return
            try :
                Auteur = searchEngine.searchAuteur(Auteur, db, True)[0]
                break
            except :
                print("Désolé, mais aucun auteur n'a été trouvé pour ce livre.")#proposer d'en ajouter
                saisie = input("Voulez-vous ajouter un auteur ? (Y / N / R (relancer la recherche)) : ")
                if saisie == "Y":
                    addAuteur(db)
                    continue
                elif saisie == "R":
                    continue
                else :
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
        while True :
            PointDeVente = getAnswer("Entrez le nom du point de vente du livre : ", "str", "Le point de vente", 1, 50)
            if PointDeVente == None: return
            try :
                PointDeVente = searchEngine.searchPointDeVente(PointDeVente, db, True)[0]
                break
            except :
                print("Désolé, mais aucun point de vente n'a été trouvé pour ce livre.")
                saisie = input("Voulez-vous ajouter un point de vente ? (Y / N / R (relancer la recherche)) : ")
                if saisie == "Y":
                    addPointDeVente(db)
                    continue
                elif saisie == "R":
                    continue
                else :
                    return
        print(f"Vous avez selectionné le point de vente : {PointDeVente[1]}")
        while True :
            Editeur = getAnswer("Entrez le nom de l'éditeur du livre : ", "str", "L'éditeur", 1, 50)
            if Editeur == None: return
            try :
                Editeur = searchEngine.searchEditeur(Editeur, db, True)[0]
                break
            except :
                print("Désolé, mais aucun éditeur n'a été trouvé pour ce livre.")
                saisie = input("Voulez-vous ajouter un éditeur ? (Y / N / R (relancer la recherche)) : ")
                if saisie == "Y":
                    addEditeur(db)
                    continue
                elif saisie == "R":
                    continue
                else :
                    return
        print(f"Vous avez selectionné l'éditeur : {Editeur[0]}")
        print("\n------------Recapitulatif-----------\n")
        if Auteur[3] == None : 
            print(f"ISBN : {ISBN}\nTitre : {Titre}\nAuteur : {Auteur[2]}{Auteur[1]}\nDescription : {Description}\nNote : {Note}\nDate de parution : {DateDeParution}\nStatut : {Statut}\n Genre : {Genre}\nFormat : {Format}\nPrix : {Prix}\nPoint de vente : {PointDeVente[1]}\nEditeur : {Editeur[0]}")
        else :
            print(f"ISBN : {ISBN}\nTitre : {Titre}\nAuteur : {Auteur[3]}\nDescription : {Description}\nNote : {Note}\nDate de parution : {DateDeParution}\nStatut : {Statut}\n Genre : {Genre}\nFormat : {Format}\nPrix : {Prix}\nPoint de vente : {PointDeVente[1]}\nEditeur : {Editeur[0]}")
        if input("Voulez-vous ajouter ce livre ? (Y/N) : ") != "N":
            db.mkRequest("insertLivre", False, ISBN, Titre, Auteur[0], Description, Note, DateDeParution, Statut, Genre, Format, Prix, PointDeVente[0], Editeur[0])
            db.db.commit()
            print("Livre ajouté avec succès !")
        else :
            print("Opération annulée.")
    except Exception as e:
        print(f"Une erreur est survenue lors de l'ajout du livre :{e}, ligne : {e.__traceback__.tb_lineno}")

def addEmprunt(db:database.db):
    pass

def addUtilisateur(db:database.db):
    pass

def deleteLivre(db:database.db):
    pass

def deleteAuteur(db:database.db):
    pass

def deletePointDeVente(db:database.db):
    pass

def deleteEditeur(db:database.db):
    pass

def deleteEmprunt(db:database.db):
    pass

def deleteUtilisateur(db:database.db):
    pass

def editLivre(db:database.db):
    pass

def editAuteur(db:database.db):
    pass

def editPointDeVente(db:database.db):
    pass

def editEditeur(db:database.db):
    pass

def editEmprunt(db:database.db):
    pass

def editUtilisateur(db:database.db):
    pass


def getAuteurNameByID(db:database.db, id:int)->str:
    try :
        db.mkRequest("selectAuteurByID", False, id)
        result = db.cursor.fetchall()
        if result == None or result == []: return "Auteur inconnu"
        if result[0][6] != None:
            return f"{result[0][6]}"
        return f"{result[0][2]} {result[0][1]}"
    except Exception as e:
        print(f"Une erreur est survenue lors de la recherche de l'auteur :{e}, ligne : {e.__traceback__.tb_lineno}")


def searchAuteur(db:database.db):
    try: 
        nomPrenomAlias = getAnswer("Rechercher un auteur : ", "str", "L'auteur", 1, 50)
        if nomPrenomAlias == None: return
        result = searchEngine.searchAuteur(nomPrenomAlias, db)
        if result == None: 
            print("Oups, aucun auteur n'a été trouvé pour cette recherche.")
            if input("Voulez-vous lancer une nouvelle recherche ? (Y/N) : ") == "Y":
                searchAuteur(db)
            return
        print(result)
        print(f"Résultat de la recherche pour '{nomPrenomAlias}' :\n")
        for i in range(len(result)) : 
            print("------------------------------------")
            if result[i][6] != None: 
                print(f"{i+1} : {result[i][2]} {result[i][1]} alias : {result[i][6]}")
            else :
                print(f"{i+1} : {result[i][2]} {result[i][1]}")
            if result[i][4] != "0000-00-00":
                print(f"Né le : {result[i][4]}")
            if result[i][5] != "0000-00-00" and result[i][5] != None:
                print(f"Décédé le : {result[i][5]}")
            print(f"Biographie : {result[i][3].replace('\n', '')}")
        input("Appuyez sur entrée pour continuer...")
    except Exception as e:
        print(f"Une erreur est survenue lors de la recherche du point de vente :{e}, ligne : {e.__traceback__.tb_lineno}")

def searchLivre(db:database.db, recherche:str = None):
    try :
        if recherche == None:
            recherche = getAnswer("Rechercher un livre : ", "str", "Le livre", 1, 50)
        if recherche == None: return
        result = searchEngine.searchLivre(recherche, db)
        if result == None: 
            print("Oups, aucun livre n'a été trouvé pour cette recherche.")
            if input("Voulez-vous lancer une nouvelle recherche ? (Y/N) : ") == "Y":
                searchLivre(db)
            return
        print(f"Résultat de la recherche pour '{recherche}' :\n")
        for i in range(len(result)) : 
            print(f"------------------------------------")
            print(f"{result[i][1].replace('\n', '')}\nISBN : {result[i][0]}\nAuteur: {getAuteurNameByID(db, result[i][2])}\nDescription : {result[i][3].replace('\n', '')}\nNote : {result[i][4]:.1f}/10\nDate de parution : {result[i][5]}\nStatut : {result[i][6]}\nGenre : {result[i][7]}\nFormat : {result[i][8]}\nPrix : {result[i][9]:.2f}\nPoint de vente : {result[i][10].replace('\n','')}\nEditeur : {result[i][11]}")
        input("Appuyez sur entrée pour continuer...")
    except Exception as e :
        print("Une erreur est survenue lors de la recherche du livre.", e, e.__traceback__.tb_lineno)

def searchPointDeVente(db:database.db):
    try :
        nom = getAnswer("Rechercher un point de vente : ", "str", "Le point de vente", 1, 50)
        if nom == None: return
        result = searchEngine.searchPointDeVente(nom, db)
        if result == None: 
            print("Oups, aucun point de vente n'a été trouvé pour cette recherche.")
            if input("Voulez-vous lancer une nouvelle recherche ? (Y/N) : ") == "Y":
                searchPointDeVente(db)
            return
        print(f"Résultat de la recherche pour '{nom}' :\n")
        for i in range(len(result)) : 
            print(f"------------------------------------")
            print(f"{result[i][1]}\nAdresse : {result[i][0].replace('\n', '')}\nSite web : {result[i][2]}\nTéléphone : {result[i][3]}")
        input("Appuyez sur entrée pour continuer...")
    except Exception as e:
        print(f"Une erreur est survenue lors de la recherche du point de vente :{e}, ligne : {e.__traceback__.tb_lineno}")

def searchEditeur(db:database.db):
    try :
        nom = getAnswer("Rechercher un éditeur : ", "str", "L'éditeur", 1, 50)
        if nom == None: return
        result = searchEngine.searchEditeur(nom, db)
        if result == None: 
            print("Oups, aucun éditeur n'a été trouvé pour cette recherche.")
            if input("Voulez-vous lancer une nouvelle recherche ? (Y/N) : ") == "Y":
                searchEditeur(db)
            return
        print(f"Résultat de la recherche pour '{nom}' :\n")
        for i in range(len(result)) : 
            print(f"------------------------------------")
            print(f"{result[i][0]}\nAdresse : {result[i][1].replace('\n', '')}")
        input("Appuyez sur entrée pour continuer...")
    except Exception as e:
        print(f"Une erreur est survenue lors de la recherche de l'éditeur :{e}, ligne : {e.__traceback__.tb_lineno}")


def showEmprunts(db:database.db):
    pass

def showUtilisateurs(db:database.db):
    pass
