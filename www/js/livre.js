const API_URL = 'http://192.168.1.20:8080';

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
                document.getElementById('config').innerHTML = `<img src="../img/smallConfig.svg" alt="Config" class="img-fluid" style="width: 60%;">`;
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


var _template = `
    <div class='row justify-content-center'>
        <div class='col-md-10' style='padding-top: 3vh'>
            <div class='card mb-3'>
                <h2 class='card-header'>{{ titre }}</h2>
                <div class='card-body'>
                    <ul class='list-group list-group-flush'>
                        <li class='list-group-item'>
                            <strong>
                                <a href='/search?search={{ auteur }}&type=Auteur'>
                                    <h3>{{ auteur }}</h3>
                                </a>
                            </strong>
                        </li>
                        <li class='list-group-item'>
                            <img class='img-fluid align-middle' style='width: 22%;' src='/img/stars/star{{ note }}.svg'>
                            <span class='align-middle'> ({{ NoteEx }})</span>
                        </li>
                        <li class='list-group-item'>Date de parution : {{ dateDeParution }}</li>
                        <li class='list-group-item'><i>{{ genre }}</i></li>
                        <li class='list-group-item'>{{ description }}</li>
                        <li class='list-group-item'>Format : {{ format }}</li>
                        <li class='list-group-item'>En vente chez {{ pointDeVenteName }} ({{ pointDeVente }}) à {{ prix }} €</li>
                        <li class='list-group-item'>Editeur : {{ editeur }}</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
`;

async function loadLivre(isbn) {
    console.log("livre: ", isbn);
    let response = await fetch(`${API_URL}/getLivre?isbn=${isbn}`);
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
        
        let template = _template
            .replace("{{ titre }}", livreData.titre)
            .replace("{{ auteur }}", livreData.auteur)
            .replace("{{ auteur }}", livreData.auteur)
            .replace("{{ note }}", Math.round(livreData.note))
            .replace("{{ dateDeParution }}", livreData.dateDeParution)
            .replace("{{ genre }}", livreData.genre)
            .replace("{{ description }}", livreData.description)
            .replace("{{ format }}", livreData.format)
            .replace("{{ pointDeVente }}", livreData.pointDeVente)
            .replace("{{ prix }}", livreData.prix)
            .replace("{{ editeur }}", livreData.editeur)
            .replace("{{ pointDeVenteName }}", livreData.pointDeVenteName)
            .replace("{{ NoteEx }}", livreData.note);

        document.getElementById("LivreInfo").innerHTML += template;
        document.getElementById("imgLivre").src = `img/livres/${isbn}.jpg`;

        let status = '';
        if (livreData.status === "emprunté") {
            status = "borrowed";
        } else if (livreData.status === "disponible") {
            status = "available";
        } else if (livreData.status === "hors stock") {
            status = "outOfStock";
        }
        if (status) {
            document.getElementById("status").innerHTML = `<img class='img-fluid mx-left d-block' style='width: 70%; padding-top: 2vh' src='img/${status}.svg'>`;
        }

        if (livreData.status === "disponible") {
            document.getElementById("reserver").innerHTML = `<button class='btn btn-primary' style="background-color:#FF8C42;">Réserver</button>`;
            document.getElementById("reserver").addEventListener("click", function () {
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

                fetch(`${API_URL}/checkLogin?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.content === "success") {
                        if (confirm("Êtes-vous sûr de vouloir réserver ce livre ?")) {
                            fetch(`${API_URL}/reserveLivre?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}&isbn=${isbn}`)
                            .then(response => response.json())
                            .then(data => {
                                if (data.content === "success") {
                                    window.location.href = "/login";
                                } else {
                                    alert("Erreur lors de la réservation");
                                }
                            });
                        }
                    } else {
                        window.location.href = "/login";
                    }
                })
            });
        }
        const noteInput = document.getElementById("inputNote");
        const noteButton = document.getElementById("buttonNote");
        noteButton.addEventListener("click", function () {
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
            fetch(`${API_URL}/checkLogin?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`)
            .then(response => response.json())
            .then(data => {
                if (data.content === "success") {
                    console.log("note: ", noteInput.value, isbn);
                    fetch(`${API_URL}/addNote?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}&isbn=${isbn}&note=${noteInput.value}`)
                    .then(response => response.json())
                    .then(data => {
                        console.log("data: ", data)
                        if (data.message === "Vous avez déjà noté ce livre !"){
                            alert("Vous avez déjà noté ce livre !");
                        } else if (data.content === "success") {
                            alert("Note ajoutée avec succès");
                            window.location.reload();
                        } else {
                            alert("Erreur lors de l'ajout de la note");
                        }
                    });
                } else {
                    window.location.href = "/login";
                }
            })
        });
    }
})