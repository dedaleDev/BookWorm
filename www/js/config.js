const API_URL = 'http://192.168.1.20:8080'

_templateHeaderLivre = `<tr><th>ISBN</th><th>Titre</th><th>Auteur</th><th>Description</th><th>Date de parution</th><th>Statut</th><th>Genre</th><th>Format</th><th>Prix (€)</th><th>Point de vente</th><th>Editeur</th><th>Supprimer</th></tr>`
_templateLivre = `<tr><td><p style="font-size: 15px;">{{ isbn }}<p></td>
    <td><textarea maxlength="100" class="form-control">{{ titre }}</textarea></td>
    <td><select class="form-control" name="auteur">{{ allAuteur }}</select></td>
    <td><textarea maxlength="1000" class="form-control">{{ description }}</textarea></td>
    <td><input type="date" class="form-control" value="{{ dateDeParution }}"></td>
    <td><select class="form-control" name="status">{{ status }}</select></td>
    <td><select class="form-control"  name="genre">{{ genre }}</select></td>
    <td><select class="form-control"  name="format">{{ format }}"</select></td>
    <td  style="width: 6%"><input type="number" pattern="[0-9*]" class="form-control" value="{{ prix }}" min="0" max="500" ></td>
    <td style="width: 7%"><select class="form-control" name="pointDeVente">{{ pointDeVente }}</select></td>
    <td><select class="form-control"  name="editeur">{{ editeur }}</select></td>
    <td><button class="btn btn-danger" onclick="deleteLivre('{{ isbn }}')">Supprimer</button></td></tr>`

_templateHeaderAuteur = `<tr><th>ID</th><th>Nom</th><th>Prénom</th><th>Alias</th><th>Biographie</th><th>Date de naissance</th><th>Date de décès</th><th>Supprimer</th></tr>`
_templateAuteur = `<tr><td>{{ id }}</td>
    <td><input type="text" class="form-control" value="{{ nom }}" maxlength="20"></td>
    <td><input type="text" class="form-control" value="{{ prénom }}" maxlength="20"></td>
    <td><input type="text" class="form-control" value="{{ alias }}" maxlength="20"></td>
    <td><textarea maxlength="1000" class="form-control">{{ biographie }}</textarea></td>
    <td><input type="date" class="form-control" value="{{ dateDeNaissance }}"></td>
    <td><input type="date" class="form-control" value="{{ dateDeDécès }}"></td>
    <td><button class="btn btn-danger" onclick="deleteAuteur('{{ id }}')">Supprimer</button></td></tr>`

_templateHeaderPointDeVente = `<tr><th>Adresse</th><th>Nom</th><th>Site web</th><th>Téléphone</th><th>Supprimer</th></tr>`
_templatePointDeVente = `<tr><td>{{ adresse }}</td>
    <td><input type="text" class="form-control" value="{{ nom }}" maxlength="20"></td>
    <td><input type="text" class="form-control" value="{{ url }}" maxlength="50"></td>
    <td><input type="number"  pattern="[0-9*]class="form-control" value="{{ tel }}" maxlength="10"></td>
    <td><button class="btn btn-danger" onclick="deletePointDeVente('{{ adresse }}')">Supprimer</button></td></tr>`

_templateEltDropDown = `<option value="{{ elt }}">{{ elt }}</option>`

_templateHeaderEditeur = `<tr><th>Nom</th><th>Adresse</th><th>Supprimer</th></tr>`
_templateEditeur = `<tr><td>{{ nom }}</td>
    <td><input type="text" class="form-control" value="{{ adresse }}" maxlength="120"></td>
    <td><button class="btn btn-danger" onclick="deleteEditeur('{{ nom }}')">Supprimer</button></td></tr>`

_templateHeaderUser  = `<tr><th>Email</th><th>Mot de passe</th><th>Grade</th><th>Nom</th><th>Prénom</th><th>Adresse</th><th>Téléphone</th><th>Supprimer</th></tr>`
_templateUser = `<tr><td>{{ email }}</td>
    <td><input type="text" class="form-control" value="{{ mdp }}" maxlength="20"></td>
    <td><select class="form-control" name="grade">{{ grade }}</select></td>
    <td><input type="text" class="form-control" value="{{ nom }}" maxlength="20"></td>
    <td><input type="text" class="form-control" value="{{ prénom }}" maxlength="20"></td>
    <td><input type="text" class="form-control" value="{{ adresse }}" maxlength="120"></td>
    <td><input type="number" class="form-control" value="{{ tel }}" maxlength="10"></td>
    <td><button class="btn btn-danger" onclick="deleteUser('{{ email }}')">Supprimer</button></td></tr>`

_templateHeaderEmprunt = `<tr><th>ID</th><th>Statut<th>Livre</th><th>Date</th><th>Utilisateur</th><th>Supprimer</th></tr>`
_templateEmprunt = `<tr><td>{{ id }}</td>
    <td>{{ statut }}</td>
    <td><select class="form-control" name="livre">{{ livre }}</select></td>
    <td><input type="date" class="form-control" value="{{ date }}"></td>
    <td><select class="form-control" name="utilisateur">{{ utilisateur }}</select></td>
    <td><button class="btn btn-danger" onclick="deleteEmprunt('{{ id }}')">Supprimer</button></td></tr>`

//Emprunts = ID, Livre (isbn), Date, Utilisateur (email)

async function deleteLivre(isbn) {
    try {
        if (confirm("Voulez-vous vraiment supprimer ce livre ?") === true) {
            const response = await await fetch(`${API_URL}/deleteLivre?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}&isbn=${isbn}`);
            let data = await response.json();
            if (data.content !== 'success') {
                alert("Erreur lors de la suppression du livre, veuillez réessayer.")
                throw new Error('Failed to delete livre');
            }
            alert("Le livra a bien été supprimé !")
            showLivreArray();
        }
    } catch (error) {
            console.error('Error deleting livre:', error);
    }
}

async function deleteAuteur(id) {
    try {
        if (confirm("Voulez-vous vraiment supprimer cet auteur ? Cela supprimera l'ensemble des oeuvres et emprunts assoicées !") === true) {
            const response = await fetch(`${API_URL}/deleteAuteur?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}&id=${id}`);
            let data = await response.json();
            if (data.content !== 'success') {
                alert("Erreur lors de la suppression de l'auteur, veuillez réessayer.");
                throw new Error('Failed to delete auteur');
            }
            alert("L'auteur a bien été supprimé !");
            showAuteurArray();
        }
    } catch (error) {
        console.error('Error deleting auteur:', error);
    }
}

async function deletePointDeVente(adresse) {
    console.log(adresse)
    try {
        let adresseReplacement = prompt("Veuillez entrer le nom du point de vente de remplacement :");
        if (adresseReplacement != undefined && adresseReplacement != null && adresseReplacement != "") {
            adresseReplacement = await fetch(`${API_URL}/getPointDeVenteReplacement?replacementName=${adresseReplacement}`);
            let data = await adresseReplacement.json();
            if (data.content === 'error') {
                alert("Erreur lors du remplacement du point de vente, veuillez réessayer avec un nom correct.");
                return;
            }
            adresseReplacement = data.content;
            if (adresseReplacement === undefined || adresseReplacement === null || adresseReplacement === "") {
                alert("Erreur lors du remplacement du point de vente, veuillez réessayer avec un nom correct.");
                return;
            }
            if (confirm(`Voulez-vous vraiment supprimer le point de vente et le remplacer par ${adresseReplacement} ?`) === true) {
                const response = await fetch(`${API_URL}/deletePointDeVente?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}&adresse=${encodeURIComponent(adresse)}&adresseReplacement=${encodeURIComponent(adresseReplacement)}`);
                let data = await response.json();
                if (data.content !== 'success') {
                    alert("Erreur lors de la suppression du point de vente, veuillez réessayer.");
                    throw new Error('Failed to delete point de vente');
                }
                alert("Le point de vente a bien été supprimé !");
                showPointDeVenteArray();
            }
        }
    } catch (error) {
        console.error('Error deleting point de vente:', error);
    }
}

async function deleteEditeur(nom) {
    try {
        if (confirm("Voulez-vous vraiment supprimer cet éditeur ? Cela supprimera l'ensemble des livres publié par cet éditeur.") === true) {
            const response = await fetch(`${API_URL}/deleteEditeur?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}&nom=${nom}`);
            let data = await response.json();
            if (data.content !== 'success') {
                alert("Erreur lors de la suppression de l'éditeur, veuillez réessayer.");
                throw new Error('Failed to delete editeur');
            }
            alert("L'éditeur a bien été supprimé !");
            showEditeurArray();
        }
    } catch (error) {
        console.error('Error deleting editeur:', error);
    }
}

async function deleteUser(emailToDelete) {
    try {
        if (confirm("Voulez-vous vraiment supprimer cet utilisateur ? Cela supprimera l'ensemble des emprunts associés.") === true) {
            const response = await fetch(`${API_URL}/deleteUser?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}&emailToDelete=${emailToDelete}`);
            let data = await response.json();
            if (data.message === 'Vous ne pouvez pas supprimer un administrateur'){
                alert("Vous ne pouvez pas supprimer un administrateur.");
                return;
            }
            else if (data.content !== 'success') {
                alert("Erreur lors de la suppression de l'utilisateur, veuillez réessayer.", data.message);
                console.error( data);
                throw new Error('Failed to delete utilisateur');
            } else {
                alert("L'utilisateur a bien été supprimé !");
            }
            showUtilisateurArray();
        }
    }
    catch (error) {
        console.error('Error deleting utilisateur:', error);
    }
}

async function deleteEmprunt(id) {
    try {
        if (confirm("Voulez-vous vraiment supprimer cet emprunt ? Celui-ci sera immédiatement considéré comme remis.") === true) {
            const response = await fetch(`${API_URL}/deleteEmprunt?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}&id=${id}`);
            let data = await response.json();
            if (data.content !== 'success') {
                alert("Erreur lors de la suppression de l'emprunt, veuillez réessayer.");
                throw new Error('Failed to delete emprunt');
            }
            alert("L'emprunt a bien été supprimé !");
            showEmpruntArray();
        }
    }
    catch (error) {
        console.error('Error deleting emprunt:', error);
    }
}

async function checkIfChangeLivres(originalLivres, auteurs) {
    document.getElementById('save').addEventListener('click', async () => {
        if (browseType === "Livres") {
            const modifiedLivres = [];
            const contentRow = document.getElementById('contentRow');
            const rows = contentRow.querySelectorAll('tr');
            rows.forEach(row => {
                const isbn = row.cells[0].innerText;
                const titre = row.cells[1].querySelector('textarea').value;
                let auteur = row.cells[2].querySelector('select').value;
                const description = row.cells[3].querySelector('textarea').value;
                const dateDeParution = row.cells[4].querySelector('input').value;
                const status = row.cells[5].querySelector('select').value;
                const genre = row.cells[6].querySelector('select').value;
                const format = row.cells[7].querySelector('select').value;
                const prix = parseFloat(row.cells[8].querySelector('input').value);
                const pointDeVente = row.cells[9].querySelector('select').value;
                const editeur = row.cells[10].querySelector('select').value;
                const originalLivre = originalLivres[isbn];
                if (originalLivre.titre !== titre || originalLivre.auteur !== auteur || originalLivre.description !== description || originalLivre.dateDeParution !== dateDeParution.split('-').reverse().join('/') || originalLivre.status !== status || originalLivre.genre !== genre || originalLivre.format !== format || originalLivre.prix !== prix || originalLivre.pointDeVente !== pointDeVente || originalLivre.editeur !== editeur) {
                    Object.keys(auteurs).forEach(id => {
                        if (auteurs[id]["prénom"] +" " + auteurs[id]["nom"] === auteur || auteurs[id]["alias"] === auteur)
                            auteur = id;
                    })
                    modifiedLivres.push({isbn,titre,auteur,description,dateDeParution,status,genre,format,prix,pointDeVente,editeur});
                    console.log("Modified ", isbn,titre,auteur,description,dateDeParution,status,genre,format,prix,pointDeVente,editeur)
                }
            });
            if (modifiedLivres.length > 0) {
                try {
                    console.log("mise à jour en cours...", modifiedLivres)
                    const response = await fetch(`${API_URL}/updateLivres`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ 
                            livres: modifiedLivres,
                            email: email,
                            password: password
                        })
                    });
                    if (!response.ok) {
                        alert("Erreur lors de la mise à jour des livres, veuillez réessayer.")
                        throw new Error('Failed to update livres');
                    }
                    alert("Les modifications ont bien été prises en compte !")
                    window.location.href = "/config";
                } catch (error) {
                    console.error('Error updating livres:', error);
                }
            } else {
                alert("Vous êtes à jour !")
            }
        }
    });
}

async function checkIfChangeAuteurs(originalAuteurs) {
    document.getElementById('save').addEventListener('click', async () => {
        if (browseType === "Auteurs") {
            const modifiedAuteurs = [];
            const contentRow = document.getElementById('contentRow');
            const rows = contentRow.querySelectorAll('tr');
            rows.forEach(row => {
                const id = row.cells[0].innerText;
                const nom = row.cells[1].querySelector('input').value;
                const prénom = row.cells[2].querySelector('input').value;
                const alias = row.cells[3].querySelector('input').value === "" ? null : row.cells[3].querySelector('input').value;
                const biographie = row.cells[4].querySelector('textarea').value;
                let  dateDeNaissance = row.cells[5].querySelector('input').value === "" ? null : row.cells[5].querySelector('input').value;
                let dateDeDeces = row.cells[6].querySelector('input').value === "" ? null : row.cells[6].querySelector('input').value;
                const originalAuteur = originalAuteurs[id];
                if (dateDeNaissance !== null) {
                    dateDeNaissance = dateDeNaissance.split('-').reverse().join('/');
                } 
                if (dateDeDeces !== null) {
                    dateDeDeces = dateDeDeces.split('-').reverse().join('/');
                }
                if ((originalAuteur.nom !== nom) || (originalAuteur.prenom !== prénom) || (originalAuteur.alias !== alias) || (originalAuteur.description !== biographie) || (originalAuteur.dateDeNaissance !== dateDeNaissance) ||  (originalAuteur.dateDeDeces !== dateDeDeces)) {
                    modifiedAuteurs.push({id,nom,prénom,alias,biographie,dateDeNaissance,dateDeDeces});
                }
            });
            if (modifiedAuteurs.length > 0) {
                try {
                    console.log("mise à jour en cours...", modifiedAuteurs)
                    const response = await fetch(`${API_URL}/updateAuteurs`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ 
                            auteurs: modifiedAuteurs,
                            email: email,
                            password: password
                        })
                    });
                    if (!response.ok) {
                        alert("Erreur lors de la mise à jour des auteurs, veuillez réessayer.")
                        throw new Error('Failed to update auteurs');
                    }{
                        alert("Les modifications ont bien été prises en compte !")
                        showAuteurArray();
                    }
                } catch (error) {
                    console.error('Error updating auteurs:', error);
                }
            } else {
                alert("Vous êtes à jour !")
            }
        }
    });
}

async function checkifChangePointDeVentes(originalPointDeVentes) {
    document.getElementById('save').addEventListener('click', async () => {
        if (browseType === "Points de ventes") {
            const modifiedPointDeVentes = [];
            const contentRow = document.getElementById('contentRow');
            const rows = contentRow.querySelectorAll('tr');
            Object.keys(originalPointDeVentes).forEach((adresse,index) => {
                        row = rows[index];
                        const nom = row.cells[1].querySelector('input').value;
                        const url = row.cells[2].querySelector('input').value;
                        const tel = row.cells[3].querySelector('input').value;
                        if (originalPointDeVentes[adresse].nom !== nom || originalPointDeVentes[adresse].url !== url || originalPointDeVentes[adresse].tel !== tel) {
                            modifiedPointDeVentes.push({adresse,nom,url,tel});
                            console.log("Modified ", adresse,nom,url,tel)
                        }
            });
            if (modifiedPointDeVentes.length > 0) {
                try {
                    console.log("mise à jour en cours...", modifiedPointDeVentes)
                    const response = await fetch(`${API_URL}/updatePointDeVentes`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ 
                            pointDeVentes: modifiedPointDeVentes,
                            email: email,
                            password: password
                        })
                    });
                    if (!response.ok) {
                        alert("Erreur lors de la mise à jour des points de ventes, veuillez réessayer.")
                        throw new Error('Failed to update points de ventes');
                    } else {
                        alert("Les modifications ont bien été prises en compte !")
                    }
                } catch (error) {
                    console.error('Error updating points de ventes:', error);
                }
            } else {
                alert("Vous êtes à jour !")
                showPointDeVenteArray();
            }
        }
    });
}

async function checkIfChangeEditeurs(originalEditeurs) {
    document.getElementById('save').addEventListener('click', async () => {
        if (browseType === "Editeurs") {
            const modifiedEditeurs = [];
            const contentRow = document.getElementById('contentRow');
            const rows = contentRow.querySelectorAll('tr');
            rows.forEach(row => {
                const nom = row.cells[0].innerText;
                const adresse = row.cells[1].querySelector('input').value;
                const originalEditeur = originalEditeurs[nom];
                if (originalEditeur.adresse !== adresse) {
                    modifiedEditeurs.push({nom,adresse});
                }
            });
            if (modifiedEditeurs.length > 0) {
                try {
                    console.log("mise à jour en cours...", modifiedEditeurs)
                    const response = await fetch(`${API_URL}/updateEditeurs`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ 
                            editeurs: modifiedEditeurs,
                            email: email,
                            password: password
                        })
                    });
                    if (!response.ok) {
                        alert("Erreur lors de la mise à jour des éditeurs, veuillez réessayer.")
                        throw new Error('Failed to update éditeurs');
                    } else {
                        alert("Les modifications ont bien été prises en compte !")
                        showEditeurArray();
                    }
                } catch (error) {
                    console.error('Error updating éditeurs:', error);
                }
            } else {
                alert("Vous êtes à jour !")
            }
        }
    });
}

async function checkIfChangeUtilisateurs(originalUtilisateurs) {
    document.getElementById('save').addEventListener('click', async () => {
        if (browseType === "Utilisateurs") {
            const modifiedUtilisateurs = [];
            const contentRow = document.getElementById('contentRow');
            const rows = contentRow.querySelectorAll('tr');
            rows.forEach(row => {
                const email = row.cells[0].innerText;
                const mdp = row.cells[1].querySelector('input').value;
                const grade = row.cells[2].querySelector('select').value;
                const nom = row.cells[3].querySelector('input').value;
                const prénom = row.cells[4].querySelector('input').value;
                const adresse = row.cells[5].querySelector('input').value;
                const tel = row.cells[6].querySelector('input').value;
                const originalUtilisateur = originalUtilisateurs[email];
                if (originalUtilisateur.mdp !== mdp || originalUtilisateur.grade !== grade || originalUtilisateur.nom !== nom || originalUtilisateur.prénom !== prénom || originalUtilisateur.adresse !== adresse || originalUtilisateur.tel !== tel) {
                    modifiedUtilisateurs.push({email,mdp,grade,nom,prénom,adresse,tel});
                }
            });
            if (modifiedUtilisateurs.length > 0) {
                try {
                    console.log("mise à jour en cours...", modifiedUtilisateurs)
                    const response = await fetch(`${API_URL}/updateUtilisateurs`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ 
                            users: modifiedUtilisateurs,
                            email: email,
                            password: password
                        })
                    });
                    console.log(response)
                    if (!response.ok) {
                        alert("Erreur lors de la mise à jour des utilisateurs, veuillez réessayer.")
                        throw new Error('Failed to update utilisateurs');
                    } else {
                        alert("Les modifications ont bien été prises en compte !")
                        showUtilisateurArray();
                    }
                } catch (error) {
                    console.error('Error updating utilisateurs:', error);
                }
            } else {
                alert("Vous êtes à jour !")
            }
        }
    });
}

async function checkIfChangeEmprunts(originalEmprunts) {
    document.getElementById('save').addEventListener('click', async () => {
        if (browseType === "Emprunts") {
            const modifiedEmprunts = [];
            const contentRow = document.getElementById('contentRow');
            const rows = contentRow.querySelectorAll('tr');
            rows.forEach(row => {
                const id = row.cells[0].innerText;
                const livre = row.cells[2].querySelector('select').value;
                let date = row.cells[3].querySelector('input').value;
                const utilisateur = row.cells[4].querySelector('select').value;
                const originalEmprunt = originalEmprunts[id];
                if (date !== null) {
                    date = date.split('-').reverse().join('/');
                }

                if (originalEmprunt.isbn !== livre || originalEmprunt.Date !== date || originalEmprunt.Utilsateur !== utilisateur) {
                    console.log("UDPATED DATE", date, "ORIGINAL DATE", originalEmprunt.Date)
                    modifiedEmprunts.push({id,livre,date,utilisateur});
                }
            });
            if (modifiedEmprunts.length > 0) {
                try {
                    console.log("mise à jour en cours...", modifiedEmprunts)
                    const response = await fetch(`${API_URL}/updateEmprunts`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ 
                            emprunts: modifiedEmprunts,
                            email: email,
                            password: password
                        })
                    });
                    if (!response.ok) {
                        alert("Erreur lors de la mise à jour des emprunts, veuillez réessayer.")
                        throw new Error('Failed to update emprunts');
                    } else {
                        alert("Les modifications ont bien été prises en compte !")
                        showEmpruntArray();
                    }
                } catch (error) {
                    console.error('Error updating emprunts:', error);
                }
            } else {
                alert("Vous êtes à jour !")
            }
        }
    });
}

async function showLivreArray() {
    try {
        document.getElementById('title').innerHTML = "Tableau des livres :"
        let response = await fetch(`${API_URL}/getAllLivre`);
        let data = await response.json();
        const livres = JSON.parse(data["content"]);
        response = await fetch(`${API_URL}/getAllNomAuteur`);
        data = await response.json();
        const auteurs = JSON.parse(data["content"]);
        response = await fetch(`${API_URL}/getAllPointDeVentes`);
        data = await response.json();
        const pointDeVentes = JSON.parse(data["content"]);
        response = await fetch(`${API_URL}/getAllEditeurs`);
        data = await response.json();
        const editeurs = JSON.parse(data["content"]);
        const header = document.getElementById('templateHeader');
        header.innerHTML = _templateHeaderLivre;
        const contentRow = document.getElementById('contentRow');
        contentRow.innerHTML = '';
        let rows = '';
        Object.keys(livres).forEach(isbn => {
            let allAuteur = _templateEltDropDown.replace("{{ elt }}",livres[isbn]["auteur"]).replace("{{ elt }}",livres[isbn]["auteur"]);
            Object.keys(auteurs).forEach(id => {
                if (auteurs[id]["prénom"] +" " + auteurs[id]["nom"] !== livres[isbn]["auteur"] && auteurs[id]["alias"] !== livres[isbn]["auteurAlias"])
                    allAuteur += _templateEltDropDown.replace("{{ elt }}",auteurs[id]["prénom"] +" " + auteurs[id]["nom"]).replace("{{ elt }}",auteurs[id]["prénom"] +" " + auteurs[id]["nom"]);
            });
            let status = _templateEltDropDown.replace("{{ elt }}",livres[isbn]["status"]).replace("{{ elt }}",livres[isbn]["status"]);
            ["disponible", "emprunté", "hors stock"].forEach(s => {
                if (s !== livres[isbn]["status"])
                    status += _templateEltDropDown.replace("{{ elt }}",s).replace("{{ elt }}",s);
            });
            let dateDeParution = `${livres[isbn]["dateDeParution"].split('/')[2]}-${livres[isbn]["dateDeParution"].split('/')[1]}-${livres[isbn]["dateDeParution"].split('/')[0]}`;
            let genre = _templateEltDropDown.replace("{{ elt }}",livres[isbn]["genre"]).replace("{{ elt }}",livres[isbn]["genre"]);
            ["Historique", "Romantique", "Policier", "Science-fiction", "Fantastique", "Aventure", "Biographique", "Autobiographique", "Épistolaire", "Thriller", "Tragédie", "Drame", "Absurde", "Philosophique", "Politique", "Légendes & Mythes", "Lettres personnelles", "Voyages", "Journal intime", "Bandes dessinées", "Documentaires", "Religieux"].forEach(g => {
                if (g !== livres[isbn]["genre"])
                    genre += _templateEltDropDown.replace("{{ elt }}",g).replace("{{ elt }}",g);
            });
            let format = _templateEltDropDown.replace("{{ elt }}",livres[isbn]["format"]).replace("{{ elt }}",livres[isbn]["format"]);
            ["Poche", "Grand Format", "E-book & numérique", "Manga", "Bande Dessinée", "Magazine", "CD", "DVD & Blu-ray"].forEach(f => {
                if (f !== livres[isbn]["format"])
                    format += _templateEltDropDown.replace("{{ elt }}",f).replace("{{ elt }}",f);
            });
            let pointDeVente = _templateEltDropDown.replace("{{ elt }}",livres[isbn]["pointDeVente"]).replace("{{ elt }}",livres[isbn]["pointDeVente"]);
            Object.keys(pointDeVentes).forEach(adresse => {
                if (adresse !== livres[isbn]["pointDeVente"])
                    pointDeVente += _templateEltDropDown.replace("{{ elt }}",adresse).replace("{{ elt }}",adresse);
            });
            let editeur = _templateEltDropDown.replace("{{ elt }}",livres[isbn]["editeur"]).replace("{{ elt }}",livres[isbn]["editeur"]);
            Object.keys(editeurs).forEach(nom => {
                if (nom !== livres[isbn]["editeur"])
                    editeur += _templateEltDropDown.replace("{{ elt }}",nom).replace("{{ elt }}",nom);
            });
            rows += _templateLivre
                .replace("{{ isbn }}",isbn)
                .replace("{{ isbn }}",isbn)
                .replace("{{ titre }}", livres[isbn]["titre"])
                .replace("{{ allAuteur }}", allAuteur)
                .replace("{{ description }}", livres[isbn]["description"])
                .replace("{{ dateDeParution }}", dateDeParution)
                .replace("{{ status }}", status)
                .replace("{{ genre }}", genre)
                .replace("{{ format }}", format)
                .replace("{{ prix }}", livres[isbn]["prix"])
                .replace("{{ pointDeVente }}", pointDeVente)
                .replace("{{ editeur }}", editeur);
        });
        contentRow.innerHTML = rows;
        checkIfChangeLivres(livres, auteurs);
    } catch (error) {
        console.error('Error fetching or processing data:', error);
    }
}

async function showAuteurArray() {
    try {
        document.getElementById('title').innerHTML = "Tableau des auteurs :"
        let response = await fetch(`${API_URL}/getAllAuteur`);
        let data = await response.json();
        const auteurs = JSON.parse(data["content"]);
        const header = document.getElementById('templateHeader');
        header.innerHTML = _templateHeaderAuteur;
        const contentRow = document.getElementById('contentRow');
        contentRow.innerHTML = '';
        let rows = '';
        let dateDeNaissance;
        let dateDeDeces;
        Object.keys(auteurs).forEach(id => {
            if (auteurs[id]["dateDeNaissance"] != null) {
                dateDeNaissance = `${auteurs[id]["dateDeNaissance"].split('/')[2]}-${auteurs[id]["dateDeNaissance"].split('/')[1]}-${auteurs[id]["dateDeNaissance"].split('/')[0]}`;
            } else {
                dateDeNaissance = ''
            }
            if (auteurs[id]["dateDeDeces"] != null) {
                dateDeDeces = `${auteurs[id]["dateDeDeces"].split('/')[2]}-${auteurs[id]["dateDeDeces"].split('/')[1]}-${auteurs[id]["dateDeDeces"].split('/')[0]}`;
            } else {
                dateDeDeces = ''
            }
            rows += _templateAuteur
                .replace("{{ id }}",id)
                .replace("{{ id }}",id)
                .replace("{{ nom }}", auteurs[id]["nom"])
                .replace("{{ prénom }}", auteurs[id]["prenom"])
                .replace("{{ alias }}", auteurs[id]["alias"] === null ? "" : auteurs[id]["alias"])
                .replace("{{ biographie }}", auteurs[id]["description"])
                .replace("{{ dateDeNaissance }}", dateDeNaissance)
                .replace("{{ dateDeDécès }}", dateDeDeces);
        }
        );
        contentRow.innerHTML = rows;
        checkIfChangeAuteurs(auteurs);
    } catch (error) {
        console.error('Error fetching or processing data:', error);
    }
}

async function showPointDeVenteArray() {
    try {
        document.getElementById('title').innerHTML = "Tableau des points de vente :"
        let response = await fetch(`${API_URL}/getAllPointDeVentes`);
        let data = await response.json();
        const pointDeVentes = JSON.parse(data["content"]);
        const header = document.getElementById('templateHeader');
        header.innerHTML = _templateHeaderPointDeVente;
        const contentRow = document.getElementById('contentRow');
        contentRow.innerHTML = '';
        let rows = '';
        Object.keys(pointDeVentes).forEach(adresse => {
            adresseReplacement = adresse.replace(/\n/g, ' ');
            rows += _templatePointDeVente
                .replace("{{ adresse }}",adresse)
                .replace("{{ adresse }}",adresseReplacement)
                .replace("{{ nom }}", pointDeVentes[adresse]["nom"])
                .replace("{{ url }}", pointDeVentes[adresse]["url"])
                .replace("{{ tel }}", pointDeVentes[adresse]["tel"] === null ? "" : pointDeVentes[adresse]["tel"]);
        });
        contentRow.innerHTML = rows;
        checkifChangePointDeVentes(pointDeVentes);
    } catch (error) {
        console.error('Error fetching or processing data:', error);
    }
}

async function showEditeurArray(){
    try {
        document.getElementById('title').innerHTML = "Tableau des éditeurs :"
        let response = await fetch(`${API_URL}/getAllEditeurs`);
        let data = await response.json();
        const editeurs = JSON.parse(data["content"]);
        const header = document.getElementById('templateHeader');
        header.innerHTML = _templateHeaderEditeur;
        const contentRow = document.getElementById('contentRow');
        contentRow.innerHTML = '';
        let rows = '';
        Object.keys(editeurs).forEach(nom => {
            rows += _templateEditeur
                .replace("{{ nom }}",nom)
                .replace("{{ nom }}",nom)
                .replace("{{ adresse }}", editeurs[nom]["adresse"]);
        });
        contentRow.innerHTML = rows;
        checkIfChangeEditeurs(editeurs);
    } catch (error) {
        console.error('Error fetching or processing data:', error);
    }
}

async function showUtilisateurArray(){
    try {
        document.getElementById('title').innerHTML = "Tableau des utilisateurs :"
        let response = await fetch(`${API_URL}/getAllUtilisateurs?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`);
        let data = await response.json();
        const utilisateurs = JSON.parse(data["content"]);
        const header = document.getElementById('templateHeader');
        header.innerHTML = _templateHeaderUser;
        const contentRow = document.getElementById('contentRow');
        contentRow.innerHTML = '';
        let rows = '';
        Object.keys(utilisateurs).forEach(email => {
            rows += _templateUser
                .replace("{{ email }}",email)
                .replace("{{ email }}",email)
                .replace("{{ mdp }}", utilisateurs[email]["mdp"])
                .replace("{{ nom }}", utilisateurs[email]["nom"])
                .replace("{{ prénom }}", utilisateurs[email]["prénom"])
                .replace("{{ adresse }}", utilisateurs[email]["adresse"])
                .replace("{{ tel }}", utilisateurs[email]["tel"]);
            let grade = _templateEltDropDown.replace("{{ elt }}",utilisateurs[email]["grade"]).replace("{{ elt }}",utilisateurs[email]["grade"]);
            ["admin", "user"].forEach(g => {
                if (g !== utilisateurs[email]["grade"])
                    grade += _templateEltDropDown.replace("{{ elt }}",g).replace("{{ elt }}",g);
            });
            rows = rows.replace("{{ grade }}", grade);
        }
        );
        contentRow.innerHTML = rows;
        checkIfChangeUtilisateurs(utilisateurs);
    } catch (error) {
        console.error('Error fetching or processing data:', error);
    }
}

async function showEmpruntArray(){
    try {
        document.getElementById('title').innerHTML = "Tableau des emprunts :"
        let response = await fetch(`${API_URL}/getAllEmprunts?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`);
        let data = await response.json();
        if (data.message === "Aucun emprunt trouvé"){
            alert("Aucun n'emprunt n'a été effectué.")
            window.location.href = "/config";
        }
        const emprunts = JSON.parse(data["content"]);
        response = await fetch(`${API_URL}/getAllLivre`);
        data = await response.json();
        const livres = JSON.parse(data["content"]);
        response = await fetch(`${API_URL}/getAllUtilisateurs?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`);
        data = await response.json();
        const utilisateurs = JSON.parse(data["content"]);
        const header = document.getElementById('templateHeader');
        header.innerHTML = _templateHeaderEmprunt;
        const contentRow = document.getElementById('contentRow');
        contentRow.innerHTML = '';
        let rows = '';
        console.log("EMPRUNTS : ", emprunts, "UTIliSATEUR", utilisateurs)
        Object.keys(emprunts).forEach(id => {
            let livre = _templateEltDropDown.replace("{{ elt }}",emprunts[id]["isbn"]).replace("{{ elt }}",livres[emprunts[id]["isbn"]]["titre"]);
            Object.keys(livres).forEach(isbn => {
                if (isbn !== emprunts[id]["livre"])
                    livre += _templateEltDropDown.replace("{{ elt }}",isbn).replace("{{ elt }}",livres[isbn]["titre"]);
            });
            let utilisateur = _templateEltDropDown.replace("{{ elt }}",emprunts[id]["Utilsateur"]).replace("{{ elt }}",utilisateurs[emprunts[id]["Utilsateur"]]["nom"] + " " + utilisateurs[emprunts[id]["Utilsateur"]]["prénom"]);
            Object.keys(utilisateurs).forEach(email => {
                if (email !== emprunts[id]["Utilsateur"])
                    utilisateur += _templateEltDropDown.replace("{{ elt }}",email).replace("{{ elt }}",utilisateurs[email]["nom"] + " " + utilisateurs[email]["prénom"]);
            });
            // the statut will be defined to in late or not if the emprunt is late of 30 days
            let statut;
            console.log(emprunts)
            const [day, month, year] = emprunts[id]["Date"].split('/');
            console.log(`${year}-${month}-${day}`)
            const today = new Date();
            const date = new Date(`${year}-${month}-${day}`);
            console.log("DATE", date)
            const diffInMilliseconds = Math.abs(today - date);
            const diffInDays = Math.ceil(diffInMilliseconds / (1000 * 3600 * 24));
            if (30-diffInDays < 0) {
                statut ="En retard"
            } else {
                statut = "OK"
            }
            rows += _templateEmprunt
                .replace("{{ id }}",id)
                .replace("{{ id }}", id)
                .replace("{{ statut }}", statut)
                .replace("{{ livre }}", livre)
                .replace("{{ date }}", emprunts[id]["Date"].split('/').reverse().join("-"))
                .replace("{{ utilisateur }}", utilisateur);
        });
        contentRow.innerHTML = rows;
        checkIfChangeEmprunts(emprunts);
    } catch (error) {
        console.error('Error fetching or processing data:', error);
    }
}

let decodedCookie = decodeURIComponent(document.cookie).split(';');
let email = '', password = '';
decodedCookie.forEach(c => {
    let cookie = c.trim();
    if (cookie.startsWith('email=')) {
        email = cookie.substring('email='.length);
    }
    if (cookie.startsWith('password=')) {
        password = cookie.substring('password='.length);
    }
});

browseType = "Livres";
fetch(`${API_URL}/isAdmin?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`)
    .then(response => response.json())
    .then(data => {
        if (data.content === "success") {
            console.log("Admin Logged")
            const browseDropDown = document.querySelectorAll('.dropdown-item');
            browseDropDown.forEach(item => {
                item.addEventListener('click', function() {
                    browseType = this.textContent;
                    if (["Livres", "Auteurs", "Editeurs", "Points de ventes","Utilisateurs", "Emprunts"].includes(browseType)) {
                        if (browseType === "Livres") {
                            showLivreArray();
                        }
                        if (browseType === "Auteurs") {
                            showAuteurArray();
                        }
                        if (browseType === "Points de ventes") {
                            showPointDeVenteArray();
                        }
                        if (browseType === "Editeurs") {
                            showEditeurArray();
                        }
                        if (browseType === "Utilisateurs") {
                            showUtilisateurArray();
                        }
                        if (browseType === "Emprunts") {
                            showEmpruntArray()
                        }
                    } 
               });
            });
            browseDropDown.textContent = "Parcourir ("+browseType+")";
            showLivreArray(browseType);
        } else {
            window.location.href = "/login";
        }
})

const addButton = document.getElementById('add');
addButton.addEventListener('click', async () => {
    if (browseType === "Livres")
        window.location.href = "/addLivre";
    else if (browseType === "Auteurs")
        window.location.href = "/addAuteur";
    else if (browseType === "Editeurs")
        window.location.href = "/addEditeur";
    else if (browseType === "Points de ventes")
        window.location.href = "/addPointDeVente";
    else if (browseType === "Utilisateurs")
        window.location.href = "/createAccount";
    else if (browseType === "Emprunts")
        window.location.href = "/index";
});