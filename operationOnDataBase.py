import database,searchEngine

def getAnswer(question:str, type:str, content:str, min_int:int=0, max_int:int=5, enum:list=[], canBeNull:bool = False)->str:
    """ This function asks the user a question and returns the answer in the correct format.
        Args :
            question : str, question to ask the user
            type : str, type of the answer expected (like "str", "int", "float", "enum", "date")
            content : str, content of the answer
            min_int : int, minimum value for an integer
            max_int : int, maximum value for an integer
            enum : list, list of possible values for an enum
            canBeNull : bool, if True, the answer can be null
        Return :
            answer : str, the answer in the correct format
    """
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
                    print(f"{content.capitalize()} doit être une valeur de la liste. Veuillez réessayer.")
            if type == "date":#DATE
                if '/' in answer:
                    answer = answer.replace('/', '-')
                answer = answer.split('-')
                answer.reverse()
                try : 
                    if len(answer) !=3 or int(answer[2]) <= 0 or int(answer[2]) > 31 or int(answer[1]) <= 0 or int(answer[1]) > 12 or int(answer[0]) <= 0 or int(answer[0]) > 2100:
                        print(f"{content.capitalize()} doit être une date valide (jj/mm/aaaa). Veuillez réessayer. Si vous ne connaissez pas la date exacte, entrez 1.")
                    else :
                        return f"{answer[0]}-{answer[1]}-{answer[2]}"
                except :
                    print(f"{content.capitalize()} doit être une date valide attendu jj/mm/aaaa. Veuillez réessayer.") 
            if type == "int":#INT
                print(answer)
                if answer.isdigit() and int(answer) >= min_int and int(answer) <= max_int:
                    return int(answer)
                else:
                    print(f"{content.capitalize()} doit être un nombre entier entre {str(min_int)} et {str(max_int) }. Veuillez réessayer.")
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
                    print(f"{content.capitalize()} doit être un nombre réel entre {str(min_int)} et {str(max_int)}. Veuillez réessayer.")
        except KeyboardInterrupt:
            return None
        except Exception as e:
            print("Désolé, l'entrée saisie est incorrect. Veuillez réessayer.")
            #print("Désolé, le format de la réponse est incorrect. Veuillez réessayer.", answer, e, e.__traceback__.tb_lineno)

def addAuteur(db:database.db):
    """ This function adds an author to the database."""
    try :
        print("\n---------Nouvel auteur--------\n")
        Nom = getAnswer("Entrez le nom de l'auteur : ", "str", "Le nom de l'auteur", 1, 20).capitalize()
        if Nom == None: return
        Prenom = getAnswer("Entrez le prénom de l'auteur : ", "str", "Le prénom de l'auteur", 1, 20).capitalize()
        if Prenom == None: return
        Alias = getAnswer("Entrez l'alias de l'auteur (facultatif) : ", "str", "L'alias de l'auteur", 0, 20, canBeNull=True).capitalize()
        Biographie = getAnswer("Entrez la biographie de l'auteur : ", "str", "La biographie de l'auteur", 0, 1000)
        if Biographie == None: return
        DateDeNaissance = getAnswer("Entrez la date de naissance de l'auteur (attendu jj/mm/aaaa): ", "date", "La date de naissance de l'auteur")
        if DateDeNaissance == None: return
        DateDeDeces = getAnswer("Entrez la date de décès de l'auteur (facultatif, attendu jj/mm/aaaa): ", "date", "La date de décès de l'auteur", canBeNull=True)
        print("\n----------Recapitulatif----------\n")
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
    """ This function adds an editor to the database."""
    try :
        print("\n---------Nouvel éditeur---------\n")
        while True :
            Nom = getAnswer("Entrez le nom de l'éditeur : ", "str", "Le nom de l'éditeur", 1, 20)
            db.mkRequest("selectEditeurByNom", False, Nom)
            if db.cursor.fetchall() == ():
                break
            print("Désolé, mais un éditeur avec ce nom existe déjà. Veuillez réessayer.")
        if Nom == None: return
        Adresse = getAnswer("Entrez l'adresse de l'éditeur : ", "str", "L'adresse de l'éditeur", 1, 120)
        if Adresse == None: return
        print("\n----------Recapitulatif---------\n")
        print(f"Nom : {Nom}\nAdresse : {Adresse}")
        if input("Voulez-vous ajouter cet éditeur ? (Y/N) : ") == "Y":
            db.mkRequest("insertEditeur", False, Nom, Adresse)
            db.db.commit()
            print("Editeur ajouté avec succès !")
    except Exception as e:
        print(f"Une erreur est survenue lors de l'ajout de l'éditeur :{e}, ligne : {e.__traceback__.tb_lineno}")

def addPointDeVente(db:database.db):
    """ This function adds a point of sale to the database."""
    try :
        print("\n---Nouveau point de vente---\n")
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
        print("\n----------Recapitulatif---------\n")
        print(f"Nom : {Nom}\nAdresse : {Adresse}\nSite web : {SiteWeb}\nTéléphone : {Telephone}")
        if input("Voulez-vous ajouter ce point de vente ? (Y/N) : ") == "Y":
            db.mkRequest("insertPointDeVente", False, Adresse, Nom, SiteWeb, Telephone)
            db.db.commit()
            print("Point de vente ajouté avec succès !")
    except Exception as e:
        print(f"Une erreur est survenue lors de l'ajout du point de vente :{e}, ligne : {e.__traceback__.tb_lineno}")


def addLivre(db:database.db):
    """ This function adds a book to the database."""
    try : 
        print("\n---------Nouveau livre--------\n")
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
            Auteur = getAnswer("Rechercher un auteur (Entrez N pour créer un nouvel auteur): ", "str", "L'auteur", 1, 50)
            if Auteur == None: return
            try :
                if Auteur == "N":
                    addAuteur(db)
                    continue
                Auteur = searchEngine.searchAuteur(Auteur, db, True)
                if Auteur == None:
                    print("Désolé, mais aucun auteur n'a été trouvé pour ce livre.")#proposer d'en ajouter
                    saisie = input("Voulez-vous ajouter un auteur ? (Y / N / R (relancer la recherche)) : ")
                    if saisie == "Y":
                        addAuteur(db)
                        continue
                    elif saisie == "R":
                        continue
                    else :
                        return
                else :
                    break
            except :
                print("Une erreur est survenue lors de la recherche de l'auteur. Veuillez réessayer.")
                return
        if len(Auteur) == 1:
            Auteur = list(Auteur[0])
        print(f"Vous avez selectionné l'auteur : {Auteur[2]} {Auteur[1]}")
        Description = getAnswer("Entrez une description pour le livre : ", "str", "La description", 0, 1000)
        if Description == None: return
        Note = getAnswer("Entrez la note initiale du livre (attendu 0-10) : ", "float", "la note", 0, 10)
        if Note == None: return
        DateDeParution = getAnswer("Entrez la date de parution du livre (attendu jj/mm/aaaa): ", "date", "La date de parution")
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
                PointDeVente = searchEngine.searchPointDeVente(PointDeVente, db, True)
                if len(PointDeVente) == 1:
                    PointDeVente = PointDeVente[0]
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
                Editeur = searchEngine.searchEditeur(Editeur, db, True)
                if len(Editeur) == 1:
                    Editeur = Editeur[0]
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

def deleteLivre(db:database.db):
    """ This function deletes a book from the database."""
    try :
        print("\n-----Supprimer un livre-----\n")
        recherche = getAnswer("Entrez le titre du livre à supprimer : ", "str", "Le titre du livre", 1, 50)
        if recherche == None: return
        livre = searchEngine.searchLivre(recherche, db, onlyOne=True)
        if len(livre) == 1:
            livre = livre[0]
        if livre == None: 
            print("Oups, aucun livre n'a été trouvé pour cette recherche.")
            return
        if input(f"Voulez vous vraiment effacer le livre : {livre[1]} (Y/N) ? ") == "Y":
            db.mkRequest("deleteLivre", False, livre[0])
            db.db.commit()
            print("Livre supprimé avec succès !")
    except Exception as e:
        print(f"Une erreur est survenue lors de la suppression du livre :{e}, ligne : {e.__traceback__.tb_lineno}")
    

def deleteAuteur(db:database.db):
    """ This function deletes an author from the database."""
    try :
        print("\n----Supprimer un auteur----\n")
        recherche = getAnswer("Rechercher un auteur à supprimer : ", "str", "L'auteur", 1, 50)
        if recherche == None: return
        auteur = searchEngine.searchAuteur(recherche, db, onlyOne=True)
        if len(auteur) == 1:
            auteur = auteur[0]
        if auteur == None: 
            print("Oups, aucun auteur n'a été trouvé pour cette recherche.")
            return
        print("Cette opération entrainera la suppression de tous les livres associés à cet auteur.")
        if input(f"Voulez vous vraiment effacer l'auteur : {auteur[2]} {auteur[1]} (Y/N) ? ") == "Y":
            db.mkRequest("deleteLivreByAuteur", False, auteur[0])
            db.mkRequest("deleteAuteur", False, auteur[0])
            db.db.commit()
            print("Auteur supprimé avec succès !")
    except Exception as e:
        print(f"Une erreur est survenue lors de la suppression de l'auteur :{e}, ligne : {e.__traceback__.tb_lineno}")

def deletePointDeVente(db:database.db):
    """This function deletes a point of sale from the database."""
    try :
        print("\n--Supprimer un point de vente--\n")
        recherche = getAnswer("Entrez le nom du point de vente à supprimer : ", "str", "Le point de vente", 1, 50)
        if recherche == None: return
        pointDeVente = searchEngine.searchPointDeVente(recherche, db, onlyOne=True)
        if len(pointDeVente) == 1:
            pointDeVente = pointDeVente[0]
        if pointDeVente == None:
            print("Oups, aucun point de vente n'a été trouvé pour cette recherche.")
            return
        print(f"Cette opération demande le remplacement du point de vente {pointDeVente} pour tous les livres associés.")
        recherche = getAnswer("Entrez le nom du point de vente de remplacement : ", "str", "Le point de vente", 1, 50)
        if recherche == None: return
        pointDeVenteRemplacement = searchEngine.searchPointDeVente(recherche, db, onlyOne=True)
        if len(pointDeVenteRemplacement) == 1:
            pointDeVenteRemplacement = pointDeVenteRemplacement[0]
        if pointDeVenteRemplacement == None:
            print("Oups, aucun point de vente n'a été trouvé pour cette recherche.")
            return
        if input(f"Confirmez vous le remplacement du point de vente {pointDeVente[1]} par {pointDeVenteRemplacement[1]} ? (Y/N) : ") != "Y":
            print("Opération annulée.")
            return
        db.mkRequest("updateLivrePointDeVente", False, pointDeVenteRemplacement[0], pointDeVente[0])
        db.mkRequest("deletePointDeVente", False, pointDeVente[0])
        db.db.commit()
        print("Point de vente supprimé avec succès !")
    except Exception as e:
        print(f"Une erreur est survenue lors de la suppression du point de vente :{e}, ligne : {e.__traceback__.tb_lineno}")

def deleteEditeur(db:database.db):
    """ This function deletes an editor from the database."""
    try :
        print("\n---Supprimer un éditeur--\n")
        recherche = getAnswer("Entrez le nom de l'éditeur à supprimer : ", "str", "L'éditeur", 1, 50)
        if recherche == None: return
        editeur = searchEngine.searchEditeur(recherche, db, onlyOne=True)
        if len(editeur) == 1:
            editeur = editeur[0]
        if editeur == None: 
            print("Oups, aucun éditeur n'a été trouvé pour cette recherche.")
            return
        print("Cette opération entrainera la suppression de tous les livres associés à cet éditeur.")
        if input(f"Voulez vous vraiment effacer l'éditeur : {editeur[0]} (Y/N) ? ") == "Y":
            db.mkRequest("deleteLivreByEditeur", False, editeur[0])
            db.mkRequest("deleteEditeur", False, editeur[0])
            db.db.commit()
            print("Editeur supprimé avec succès !")
    except Exception as e:
        print(f"Une erreur est survenue lors de la suppression de l'éditeur :{e}, ligne : {e.__traceback__.tb_lineno}")

def editLivre(db:database.db):
    """ This function edits a book in the database."""
    try : 
        print("\n--------Editer un livre--------\n")
        recherche = getAnswer("Recherchez le livre à éditer : ", "str", "Le titre du livre", 1, 50)
        if recherche == None: return
        livre = searchEngine.searchLivre(recherche, db, onlyOne=True)
        if livre == None:
            print("Oups, aucun livre n'a été trouvé pour cette recherche.")
            return
        if len(livre) == 1:
            livre = list(livre[0])
        operation = [["ISBN"],["le titre","str", 1, 50],["l'auteur","str", 1, 50],["la description","str", 0, 1000],["la note","float", 0, 10],["la date de parution (jj/mm/aaaa)","date", 0, 10],["le statut","enum", ["Disponible", "Emprunté", "hors stock"]],["le genre","enum", ["Historique","Romantique","Policier","Science-fiction","Fantastique","Aventure","Biographique","Autobiographique","Épistolaire","Thriller","Tragédie","Drame","Absurde","Philosophique","Politique","Légendes & Mythes","Lettres personnelles","Voyages","Journal intime","Bandes dessinées","Documentaires","Religieux"]],["le format","enum", ["Poche","Grand Format","E-book & numérique","Manga","Bande Dessinée","Magazine","CD","DVD & Blu-ray"]],["le prix","float", 0, 1000],["le point de vente","str", 1, 50],["l'editeur","str", 1, 50],["quiter et sauvegarder (CTRL+C)"]]
        externalKeyOperation = {"l'auteur":searchEngine.searchAuteur,"le point de vente":searchEngine.searchPointDeVente,"l'editeur":searchEngine.searchEditeur}    
        print(f"Vous avez selectionné le livre : {livre[1]}")
        print("Veuillez noter qu'il n'est pas possible d'éditer le code ISBN. Si cela est nécessaire, veuillez supprimer le livre et en ajouter un nouveau.")
        print("Que voulez-vous modifier ?")
        while True :
            for i in range(len(operation)):
                if i != 0 : #n'affiche pas la clé primaire car pas modifiable
                    print(f"{i} : {operation[i][0].capitalize()}")
            try :
                saisie = int(input("Veuillez saisir le numéro de l'élément à modifier :"))
                if saisie == 12:
                    saisie = input("Voulez-vous appliquer les modifications ? (Y / N) : ")
                    if  saisie == "Y":
                        db.mkRequest("updateLivre", False,livre[1], livre[2], livre[3], livre[4], livre[5], livre[6], livre[7], livre[8], livre[9], livre[10], livre[11], livre[0])
                        db.db.commit()
                        print("Livre modifié avec succès !")
                        return
                    elif saisie == "N":
                        print("Opération annulée.")
                        return
                    else :
                        continue
            except KeyboardInterrupt:
                return
            except :
                print("Désolé, le format de la réponse est incorrect. Veuillez réessayer.")
            print(saisie)
            if  int(saisie) >= 1 and int(saisie) <= len(operation)-1:
                for i in range(len(operation)):
                    if i == saisie and i != 0:
                        if operation[i][0] in externalKeyOperation.keys():
                            saisie = input(f"Entre la nouvelle valeur pour {operation[i][0]} : ")
                            change = externalKeyOperation[operation[i][0]](saisie, db, True)
                            if change == None:
                                print("Oups, aucun élément n'a été trouvé pour cette recherche.")
                                continue
                            if len(change) == 1:
                                change = change[0]
                            if change == None:
                                print("Oups, aucun élément n'a été trouvé pour cette recherche.")
                                continue
                            if operation[i][0] == "auteur":
                                print("Vous avez selectionné : ", change[2], change[1])
                            else :
                                print("Vous avez selectionné : ", change[1])
                            change = change[0]
                        elif len(operation[i]) == 4:
                            change = getAnswer(f"Entrez {operation[i][0]} : ", operation[i][1], operation[i][0], operation[i][2], operation[i][3])
                        else :
                            change = getAnswer(f"Entrez {operation[i][0]} : ", operation[i][1], operation[i][0], enum = operation[i][2])
                        if change == None: return
                        livre = [change if j == i else livre[j] for j in range(len(livre))]
                        print(livre)
                        saisie = input("Voulez-vous appliquer les modifications ? (Y / N / P (poursuivre modifications)) : ")
                        if  saisie == "Y":
                            db.mkRequest("updateLivre", False,livre[1], livre[2], livre[3], livre[4], livre[5], livre[6], livre[7], livre[8], livre[9], livre[10], livre[11], livre[0])
                            db.db.commit()
                            print("Livre modifié avec succès !")
                            return
                        elif saisie == "N":
                            print("Opération annulée.")
                            return
                        else :
                            continue
            else:
                print("Désolé, le format de la réponse est incorrect. Veuillez réessayer.")
    except Exception as e:  
        print(f"Une erreur est survenue lors de l'édition du livre :{e}, ligne : {e.__traceback__.tb_lineno}")

def editAuteur(db:database.db):
    """ This function edits an author in the database."""
    try :
        print("\n--------Editer un auteur--------\n")
        recherche = getAnswer("Recherchez l'auteur à éditer : ", "str", "L'auteur", 1, 50)
        if recherche == None: return
        auteur = searchEngine.searchAuteur(recherche, db, True)
        if auteur == None:
            print("Oups, aucun auteur n'a été trouvé pour cette recherche.")
            return
        if len(auteur) == 1:
            auteur = list(auteur[0])
        operation = [["l'id"],["le nom","str", 1, 20],["le prénom","str", 1, 20],["la biographie","str", 0, 1000],["la date de naissance (jj/mm/aaaa)","date", 0, 10],["la date de décès (jj/mm/aaaa)","date", 0, 10, None],["l'alias","str", 0, 20,None],["quiter et sauvegarder (CTRL+C)"]]
        print(f"Vous avez selectionné l'auteur : {auteur[2]} {auteur[1]}")
        print("Que voulez-vous modifier ?")
        while True :
            for i in range(len(operation)):
                if i != 0 : #n'affiche pas la clé primaire car pas modifiable
                    print(f"{i} : {operation[i][0].capitalize()}")
            try :
                saisie = int(input("Veuillez saisir le numéro de l'élément à modifier :"))
            except KeyboardInterrupt:
                return
            except :
                print("Désolé, le format de la réponse est incorrect. Veuillez réessayer.")
            if  int(saisie) >= 1 and int(saisie) <= len(operation)-1:
                if saisie == 7 :
                    saisie = input("Voulez-vous appliquer les modifications ? (Y / N) : ")
                    if  saisie == "Y":
                        db.mkRequest("updateAuteur", False,auteur[1], auteur[2], auteur[3], auteur[4], auteur[5],auteur[6], auteur[0])
                        db.db.commit()
                        print("Auteur modifié avec succès !")
                        return
                    elif saisie == "N":
                        print("Opération annulée.")
                        return
                    else :
                        continue
                for i in range(len(operation)):
                    if i == saisie and i != 0:
                        if len(operation[i]) == 5:
                                change = getAnswer(f"Entrez {operation[i][0]} : ", operation[i][1], operation[i][0], operation[i][2], operation[i][3], canBeNull=True)
                        else :
                            change = getAnswer(f"Entrez {operation[i][0]} : ", operation[i][1], operation[i][0], operation[i][2], operation[i][3])
                        auteur = [change if j == i else auteur[j] for j in range(len(auteur))]
                        print(auteur)
                        saisie = input("Voulez-vous appliquer les modifications ? (Y / N / P (poursuivre modifications)) : ")
                        if  saisie == "Y":
                            db.mkRequest("updateAuteur", False,auteur[1], auteur[2], auteur[3], auteur[4], auteur[5],auteur[6], auteur[0])
                            db.db.commit()
                            print("Auteur modifié avec succès !")
                            return
                        elif saisie == "N":
                            print("Opération annulée.")
                            return
                        else :
                            continue
            else:
                print("Désolé, le format de la réponse est incorrect. Veuillez réessayer.")
    except Exception as e:
        print(f"Une erreur est survenue lors de l'édition de l'auteur :{e}, ligne : {e.__traceback__.tb_lineno}")


def editPointDeVente(db:database.db):
    """ This function edits a point of sale in the database."""
    try  :
        print("\n----Editer un point de vente----\n")
        recherche = getAnswer("Recherchez le point de vente à éditer : ", "str", "Le point de vente", 1, 50)
        if recherche == None: return
        pointDeVente = searchEngine.searchPointDeVente(recherche, db, True)
        if pointDeVente == None:
            print("Oups, aucun point de vente n'a été trouvé pour cette recherche.")
            return
        if len(pointDeVente) == 1:
            pointDeVente = list(pointDeVente[0])
        operation = [["l'adresse"],["le nom","str", 1, 20],["le site web","str", 1, 50],["le numéro de téléphone","str", 10, 10, None],["quiter et sauvegarder (CTRL+C)"]]
        print(f"Vous avez selectionné le point de vente : {pointDeVente[1]}")
        print("Veuillez noter qu'il n'est pas possible d'éditer l'adresse. Si cela est nécessaire, veuillez supprimer le point de vente et en ajouter un nouveau.")
        print("Que voulez-vous modifier ?")
        while True :
            for i in range(len(operation)):
                if i != 0 : #n'affiche pas la clé primaire car pas modifiable
                    print(f"{i} : {operation[i][0].capitalize()}")
            try :
                saisie = int(input("Veuillez saisir le numéro de l'élément à modifier :"))
                if saisie == 4:
                    saisie = input("Voulez-vous appliquer les modifications ? (Y / N) : ")
                    if  saisie == "Y":
                        db.mkRequest("updatePointDeVente", False,pointDeVente[1], pointDeVente[2], pointDeVente[3], pointDeVente[0])
                        db.db.commit()
                        print("Point de vente modifié avec succès !")
                        return
                    elif saisie == "N":
                        print("Opération annulée.")
                        return
                    else :
                        continue
            except KeyboardInterrupt:
                return
            except :
                print("Désolé, le format de la réponse est incorrect. Veuillez réessayer.")
            if  int(saisie) >= 1 and int(saisie) <= len(operation)-1:
                for i in range(len(operation)):
                    if i == saisie and i != 0:
                        if len(operation[i]) == 5:
                                change = getAnswer(f"Entrez {operation[i][0]} : ", operation[i][1], operation[i][0], operation[i][2], operation[i][3], canBeNull=True)
                        else :
                            change = getAnswer(f"Entrez {operation[i][0]} : ", operation[i][1], operation[i][0], operation[i][2], operation[i][3])
                        pointDeVente = [change if j == i else pointDeVente[j] for j in range(len(pointDeVente))]
                        print(pointDeVente)
                        saisie = input("Voulez-vous appliquer les modifications ? (Y / N / P (poursuivre modifications)) : ")
                        if  saisie == "Y":
                            db.mkRequest("updatePointDeVente", False,pointDeVente[1], pointDeVente[2], pointDeVente[3], pointDeVente[0])
                            db.db.commit()
                            print("Point de vente modifié avec succès !")
                            return
                        elif saisie == "N":
                            print("Opération annulée.")
                            return
                        else :
                            continue
            else:
                print("Désolé, le format de la réponse est incorrect. Veuillez réessayer.")
    except Exception as e:
        print(f"Une erreur est survenue lors de l'édition du point de vente :{e}, ligne : {e.__traceback__.tb_lineno}")

def editEditeur(db:database.db):
    """ This function edits an editor in the database."""
    try : 
        print("\n----Editer un éditeur----\n")
        recherche = getAnswer("Recherchez l'éditeur à éditer : ", "str", "L'éditeur", 1, 50)
        if recherche == None: return
        editeur = searchEngine.searchEditeur(recherche, db, True)
        if editeur == None:
            print("Oups, aucun éditeur n'a été trouvé pour cette recherche.")
            return
        if len(editeur) == 1:
            editeur = list(editeur[0])
        operation = [["le nom"],["l'adresse","str", 1, 120],["quiter et sauvegarder (CTRL+C)"]]
        print(f"Vous avez selectionné l'éditeur : {editeur[0]}")
        print("Veuillez noter qu'il n'est pas possible d'éditer le nom. Si cela est nécessaire, veuillez supprimer l'éditeur et en ajouter un nouveau.")
        print("Que voulez-vous modifier ?")
        while True :
            for i in range(len(operation)):
                if i != 0 : #n'affiche pas la clé primaire car pas modifiable
                    print(f"{i} : {operation[i][0].capitalize()}")
            try :
                saisie = int(input("Veuillez saisir le numéro de l'élément à modifier :"))
                if saisie == 2:
                    saisie = input("Voulez-vous appliquer les modifications ? (Y / N) : ")
                    if  saisie == "Y":
                        db.mkRequest("updateEditeur", False,editeur[1], editeur[0])
                        db.db.commit()
                        print("Editeur modifié avec succès !")
                        return
                    elif saisie == "N":
                        print("Opération annulée.")
                        return
                    else :
                        continue
            except KeyboardInterrupt:
                return
            except :
                print("Désolé, le format de la réponse est incorrect. Veuillez réessayer.")
            if  int(saisie) >= 1 and int(saisie) <= len(operation)-1:
                for i in range(len(operation)):
                    if i == saisie and i != 0:
                        change = getAnswer(f"Entrez {operation[i][0]} : ", operation[i][1], operation[i][0], operation[i][2], operation[i][3])
                        editeur = [change if j == i else editeur[j] for j in range(len(editeur))]
                        print(editeur)
                        saisie = input("Voulez-vous appliquer les modifications ? (Y / N / P (poursuivre modifications)) : ")
                        if  saisie == "Y":
                            db.mkRequest("updateEditeur", False,editeur[1], editeur[0])
                            db.db.commit()
                            print("Editeur modifié avec succès !")
                            return
                        elif saisie == "N":
                            print("Opération annulée.")
                            return
                        else :
                            continue
            else:
                print("Désolé, le format de la réponse est incorrect. Veuillez réessayer.")
    except Exception as e:
        print(f"Une erreur est survenue lors de l'édition de l'éditeur :{e}, ligne : {e.__traceback__.tb_lineno}")

def searchAuteur(db:database.db):
    """ This function searches for an author in the database."""
    try: 
        nomPrenomAlias = getAnswer("Rechercher un auteur : ", "str", "L'auteur", 1, 50)
        if nomPrenomAlias == None: return
        result = searchEngine.searchAuteur(nomPrenomAlias, db)
        if result == None: 
            print("Oups, aucun auteur n'a été trouvé pour cette recherche.")
            if input("Voulez-vous lancer une nouvelle recherche ? (Y/N) : ") == "Y":
                searchAuteur(db)
            return
        print(f"Résultat de la recherche pour '{nomPrenomAlias}' :\n")
        for i in range(len(result)) : 
            print("-----------------------------------")
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

def filterLivre(livres:list, operation:str,db:database.db)-> list:
    """ This function filters the books.
    Args:
        livres (list): The list of books.
        operation (str): The operation to perform.
        db (database.db): The database object.
    Returns:
        list: The filtered list of books.
    """
    try :
        result = []
        if operation == "auteur":
            recherche = getAnswer("Saisir un auteur pour appliquer le filtre :", "str", "L'auteur", 1, 50)
            if recherche == None: return None
            auteur = searchEngine.searchAuteur(recherche, db, onlyOne=True)
            if result == None: 
                print("Oups, aucun auteur n'a été trouvé pour cette recherche. Par conséquent, aucun filtre n'a été appliqué.")
                return None
            if len(auteur) == 1:
                auteur = auteur[0]         
            for i in range(len(livres)):
                if livres[i][2] == auteur[0]:
                    result.append(livres[i])
        elif operation == "genre":
            recherche = getAnswer("Saisir un genre pour appliquer le filtre :", "enum", "Le genre",enum=["Historique","Romantique","Policier","Science-fiction","Fantastique","Aventure","Biographique","Autobiographique","Épistolaire","Thriller","Tragédie","Drame","Absurde","Philosophique","Politique","Légendes & Mythes","Lettres personnelles","Voyages","Journal intime","Bandes dessinées","Documentaires","Religieux"])
            if recherche == None: return None
            for i in range(len(livres)):
                if livres[i][7] == recherche:
                    result.append(livres[i])
        elif operation == "format":
            recherche = getAnswer("Saisir un format pour appliquer le filtre :", "enum", "Le format",  enum = ["Poche","Grand Format","E-book & numérique","Manga","Bande Dessinée","Magazine","CD","DVD & Blu-ray"])
            if recherche == None: return None
            for i in range(len(livres)):
                if livres[i][8] == recherche:
                    result.append(livres[i])
        elif operation == "statut":
            recherche = getAnswer("Saisir un statut pour appliquer le filtre :", "enum", "Le statut", enum = ["Disponible", "Emprunté", "hors stock"])
            if recherche == None: return None
            for i in range(len(livres)):
                if livres[i][6] == recherche:
                    result.append(livres[i])
        elif operation == "éditeur":
            recherche = getAnswer("Saisir un éditeur pour appliquer le filtre :", "str", "L'éditeur", 1, 50)
            if recherche == None: return None
            editeur = searchEngine.searchEditeur(recherche, db, onlyOne=True)
            if result == None: 
                print("Oups, aucun éditeur n'a été trouvé pour cette recherche. Par conséquent, aucun filtre n'a été appliqué.")
                return None
            if len(editeur) == 1:
                editeur = editeur[0]
            for i in range(len(livres)):
                if livres[i][11] == editeur[0]:
                    result.append(livres[i])
        return result
    except Exception as e:
        print(f"Une erreur est survenue lors du filtrage des livres :{e}, ligne : {e.__traceback__.tb_lineno}")

def sortLivre(livres:list, operation:str)-> list:
    """ This function sorts the books.
    Args:
        livres (list): The list of books.
        operation (str): The operation to perform.
    Returns:
        list: The sorted list of books.
    """
    try :
        if operation == "note":
            print("Tri par note")
            livres.sort(key=lambda x: x[4], reverse=True)
        elif operation == "ordre alphabétique":
            print("Tri par ordre alphabétique")
            livres.sort(key=lambda x: x[1])
        elif operation == "date de parution":
            print("Tri par date de parution")
            #algo de tri sans utiliser sort : 
            try :
                for i in range(len(livres)):
                    for j in range(i+1, len(livres)):
                        if int(str(livres[i][5]).split('-')[0]) > int(str(livres[j][5]).split('-')[0]) :#si l'année est plus grande
                            livres[i], livres[j] = livres[j], livres[i]
                        elif int(str(livres[i][5]).split('-')[0]) == int(str(livres[j][5]).split('-')[0]) :#si l'année est la même
                            if int(str(livres[i][5]).split('-')[1]) > int(str(livres[j][5]).split('-')[1]) :# mais que le mois est plus grand
                                livres[i], livres[j] = livres[j], livres[i]
                            elif int(str(livres[i][5]).split('-')[1]) == int(str(livres[j][5]).split('-')[1]) :#si le mois est le même
                                if int(str(livres[i][5]).split('-')[2]) > int(str(livres[j][5]).split('-')[2]) :#mais que le jour est plus grand
                                    livres[i], livres[j] = livres[j], livres[i]
                livres = livres[::-1]#on inverse la liste pour avoir le tri dans l'ordre croissant
            except ValueError as e:
                print(e, e.__traceback__.tb_lineno)
                pass
            except Exception as e:
                print(f"Une erreur est survenue lors du tri par date de parution :{e}, ligne : {e.__traceback__.tb_lineno}")
            print('Résultat du tri par date de parution :')
        elif operation == "prix":
            print("Tri par prix")
            livres.sort(key=lambda x: x[9])
        elif operation == "point de vente":
            print("Tri par point de vente")
            livres.sort(key=lambda x: x[10])
        return livres
    except Exception as e:
        print(f"Une erreur est survenue lors du tri des livres :{e}, ligne : {e.__traceback__.tb_lineno}")
                     
def searchLivre(db:database.db, recherche:str = None):
    """ This function searches for a book in the database.
    Args:
        db (database.db): The database object.
        recherche (str, optional): The book to search. Defaults to None.
    """
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
        filtre = ["Tout afficher","Filtrer par auteur", "Filtrer par genre","Filtrer par format", "Filtrer par statut", "Filtrer par éditeur"]
        sortResult = ["ordre alphabétique", "note", "date de parution", "prix", "point de vente"]
        if len(result) > 1:
            print(f"Plusieurs résultats ont été trouvés : comment souhaitez-vous procéder ?")
            print("1 : Tout afficher (par défaut)\n2 : Filtrer\n3 : Trier")
            entry = input("Veuillez saisir une opération : ").strip()
            if entry == "2":
                for i in range(len(filtre)):
                    print(f"{i+1} : {filtre[i]}")
                try :
                    entry = int(input("Veuillez saisir un filtre :").strip().split()[0])
                    if entry > 1 and entry <=6:
                        print(result)
                        result = filterLivre(result, filtre[entry-1].split()[2],db)
                        print(result)
                        if filterLivre == None:
                            print("Aucun filtre n'a été appliqué.")
                except :
                    pass
            elif entry == "3":
                for i in range(len(sortResult)):
                    print(f"{i+1} : Par {sortResult[i]}")
                try :
                    entry = int(input("Veuillez saisir un tri :").strip().split()[0])
                    if entry > 1 and entry <=5:
                        result = sortLivre(result, sortResult[entry-1])
                        if sortLivre == None:
                            print("Aucun tri n'a été appliqué.")
                except :
                    pass
        print(f"Résultat de la recherche pour '{recherche}' :\n")
        for i in range(len(result)) : 
            print(f"-----------------------------------")
            print(f"{result[i][1].replace('\n', '')}\nISBN : {result[i][0]}\nAuteur: {searchEngine.getAuteurNameByID(db, result[i][2])}\nDescription : {result[i][3].replace('\n', '')}\nNote : {result[i][4]:.1f}/10\nDate de parution : {result[i][5]}\nStatut : {result[i][6]}\nGenre : {result[i][7]}\nFormat : {result[i][8]}\nPrix : {result[i][9]:.2f}\nPoint de vente : {result[i][10].replace('\n','')}\nEditeur : {result[i][11]}")
        input("Appuyez sur entrée pour continuer...")
    except Exception as e :
        print("Une erreur est survenue lors de la recherche du livre.", e, e.__traceback__.tb_lineno)

def searchPointDeVente(db:database.db):
    """ This function searches for a point of sale in the database."""
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
            print(f"-----------------------------------")
            print(f"{result[i][1]}\nAdresse : {result[i][0].replace('\n', '')}\nSite web : {result[i][2]}\nTéléphone : {result[i][3]}")
        input("Appuyez sur entrée pour continuer...")
    except Exception as e:
        print(f"Une erreur est survenue lors de la recherche du point de vente :{e}, ligne : {e.__traceback__.tb_lineno}")

def searchEditeur(db:database.db):
    """ This function searches for an editor in the database."""
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
            print(f"-----------------------------------")
            print(f"{result[i][0]}\nAdresse : {result[i][1].replace('\n', '')}")
        input("Appuyez sur entrée pour continuer...")
    except Exception as e:
        print(f"Une erreur est survenue lors de la recherche de l'éditeur :{e}, ligne : {e.__traceback__.tb_lineno}")