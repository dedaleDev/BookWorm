const API_URL = 'http://192.168.1.20:8080'


let email, password, dispoOnly, genre;

async function getCookieValue(name) {
    const cookieString = decodeURIComponent(document.cookie);
    const cookies = cookieString.split(';');
    for (let cookie of cookies) {
        let [key, value] = cookie.trim().split('=');
        if (key === name) {
            return value;
        }
    }
    return null;
}

async function checkLoginAndGetUserInfo() {
    try {
        email = await getCookieValue('email');
        password = await getCookieValue('password');
        const response = await fetch(`${API_URL}/checkLogin?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`);
        const data = await response.json();
        if (data.content === 'success') {
            document.getElementById("account").src = "../img/account.svg";
            const adminResponse = await fetch(`${API_URL}/isAdmin?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`);
            const adminData = await adminResponse.json();
            if (adminData.content === "success") {
                document.getElementById('config').innerHTML = `<img src="../img/smallConfig.svg" alt="Config" class="img-fluid"  style="width: 20vh;"">`;
            } else {
                document.getElementById('config').innerHTML = "";
            }
        } else {
            document.getElementById('config').innerHTML = "";
            document.getElementById("account").src = "../img/login.svg";
        }
    } catch (error) {
        console.error('Error checking login and fetching user info:', error);
        document.getElementById('config').innerHTML = "";
        document.getElementById("account").src = "../img/login.svg";
    }
}
checkLoginAndGetUserInfo();

const urlParams = new URLSearchParams(window.location.search);
const searchValue = urlParams.get('search');
let typeSearch = urlParams.get('type');
let sort = ""
if (typeSearch == "Livre"){
    sort= urlParams.get('sort');
    if (sort == null){
        sort = "sortByPertinence";
    }
    filterAuteur = urlParams.get('auteur');
    if (filterAuteur == null){
        filterAuteur = "all";
    }
}

dispoOnly = false;
async function checkDispo() {
    dispoOnly = await getCookieValue('dispoOnly');
    console.log("dispoOnly", dispoOnly);
    const dispoCheckBox = document.getElementById("dispo");
    if (dispoOnly == "true") {
        dispoCheckBox.checked = true;
    } else {
        dispoCheckBox.checked = false;
    }

    dispoCheckBox.addEventListener('change', async (e) => {
        if (e.target.checked) {
            document.cookie = `dispoOnly=${true}`;
            window.location.href = `search?search=${searchValue}&type=${typeSearch}&sort=${sort}&auteur=${filterAuteur}`;
        } else {
            document.cookie = `dispoOnly=${false}`;
            window.location.href = `search?search=${searchValue}&type=${typeSearch}&sort=${sort}&auteur=${filterAuteur}`;
        }
    });
}

checkDispo();

async function checkGenre() {
    genre = await getCookieValue('genre');
    if (genre == null){
        genre = "all";
    }
    let genreButton = {
        "Historique": "Historique",
        "Romantique": "Romantique",
        "Policier": "Policier",
        "Science-fiction": "Science-fiction",
        "Fantastique": "Fantastique",
        "Aventure": "Aventure",
        "Biographique": "Biographique",
        "Autobiographique": "Autobiographique",
        "Épistolaire": "Épistolaire",
        "Thriller": "Thriller",
        "Tragédie": "Tragédie",
        "Drame": "Drame",
        "Absurde": "Absurde",
        "Philosophique": "Philosophique",
        "Politique": "Politique",
        "Légendes & Mythes": "Légendes & Mythes",
        "Lettres personnelles": "Lettres personnelles",
        "Voyages": "Voyages",
        "Journal intime": "Journal intime",
        "Bandes dessinées": "Bandes dessinées",
        "Documentaires": "Documentaires",
        "Religieux": "Religieux"
    }
    if (genre == "all"){
        document.getElementById("selectGenre").textContent = "Genre";
    } else {
        document.getElementById("selectGenre").textContent = "Genre "+genreButton[genre];
    }
    console.log("Genre", genre);
    let dropdownItems = document.querySelectorAll('.dropdown-item');//CHOIX DU TYPE DE RECHERCHE
    dropdownItems.forEach(item => {
        item.addEventListener('click', function() {
            let selectedValue = this.textContent;
            if (["Historique", "Romantique", "Policier", "Science-fiction", "Fantastique", "Aventure", "Biographique", "Autobiographique", "Épistolaire", "Thriller", "Tragédie", "Drame", "Absurde", "Philosophique", "Politique", "Légendes & Mythes", "Lettres personnelles", "Voyages", "Journal intime", "Bandes dessinées", "Documentaires", "Religieux"].includes(selectedValue)) {
                document.cookie = `genre=${selectedValue}`;
                window.location.href = `search?search=${searchValue}&type=${typeSearch}&sort=${sort}&auteur=${filterAuteur}`;
            } else if (selectedValue == "Tout") {
                document.cookie = `genre=all`;
                window.location.href = `search?search=${searchValue}&type=${typeSearch}&sort=${sort}&auteur=${filterAuteur}`;
            }
        });
    });
}
checkGenre();


document.getElementById("selectTypeButton").textContent = "Type de recherche ("+typeSearch+")";
let sortButton = {
    "sortByPertinence": "pertinence✦",
    "sortByAlpha": "ordre alphabétique",
    "sortByNote": "note",
    "sortByDate": "date de parution",
    "sortByPrix": "prix"
}
if (typeSearch == "Livre"){
    document.getElementById("selectSortButton").textContent = "Tri par "+sortButton[sort];
} else {
    document.getElementById("selectSortButton").style.display = "none";
}
var _templateLivre = "\
<div class='row justify-content-center'> \
    <div class='col-md-6'>\
        <div class='card mb-3'>\
            <h2 class='card-header'></strong>{{ titre }}</h2>\
            <div class='card-body'>\
                <ul class='list-group list-group-flush'>\
                    <li class='list-group-item'><strong><a href='/search?search={{ auteur }}&type=Auteur'><h3>{{ auteur }}</h3></a></strong></li>\
                    <li class='list-group-item'><img class='img-fluid align-middle' style='width: 10%;' src='/img/stars/star{{ note }}.svg'><span class='align-middle'> ({{ NoteEx }})</span></li>\
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
            <h2 class='card-header'></strong>{{ prenom }} {{ nom }}</h2>\
            <div class='card-body'>\
                <ul class='list-group list-group-flush'>\
                    <li class='list-group-item'><strong>Né le : {{ dateDeNaissance }}</strong></li>\
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
            <h2 class='card-header'></strong>{{ alias }}</h2>\
            <div class='card-body'>\
                <ul class='list-group list-group-flush'>\
                    <li class='list-group-item'><strong><h3>{{ prenom }} {{ nom }}</h3></strong></li>\
                    <li class='list-group-item'><strong>Né le : {{ dateDeNaissance }}</strong></li>\
                    <li class='list-group-item'>{{ description }}</li>\
                </ul>\
            </div>\
        </div>\
    </div>;\
<div>\
";

var _templatePointDeVente = "\
<div class='row justify-content-center'> \
    <div class='col-md-6'>\
        <div class='card mb-3'>\
            <h2 class='card-header'></strong>{{ nom }}</h2>\
            <div class='card-body'>\
                <ul class='list-group list-group-flush'>\
                    <li class='list-group-item'><strong>Adresse : {{ adresse }}</strong></li>\
                    <li class='list-group-item'>Site web : <a script='color: black;' href={{ url }}>{{ url }}</a></li>\
                    <li class='list-group-item'>N°{{ tel }}</li>\
                </ul>\
            </div>\
        </div>\
    </div>;\
<div>\
";


var _templateEditeur = "\
<div class='row justify-content-center'> \
    <div class='col-md-6'>\
        <div class='card mb-3'>\
            <h2 class='card-header'></strong>{{ nom }}</h2>\
            <div class='card-body'>\
                <ul class='list-group list-group-flush'>\
                    <li class='list-group-item'><strong>Adresse : {{ adresse }}</strong></li>\
                </ul>\
            </div>\
        </div>\
    </div>;\
<div>\
";

var _templateFilter = "<div class='checkbox' style='padding-left: 1vh;'><label>{{ auteur }}</label></div>";

async function search() {//RECHERCHE
    if (typeSearch == null) {
        typeSearch = "Livre";
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
        searchData = await response.json();
        if (searchData == null) {
            return null;
        }
    }
    else if (typeSearch == "Point de vente") {
        let response =  await fetch(`${API_URL}/searchPointDeVente?search=${searchValue}`);
        searchData = await response.json();
        if (searchData == null) {
            return null;
        }
    }
    else {
        let response =  await fetch(`${API_URL}/searchLivre?search=${searchValue}&sort=${sort}&auteur=${filterAuteur}`);
        searchData = await response.json();
        if (response == null) {
            return null;
        }
    }
    console.log("searchData: ", searchData);
    try {
        searchData = JSON.parse(searchData["content"]);
    } catch (error) {
        console.error(error);
        return null;
    }
    console.log("searchData: ", searchData);
    return searchData;
}

let auteurs = []

async function showLivre(searchData, isbnArray) {
    cmpt = 0;
    isbnArray.forEach(id => {
        let display = true;
        console.log("dispoOnly: ", dispoOnly, typeof(dispoOnly));
        if (dispoOnly == "true") {
            if (searchData[id]["status"] === "emprunté" || searchData[id]["status"] === "hors stock") {
                display = false;
            }
        }
        if (genre != "all"){
            if (!searchData[id]["genre"].includes(genre)){
                display = false;
            }
        }
        if (display){
            let template = _templateLivre.replace("{{ titre }}", searchData[id]["titre"]).replace("{{ auteur }}", searchData[id]["auteur"]).replace("{{ note }}", Math.round(searchData[id]["note"])).replace("{{ isbn }}", searchData[id]["ISBN"]).replace("{{ auteur }}", searchData[id]["auteur"]).replace("{{ NoteEx }}", searchData[id]["note"]);
            const livre = document.createElement('div');
            livre.innerHTML = template;
            livre.addEventListener('click', () => {
                window.location.href = `livre?isbn=${searchData[id]["ISBN"]}`;
            });
            document.getElementById("searchResult").appendChild(livre);
            if (!auteurs.includes(searchData[id]["auteur"])) {
                auteurs.push(searchData[id]["auteur"]);
                const filter = document.getElementById("FilterAuteur");
                const filterAuteur = document.createElement('div');
                filterAuteur.innerHTML = _templateFilter.replace("{{ auteur }}", searchData[id]["auteur"]);
                filter.appendChild(filterAuteur);
            }
            if (filterAuteur != "all" && searchData[id]["auteur"] != filterAuteur) {
                livre.style.display = "none";
            } else {
                cmpt++;
            }
        } else {
            console.log("livre non affiché : ", searchData[id]);
        }
    }); 
    if (auteurs.length <= 1){
        document.getElementById("dropdownAuteurFilter").style.display = "none";
    }
    if (cmpt == 0) {
        let error404 = "<h2 class='text-center' style='color:white; padding:0px'>Oups, aucun résultat n'a été trouvé dans {{ typeSearch }}.<h2><img id='mascotte404' class='img-fluid mx-auto d-block w-25' src='../img/error404.svg' alt='404'>".replace("{{ typeSearch }}", typeSearch);
        document.getElementById("searchResult").innerHTML = error404;
    } else {
        console.log("cmpt: ", cmpt);
        document.getElementById("cmpt").innerHTML = cmpt+" documents trouvés.";
    }
}

async function showAuteur(searchData, idAuteur) {
    let cmpt = 0;
    document.getElementById("dropdownAuteurFilter").style.display = "none";
    document.getElementById("dropdownGenre").style.display = "none";
    document.getElementById("dropdownSort").style.display = "none";
    document.getElementById("disponibleCheckBox").style.display = "none";
    idAuteur.forEach(id => {
        cmpt++;
        let template =  _templateAuteur.replace("{{ prenom }}", searchData[id]["prenom"]).replace("{{ nom }}", searchData[id]["nom"]).replace("{{ dateDeNaissance }}", searchData[id]["dateDeNaissance"]).replace("{{ description }}", searchData[id]["description"]);
        if (searchData[id]["alias"] != null) {
            template = _templateAuteurWithAlias.replace("{{ alias }}", searchData[id]["alias"]).replace("{{ prenom }}", searchData[id]["prenom"]).replace("{{ nom }}", searchData[id]["nom"]).replace("{{ dateDeNaissance }}", searchData[id]["dateDeNaissance"]).replace("{{ description }}", searchData[id]["description"]);
        }
        const auteur = document.createElement('div');
        auteur.innerHTML = template;
        console.log("id: ", id);
        document.getElementById("searchResult").appendChild(auteur);
    });
    if (cmpt == 0) {
        let error404 = "<h2 class='text-center' style='color:white; padding:0px'>Oups, aucun résultat n'a été trouvé dans {{ typeSearch }}.<h2><img id='mascotte404' class='img-fluid mx-auto d-block w-25' src='../img/error404.svg' alt='404'>".replace("{{ typeSearch }}", typeSearch);
        document.getElementById("searchResult").innerHTML = error404;
    } else {
        console.log("cmpt: ", cmpt);
        document.getElementById("cmpt").innerHTML = cmpt+" auteurs trouvés.";
    }
}

async function showPointDeVente(searchData, idPointDeVente) {
    let cmpt = 0;
    document.getElementById("dropdownAuteurFilter").style.display = "none";
    document.getElementById("dropdownGenre").style.display = "none";
    document.getElementById("dropdownSort").style.display = "none";
    document.getElementById("disponibleCheckBox").style.display = "none";
    idPointDeVente.forEach(id => {
        let template =  _templatePointDeVente.replace("{{ nom }}", searchData[id]["nom"]).replace("{{ adresse }}", id).replace("{{ url }}", searchData[id]["url"]).replace("{{ tel }}", searchData[id]["tel"]);
        template = template.replace("{{ url }}", searchData[id]["url"]);
        const pointDeVente = document.createElement('div');
        pointDeVente.innerHTML = template;
        document.getElementById("searchResult").appendChild(pointDeVente);
        cmpt++;
    });
    if (cmpt == 0) {
        let error404 = "<h2 class='text-center' style='color:white; padding:0px'>Oups, aucun résultat n'a été trouvé dans {{ typeSearch }}.<h2><img id='mascotte404' class='img-fluid mx-auto d-block w-25' src='../img/error404.svg' alt='404'>".replace("{{ typeSearch }}", typeSearch);
        document.getElementById("searchResult").innerHTML = error404;
    } else {
        console.log("cmpt: ", cmpt);
        document.getElementById("cmpt").innerHTML = cmpt+" points de ventes trouvés.";
    }
}

async function showEditeur(searchData, idEditeur) {
    let cmpt = 0;
    document.getElementById("dropdownAuteurFilter").style.display = "none";
    document.getElementById("dropdownGenre").style.display = "none";
    document.getElementById("dropdownSort").style.display = "none";
    document.getElementById("disponibleCheckBox").style.display = "none";
    console.log(searchData)
    idEditeur.forEach(id => {
        let template =  _templateEditeur.replace("{{ nom }}", id).replace("{{ adresse }}", searchData[id]["adresse"]);
        const editeur = document.createElement('div');
        editeur.innerHTML = template;
        document.getElementById("searchResult").appendChild(editeur);
        cmpt++;
    });
    if (cmpt == 0) {
        let error404 = "<h2 class='text-center' style='color:white; padding:0px'>Oups, aucun résultat n'a été trouvé dans {{ typeSearch }}.<h2><img id='mascotte404' class='img-fluid mx-auto d-block w-25' src='../img/error404.svg' alt='404'>".replace("{{ typeSearch }}", typeSearch);
        document.getElementById("searchResult").innerHTML = error404;
    } else {
        console.log("cmpt: ", cmpt);
        document.getElementById("cmpt").innerHTML = cmpt+" editeurs trouvés.";
    }
}

search().then(searchData => {//AFFICHAGE DES RESULTATS
    console.log("searchData: ", searchData, typeof searchData);
    if (typeof searchData === 'object' && searchData !== null) {
        let primaryKeys = Object.keys(searchData);
        if (typeSearch == "Livre") {
            showLivre(searchData, primaryKeys);
        } else if (typeSearch == "Auteur") {
            showAuteur(searchData, primaryKeys);
        } else if (typeSearch == "Point de vente") {
            showPointDeVente(searchData, primaryKeys);
        } else if (typeSearch == "Editeur") {
            showEditeur(searchData, primaryKeys);
        }
    }
    else {
        let error404 = "<h2 class='text-center' style='color:white; padding:0px'>Oups, aucun résultat n'a été trouvé dans {{ typeSearch }}.<h2><img id='mascotte404' class='img-fluid mx-auto d-block w-25' src='../img/error404.svg' alt='404'>".replace("{{ typeSearch }}", typeSearch);
        document.getElementById("searchResult").innerHTML = error404;
        document.getElementById("dropdownGenre").style.display = "none";
        document.getElementById("dropdownSort").style.display = "none";
        document.getElementById("disponibleCheckBox").style.display = "none";
        document.getElementById("dropdownAuteurFilter").style.display = "none";
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
        } else if ([ "Pertinence✦","Ordre alphabétique", "Note", "Date de parution", "Prix"].includes(selectedValue)) {
            sort = this.id;
            console.log("sort: ", sort);
            window.location.href = `search?search=${searchValue}&type=${typeSearch}&sort=${sort}&auteur=${filterAuteur}`;
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

const filtersAuteurs = document.getElementById("FilterAuteur");
filtersAuteurs.addEventListener('click', async (e) => {
    if (e.target.tagName === 'INPUT' && e.target.type === 'checkbox') {
        return; // allow the checkbox to toggle its state
      }
    e.preventDefault();
    const filterAuteur = e.target.textContent;
    console.log("filterAuteur: ", filterAuteur);
    window.location.href = `search?search=${searchValue}&type=${typeSearch}&sort=${sort}&auteur=${filterAuteur}`;
})


