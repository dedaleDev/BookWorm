import database, searchEngine

def unformatDate(date)->str:
    """ This function formats a date in the format "aaaa-mm-jj" to the format "jj/mm/aaaa".
        Args :
            date : str, date in the format "aaaa-mm-jj"
        Return :
            date : str, date in the format "jj/mm/aaaa"
    """
    try : 
        #obtenir une str de la date
        result = date.strftime("%Y-%m-%d").split('-')
        result.reverse()
        return f"{result[0]}/{result[1]}/{result[2]}"
    except :
        return date

def filterLivreByAuteur(livres:list[tuple], auteur:str,db:database.db)-> list:
    """ This function filters the books by author.
    Args : 
        livres (list): The list of books.
        auteur (str): The author.
        db (database.db): The database object.
    Returns:
        list: The filtered list of books."""
    try : 
        result = []
        for i in range(len(livres)):
            if searchEngine.getAuteurNameByID(db,livres[i][2]) == auteur:
                result.append(livres[i])
        return result
    except Exception as e:
        print(f"\033[31m Une erreur est survenue lors du filtrage des livres par auteur :{e}, ligne : {e.__traceback__.tb_lineno}\033[0m")
        return livres

def sortLivre(livres:list, operation:str)-> list:
    """ This function sorts the books.
    Args:
        livres (list): The list of books.
        operation (str): The operation to perform.
    Returns:
        list: The sorted list of books.
    """
    try :
        if operation == "sortByPertinence" :
            return livres
        if operation == "sortByNote":
            livres.sort(key=lambda x: x[4], reverse=True)
        elif operation == "sortByAlpha":
            livres.sort(key=lambda x: x[1])
        elif operation == "sortByDate":
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
                print(f"\033[31m Une erreur est survenue lors du tri par date de parution :{e}, ligne : {e.__traceback__.tb_lineno}\033[0m")
                pass
            except Exception as e:
                print(f"\033[31m Une erreur est survenue lors du tri par date de parution :{e}, ligne : {e.__traceback__.tb_lineno}\033[0m")
        elif operation == "sortByPrix":
            livres.sort(key=lambda x: x[9])
        return livres
    except Exception as e:
        print(f"\033[31m Une erreur est survenue lors du tri des livres :{e}, ligne : {e.__traceback__.tb_lineno}\033[0m")


def  getStatus(isbn:str, db:database.db):
    """ This function returns the status of a book
    Args  : isbn (str): The ISBN of the book.
            db (database.db): The database object.
    Returns : str : The status of the book."""
    try : 
        db.mkRequest("selectEmpruntByISBN", False, isbn)
        emprunt = db.cursor.fetchall()
        db.mkRequest("selectLivreByISBN", True, isbn)
        livre = db.cursor.fetchall()
        if livre != None:
            dbStatus = livre[0][6]
        if dbStatus == "hors stock": return "hors stock"
        elif  emprunt == None or emprunt ==[] or emprunt == (): return "disponible"
        else : return "emprunté"
    except Exception as e:
        print(f"\033[31m Une erreur est survenue lors de la recherche du status du livre :{e}, ligne : {e.__traceback__.tb_lineno}\033[0m")
        return None
    
def convertPointDeVenteToAcceptablePointDeVente(pointDeVente:str,db:database.db)->str:
    """ This function converts a pointDeVente to an acceptable pointDeVente. Use this to avoid errors sql errors.
    Args : pointDeVente (str): The point of sale.
           db (database.db): The database object.
    Returns : str : The acceptable point of sale."""
    try : 
        db.mkRequest("selectAllPointsDeVentes", False)
        pointDeVente = pointDeVente.replace(" ", "").replace("\n", "").replace("\r", "")
        pointsDeVentes = db.cursor.fetchall()
        for i in range(len(pointsDeVentes)):
            originPointDeVente = pointsDeVentes[i][0].replace(" ", "").replace("\n", "").replace("\r", "")
            if pointDeVente == originPointDeVente:
                return pointsDeVentes[i][0]
    except Exception as e:
        print(f"\033[31m Une erreur est survenue lors de la conversion du point de vente :{e}, ligne : {e.__traceback__.tb_lineno}\033[0m")
            
def getRealNote(isbn:str,db:database.db) -> float : 
    """ This function returns the real note of a book.
    Args : isbn (str): The ISBN of the book.
    Returns : float : The real note of the book."""
    try :
        db.mkRequest("selectNoteByISBN", False, isbn)
        notes = db.cursor.fetchall()
        moy = 0
        nbNotes = 0
        for note in notes : 
            print(note[3], isbn)
            if note[3] ==isbn: 
                moy += note[1]
                nbNotes+=1
        if nbNotes != 0:
            return moy/nbNotes
        else : 
            db.mkRequest("selectLivreByISBN", True, isbn)
            result = db.cursor.fetchall()
            return result[0][4]
    except Exception as e:
        print(f"\033[31m Une erreur est survenue lors de la recherche de la note réelle du livre :{e}, ligne : {e.__traceback__.tb_lineno}\033[0m")
        return 0