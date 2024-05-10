const API_URL = 'http://127.0.0.1:8080'

var _template = " <div class='row justify-content-center'> \
<div class='col-md-4'>\
    <div class='card mb-3'>\
        <h5 class='card-header'></strong>{{ titre }}</h5>\
        <div class='card-body'>\
            <ul class='list-group list-group-flush'>\
                <li class='list-group-item'><strong>{{ auteur }}</strong></li>\
                <li class='list-group-item'><strong>Note :</strong>{{ note }}</li>\
                <li class='list-group-item'><img class='img-fluid' src='img/livres/{{ titre }}.jpg'></li>\
            </ul>\
        </div>\
    </div>\
</div>";
async function search() {
    const urlParams = new URLSearchParams(window.location.search);
    const searchValue = urlParams.get('search');
    console.log("search: ", searchValue);
    let response =  await fetch(`${API_URL}/searchLivre?search=${searchValue}`);
    let searchData = await response.json();
    searchData = JSON.parse(searchData["content"]);
    console.log("response: ", searchData);
    return searchData;
}

function ConvertTitleToImagePath(imagePath){
    let bannedChar = ['"', "'", '/', '\\', '?', '*', '<', '>', '|', ':', ' '];
    for (let i = 0; i < bannedChar.length; i++) {
        imagePath = imagePath.split(bannedChar[i]).join('_');
    }
    imagePath = imagePath.replace(/à|á|ã|å|ä/g, 'a');
    imagePath = imagePath.replace(/é|è|ë|ê/g, 'e');
    imagePath = imagePath.replace(/î|ï|î/g, 'i');
    imagePath = imagePath.replace(/ô|ö|ò|õ/g, 'o');
    imagePath = imagePath.replace(/û|ü|ù/g, 'u');
    imagePath = imagePath.replace(/ç/g, 'c');
    return imagePath
}

search().then(searchData => {
    if (typeof searchData === 'object' && searchData !== null) {
        let isbnArray = Object.keys(searchData);
        for (var i = 0; i < isbnArray.length; i++) {
            let template = _template.replace("{{ titre }}", searchData[isbnArray[i]]["titre"]).replace("{{ auteur }}", searchData[isbnArray[i]]["auteur"]).replace("{{ note }}", searchData[isbnArray[i]]["note"]);
            //dictionnaraire remplacement accents et caractères non accentués
            let imagePath = ConvertTitleToImagePath(searchData[isbnArray[i]]["titre"]);
            console.log(imagePath)
            template = template.replace("{{ titre }}",imagePath);
            document.getElementById("searchResult").innerHTML += template;
        }
    }
    else {
        document.getElementById("searchResult").innerHTML = "<br>Oups, aucun résultat n'a été trouvé. Veuillez retenter votre recherche.<br><img id='mascotte404' class='img-fluid' src='../img/error404.svg' alt='404'>";
    }
    
});