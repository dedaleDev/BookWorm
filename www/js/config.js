const API_URL = 'http://192.168.1.20:8080'

_templateHeaderLivre = `<tr><th>ISBN</th><th>Titre</th><th>Auteur</th><th>Description</th><th>Date de parution</th><th>Status</th><th>Genre</th><th>Format</th><th>Prix</th><th>Point de vente</th><th>Editeur</th><th>Supprimer</th></tr>`
_templateLivre = `<tr><td>{{ isbn }}</td>
    <td><textarea maxlength="100" class="form-control">{{ titre }}</textarea></td>
    <td><select class="form-control" name="auteur">{{ allAuteur }}</select></td>
    <td><textarea maxlength="1000" class="form-control">{{ description }}</textarea></td>
    <td><input type="date" class="form-control" value="{{ dateDeParution }}"></td>
    <td><select class="form-control" name="status">{{ status }}</select></td>
    <td><select class="form-control"  name="genre">{{ genre }}</select></td>
    <td><select class="form-control"  name="format">{{ format }}"</select></td>
    <td><input type="number" class="form-control" value="{{ prix }}" min="0" max="500" ></td>
    <td><select class="form-control"  name="pointDeVente">{{ pointDeVente }}</select></td>
    <td><select class="form-control"  name="editeur">{{ editeur }}</select></td>
    <td><button class="btn btn-danger" onclick="deleteLivre('{{ isbn }}')">Supprimer</button></td></tr>`
_templateEltDropDown = `<option value="{{ elt }}">{{ elt }}</option>`

async function deleteLivre(isbn) {
    try {
        if (confirm("Voulez-vous vraiment supprimer ce livre ?") === true) {
            const response = await await fetch(`${API_URL}/deleteLivre?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}&isbn=${isbn}`);
            let data = await response.json();
            console.log(data)
            if (data.content !== 'success') {
                alert("Erreur lors de la suppression du livre, veuillez réessayer.")
                throw new Error('Failed to delete livre');
            }
            alert("Le livre a bien été supprimé !")
            window.location.href = "/config";
            showLivreArray();
        }
    } catch (error) {
            console.error('Error deleting livre:', error);
    }
}

async function checkIfChangeLivres(originalLivres, auteurs) {
    document.getElementById('save').addEventListener('click', async () => {
        const modifiedLivres = [];
        const contentRow = document.getElementById('contentRow');
        const rows = contentRow.querySelectorAll('tr');
        console.log(originalLivres)
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
                console.log(originalLivre.auteur, "==", auteur)
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
            } catch (error) {
                console.error('Error updating livres:', error);
            }
        } else {
            alert("Vous êtes à jour !")
        }
    });
}

async function showLivreArray() {
    try {
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
                            showLivreArray(browseType);
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