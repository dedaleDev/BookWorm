const API_URL = 'http://127.0.0.1:8080'

var _template = "<div class='row justify-content-center'> \
<div class='col-md-4'>\
    <div class='card mb-3'>\
        <h5 class='card-header'></strong>{{ titre }}</h5>\
        <div class='card-body'>\
            <ul class='list-group list-group-flush'>\
                <li class='list-group-item'><strong>{{ auteur }}</strong></li>\
                <li class='list-group-item'><strong>Note :</strong>{{ note }}</li>\
                <li class='list-group-item'><img class='img-fluid' src='img/livres/{{ isbn }}.jpg'></li>\
            </ul>\
        </div>\
    </div>\
</div>";
async function search() {
    const urlParams = new URLSearchParams(window.location.search);
    const searchValue = urlParams.get('search');
    document.getElementById("searchInput").setAttribute("value", searchValue);
    console.log("search: ", searchValue);
    let response =  await fetch(`${API_URL}/searchLivre?search=${searchValue}`);
    let searchData = await response.json();
    searchData = JSON.parse(searchData["content"]);
    console.log("response: ", searchData);
    return searchData;
}

search().then(searchData => {
    if (typeof searchData === 'object' && searchData !== null) {
        let isbnArray = Object.keys(searchData);
        isbnArray.forEach(isbn => {
            let template = _template.replace("{{ titre }}", searchData[isbn]["titre"]).replace("{{ auteur }}", searchData[isbn]["auteur"]).replace("{{ note }}", searchData[isbn]["note"]).replace("{{ isbn }}", isbn);
            const livre = document.createElement('div');
            livre.innerHTML = template;
            livre.addEventListener('click', () => {
                window.location.href = `livre?isbn=${isbn}`;
            });
            document.getElementById("searchResult").appendChild(livre);
        });
    }
    else {
        document.getElementById("searchResult").innerHTML = "<br><h2 class='text-center' style='color:white'>Oups, aucun résultat n'a été trouvé.<h2><br><img id='mascotte404' class='img-fluid mx-auto d-block w-25' src='../img/error404.svg' alt='404'>";
    }
});

const searchInput = document.querySelector('input#searchInput');
const searchButton = document.querySelector('button#searchButton');
searchButton.addEventListener('click', async (e) => {
    e.preventDefault(); // evite le rechargement de la page
    const searchValue = searchInput.value.trim();// recupere la valeur de l'input sans les espaces
    if (searchValue) {
      try {
          window.location.href = `search?search=${searchValue}`;
      } catch (error) {
        console.error(error);
      }
    }
  });