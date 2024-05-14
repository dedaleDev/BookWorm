const API_URL = 'http://127.0.0.1:8080'
const urlParams = new URLSearchParams(window.location.search);
const searchValue = urlParams.get('search');
let typeSearch = urlParams.get('type');

var _templateLivre = "\
<div class='row justify-content-center'> \
    <div class='col-md-6'>\
        <div class='card mb-3'>\
            <h5 class='card-header'></strong>{{ titre }}</h5>\
            <div class='card-body'>\
                <ul class='list-group list-group-flush'>\
                    <li class='list-group-item'><strong>{{ auteur }}</strong></li>\
                    <li class='list-group-item'><strong>Note :</strong>{{ note }}</li>\
                    <li class='list-group-item'><img class='img-fluid mx-auto d-block w-30' src='img/livres/{{ isbn }}.jpg'></li>\
                </ul>\
            </div>\
        </div>\
    </div>;\
<div>\
";

var _templateAuteur = "\
<div class='row justify-content-center'> \
    <div class='col-md-6'>\
        <div class='card mb-3'>\
            <h5 class='card-header'></strong>{{ prenom }} {{ nom }}</h5>\
            <div class='card-body'>\
                <ul class='list-group list-group-flush'>\
                    <li class='list-group-item'><strong>{{ dateDeNaissance }}</strong></li>\
                    <li class='list-group-item'>{{ description }}</li>\
                </ul>\
            </div>\
        </div>\
    </div>;\
<div>\
";

var _templateAuteurWithAlias = "\
<div class='row justify-content-center'> \
    <div class='col-md-6'>\
        <div class='card mb-3'>\
            <h5 class='card-header'></strong>{{ alias }}</h5>\
            <div class='card-body'>\
                <ul class='list-group list-group-flush'>\
                    <li class='list-group-item'><strong>{{ prenom }} {{ nom }}</strong></li>\
                    <li class='list-group-item'><strong>{{ dateDeNaissance }}</strong></li>\
                    <li class='list-group-item'>{{ description }}</li>\
                </ul>\
            </div>\
        </div>\
    </div>;\
<div>\
";

async function search() {//RECHERCHE
    if (typeSearch == null) {
        typeSearch = "livre";
    }
    document.getElementById("searchInput").setAttribute("value", searchValue);
    let searchData = ""
    if (typeSearch == "Auteur") {
        let response =  await fetch(`${API_URL}/searchAuteur?search=${searchValue}`);
        searchData = await response.json();
        if (searchData == null) {
            return null;
        }
    }
    else if (typeSearch == "Editeur") {
        let response =  await fetch(`${API_URL}/searchEditeur?search=${searchValue}`);
    }
    else if (typeSearch == "Point de vente") {
        let response =  await fetch(`${API_URL}/searchPointDeVente?search=${searchValue}`);
    }
    else {
        let response =  await fetch(`${API_URL}/searchLivre?search=${searchValue}`);
        searchData = await response.json();
        if (response == null) {
            return null;
        }
    }
    searchData = JSON.parse(searchData["content"]);
    console.log("searchData: ", searchData);
    return searchData;
}

async function showLivre(searchData, isbnArray) {
    isbnArray.forEach(isbn => {
        let template = _templateLivre.replace("{{ titre }}", searchData[isbn]["titre"]).replace("{{ auteur }}", searchData[isbn]["auteur"]).replace("{{ note }}", searchData[isbn]["note"]).replace("{{ isbn }}", isbn);
        const livre = document.createElement('div');
        livre.innerHTML = template;
        livre.addEventListener('click', () => {
            window.location.href = `livre?isbn=${isbn}`;
        });
        document.getElementById("searchResult").appendChild(livre);
    });
}

async function showAuteur(searchData, idAuteur) {
    idAuteur.forEach(id => {
        let template =  _templateAuteur.replace("{{ prenom }}", searchData[id]["prenom"]).replace("{{ nom }}", searchData[id]["nom"]).replace("{{ dateDeNaissance }}", searchData[id]["dateDeNaissance"]).replace("{{ description }}", searchData[id]["description"]);
        if (searchData[id]["alias"] != null) {
            template = _templateAuteurWithAlias.replace("{{ alias }}", searchData[id]["alias"]).replace("{{ prenom }}", searchData[id]["prenom"]).replace("{{ nom }}", searchData[id]["nom"]).replace("{{ dateDeNaissance }}", searchData[id]["dateDeNaissance"]).replace("{{ description }}", searchData[id]["description"]);
        }
        const auteur = document.createElement('div');
        auteur.innerHTML = template;
        console.log("id: ", id);
        document.getElementById("searchResult").appendChild(auteur);
    });
}

search().then(searchData => {//AFFICHAGE DES RESULTATS
    if (typeof searchData === 'object' && searchData !== null) {
        let primaryKeys = Object.keys(searchData);
        if (typeSearch == "Livre") {
            showLivre(searchData, primaryKeys);
        } else if (typeSearch == "Auteur") {
            showAuteur(searchData, primaryKeys);
        }
        
    }
    else {
        document.getElementById("searchResult").innerHTML = "<h2 class='text-center' style='color:white; padding:0px'>Oups, aucun résultat n'a été trouvé.<h2><img id='mascotte404' class='img-fluid mx-auto d-block w-25' src='../img/error404.svg' alt='404'>";
    }
});

const searchInput = document.querySelector('input#searchInput');
const searchButton = document.querySelector('button#searchButton');


let dropdownItems = document.querySelectorAll('.dropdown-item');//CHOIX DU TYPE DE RECHERCHE
dropdownItems.forEach(item => {
    item.addEventListener('click', function() {
        let selectedValue = this.textContent;
        if (["Livre", "Auteur", "Editeur", "Point de vente"].includes(selectedValue)) {
            typeSearch = selectedValue;
            window.location.href = `search?search=${searchValue}&type=${typeSearch}`;
        }            
    });
});

searchButton.addEventListener('click', async (e) => {//BOUTON RECHERCHER
    e.preventDefault(); // evite le rechargement de la page
    const searchValue = searchInput.value.trim();// recupere la valeur de l'input sans les espaces
    if (searchValue) {
      try {
        window.location.href = `search?search=${searchValue}&type=${typeSearch}`;
      } catch (error) {
        console.error(error);
      }
    }
  });

