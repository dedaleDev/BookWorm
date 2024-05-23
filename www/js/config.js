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
            window.location.href = "/config";
            showLivreArray();
        }
    } catch (error) {
            console.error('Error deleting livre:', error);
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
                    }
                    alert("Les modifications ont bien été prises en compte !")
                    //window.location.href = "/config";
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
                    }
                    alert("Les modifications ont bien été prises en compte !")
                    //window.location.href = "/config";
                } catch (error) {
                    console.error('Error updating points de ventes:', error);
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
            Object.keys(pointDeVentes).forEach(addresse => {
                if (addresse !== livres[isbn]["pointDeVente"])
                    pointDeVente += _templateEltDropDown.replace("{{ elt }}",addresse).replace("{{ elt }}",addresse);
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

//Auteur Row = ID, Nom, Prénom,Alias (can be null), Biographie, Date de naissance, dateDeDeces (can be null)

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

//Adresse Nom Site web	varchar(50)	Tel (can be null)

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
            rows += _templatePointDeVente
                .replace("{{ adresse }}",adresse)
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
        window.location.href = "/addUtilisateur";
    else if (browseType === "Emprunts")
        window.location.href = "/addEmprunt";
});