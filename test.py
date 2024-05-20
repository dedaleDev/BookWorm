   @cherrypy.expose
    @cherrypy.tools.json_out()
    def newLivre(self, **params) :
        try : 
            email =  params.get("email")
            password = params.get("password")
            self.db.mkRequest("selectUserByEmail", False, email)
            user = self.db.cursor.fetchall()
            if user is not None and user != () and user != []:
                if user[0][1] == password:
                    if user[0][2] == "admin":
                        isbn = params.get("isbn")
                        titre = params.get("titre")
                        auteur = params.get("auteur")
                        description = params.get("description")
                        dateDeParution = params.get("dateParution")
                        note = params.get("note")
                        statut = params.get("statut")
                        genre = params.get("genre")
                        format = params.get("format")
                        prix = params.get("prix")
                        pointDeVente = params.get("pointDeVente")
                        editeur = params.get("editeur")
                        image = params.get("image")
                        print(isbn, titre, auteur, description, dateDeParution, statut, genre, format, prix, pointDeVente, editeur)
                        if isbn is not None and titre is not None and auteur is not None and description is not None and dateDeParution is not None and statut is not None and genre is not None and format is not None and prix is not None and pointDeVente is not None and editeur is not None:
                            self.db.mkRequest("selectLivreByISBN", False, isbn)
                            checkISBN = self.db.cursor.fetchall()
                            if  checkISBN != [] and checkISBN != ():
                                print("REFUSED", checkISBN)
                                return self.makeResponse(is_error=True, error_message="Un livre avec cet ISBN existe déjà")
                            print('.'+str(pointDeVente+'.'))
                            self.db.mkRequest("insertLivre", False, isbn, titre, auteur, description, note, dateDeParution, statut, genre, format, prix, str(pointDeVente), editeur)
                            self.db.db.commit()
                            try : 
                                upload_filename = isbn+".jpg"
                                upload_file_path = os.path.join("./www/img/livres", upload_filename)
                                print("UPLOADING IMAGE", upload_file_path)
                                #check if file exists if yes no upload security
                                if os.path.exists(upload_file_path) != False:
                                    print("REFUSED UPLOAD, FILE EXISTS")
                                    return self.makeResponse(is_error=True, error_message="Une image avec ce nom existe déjà")
                                with open(upload_file_path, 'wb') as out:
                                    while True:
                                        data = image.file.read(8192)
                                        if not data:
                                            break
                                        out.write(data)
                            except Exception as e:
                                print("\033[31mErreur lors de l'ajout de l'image : ",e, e.__traceback__.tb_lineno, "\033[0m")
                            print("ADDED NEW LIVRE")
                            return self.makeResponse(content="success")
                        return self.makeResponse(is_error=True, error_message="Les données envoyées sont incorrectes")
                    else:
                        return self.makeResponse(is_error=True, error_message="Vous n'êtes pas administrateur")
                else:
                    return self.makeResponse(is_error=True, error_message="Mot de passe incorrect")