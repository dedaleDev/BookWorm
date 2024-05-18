const API_URL = 'http://192.168.1.20:8080'

var _template = " <div class='row justify-content-center'> \
<div class='col-md-10' style='padding-top: 3vh'>\
    <div class='card mb-3'>\
        <h2 class='card-header'></strong>{{ titre }}</h2>\
        <div class='card-body'>\
            <ul class='list-group list-group-flush'>\
                <li class='list-group-item'><strong><a href='/search?search={{ auteur }}&type=Auteur'><h3>{{ auteur }}<h3></a></strong></li>\
                <li class='list-group-item'><img class='img-fluid align-middle' style='width: 22%;' src='/img/stars/star{{ note }}.svg'><span class='align-middle'> ({{ NoteEx }})</span></li>\
                <li class='list-group-item'>Date de parution : {{ dateDeParution }}</li>\
                <li class='list-group-item'><italic>{{ genre }}</italic></li>\
                <li class='list-group-item'>{{ description }}</li>\
                <li class='list-group-item'>Format : {{ format }}</li>\
                <li class='list-group-item'>En vente chez {{ pointDeVenteName }} ({{ pointDeVente }}) à {{ prix }} €</li>\
                <li class='list-group-item'> Editeur : {{ editeur }}</li>\
            </ul>\
        </div>\
    </div>\
</div>";


async function loadLivre(isbn) {
    console.log("livre: ", isbn);
    let response =  await fetch(`${API_URL}/getLivre?isbn=${isbn}`);
    let livreData = await response.json();
    livreData = JSON.parse(livreData["content"]);
    console.log("livre: ", livreData);
    return livreData[isbn];
}
const urlParams = new URLSearchParams(window.location.search);
const isbn = urlParams.get('isbn');

loadLivre(isbn).then(livreData => {
    if (typeof livreData === 'object' && livreData !== null) {
            console.log("livreData: ", livreData);
            let template = _template.replace("{{ titre }}", livreData["titre"]).replace("{{ auteur }}", livreData["auteur"]).replace("{{ note }}", Math.round(livreData["note"])).replace("{{ isbn }}", livreData["isbn"]).replace("{{ dateDeParution }}", livreData["dateDeParution"]).replace("{{ genre }}", livreData["genre"]).replace("{{ description }}", livreData["description"]).replace("{{ format }}", livreData["format"]).replace("{{ pointDeVente }}", livreData["pointDeVente"]).replace("{{ prix }}", livreData["prix"]).replace("{{ editeur }}", livreData["editeur"]).replace("{{ pointDeVenteName }}", livreData["pointDeVenteName"]).replace("{{ auteur }}", livreData["auteur"]).replace("{{ NoteEx }}", livreData["note"]);
            if (livreData["status"] == "emprunté") {
                document.getElementById("reservation").innerHTML = "<img class='img-fluid mx-left d-block' style='width: 70%; padding-top: 2vh' src='img/{{ status }}.svg'>".replace("{{ status }}", "borrowed");
            } else if (livreData["status"] == "disponible") {
                document.getElementById("reservation").innerHTML = "<img class='img-fluid mx-left d-block' style='width: 70%; padding-top: 2vh' src='img/{{ status }}.svg'>".replace("{{ status }}", "available");
            } else if (livreData["status"] == "hors stock") { 
                document.getElementById("reservation").innerHTML = "<img class='img-fluid mx-left d-block' style='width: 70%; padding-top: 2vh' src='img/{{ status }}.svg'>".replace("{{ status }}", "outOfStock");
            }
            template = template.replace("{{ isbn }}", livreData[isbn]);
            document.getElementById("LivreInfo").innerHTML += template;
            console.log('img/livres/'+isbn+'.jpg')
            document.getElementById("imgLivre").src = `img/livres/${isbn}.jpg`;
        }
    else {
        document.getElementById("LivreInfo").innerHTML = "<br><h2 class='text-center' style='color:white'>Oups, aucun résultat n'a été trouvé.<h2><br><img id='mascotte404' class='img-fluid mx-auto d-block w-25' src='../img/error404.svg' alt='404'>";
    }
    
});
