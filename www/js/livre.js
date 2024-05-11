const API_URL = 'http://127.0.0.1:8080'

var _template = " <div class='row justify-content-center'> \
<a href='livre?isbn={{ isbn }}'\
<div class='col-md-4'>\
    <div class='card mb-3'>\
        <h5 class='card-header'></strong>{{ titre }}</h5>\
        <div class='card-body'>\
            <ul class='list-group list-group-flush'>\
                <li class='list-group-item'><strong>{{ auteur }}</strong></li>\
                <li class='list-group-item'><strong>Note :</strong>{{ note }}</li>\
                <li class='list-group-item'>{{ dateDeParution }}</li>\
                <li class='list-group-item'><img class='img-fluid' src=img/{{ status }}.png</li>\
                <li class='list-group-item'><italic>{{ genre }}</italic></li>\
                <li class='list-group-item'>{{ description }}</li>\
                <li class='list-group-item'>Format : {{ format }}</li>\
                <li class='list-group-item'>En vente chez {{ pointDeVente }} à {{ prix }} €</li>\
                <li class='list-group-item'> Editeur : {{ editeur }}</li>\
            </ul>\
        </div>\
    </div>\
</a>\
</div>";

async function loadLivre() {
    const urlParams = new URLSearchParams(window.location.search);
    const isbn = urlParams.get('isbn');
    console.log("livre: ", isbn);
    let response =  await fetch(`${API_URL}/getLivre?isbn=${isbn}`);
    let livreData = await response.json();
    livreData = JSON.parse(livreData["content"]);
    console.log("response: ", livreData);
    return livreData;
}

loadLivre().then(livreData => {
    if (typeof livreData === 'object' && livreData !== null) {
            let template = _template.replace("{{ titre }}", livreData["titre"]).replace("{{ auteur }}", livreData["auteur"]).replace("{{ note }}", livreData["note"]).replace("{{ isbn }}", livreData["isbn"]).replace("{{ dateDeParution }}", livreData["dateDeParution"]).replace("{{ status }}", livreData["status"]).replace("{{ genre }}", livreData["genre"]).replace("{{ description }}", livreData["description"]).replace("{{ format }}", livreData["format"]).replace("{{ pointDeVente }}", livreData["pointDeVente"]).replace("{{ prix }}", livreData["prix"]).replace("{{ editeur }}", livreData["editeur"]);
            document.getElementById("searchResult").innerHTML += template;
        }
    else {
        document.getElementById("searchResult").innerHTML = "<br><h2 class='text-center' style='color:white'>Oups, aucun résultat n'a été trouvé.<h2><br><img id='mascotte404' class='img-fluid mx-auto d-block w-25' src='../img/error404.svg' alt='404'>";
    }
    
});
