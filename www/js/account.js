const API_URL = 'http://192.168.1.20:8080';

let userInfo = "";
let email, password;

async function checkLoginAndGetUserInfo() {
    let decodedCookie = decodeURIComponent(document.cookie).split(';');
    for (let i = 0; i < decodedCookie.length; i++) {
        let c = decodedCookie[i].trim();
        if (c.startsWith('email=')) {
            email = c.substring('email='.length);
        }
        if (c.startsWith('password=')) {
            password = c.substring('password='.length);
        }
    }
    const response = await fetch(`${API_URL}/checkLogin?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`);
    const data = await response.json();
    if (data["content"] === 'success') {
        let reponse = await fetch(`${API_URL}/getUserInfo?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`);
        reponse = await reponse.json();
        userInfo = JSON.parse(reponse["content"]);
    } else {
        window.location.href = '/login';
    }
}

let emprunts = "";
async function GetEmprunts() {
    const reponse = await fetch(`${API_URL}/getEmprunt?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`);
    const data = await reponse.json();
    emprunts = JSON.parse(data["content"]);
}

async function GetLivreTitre(isbn) {
    const response = await fetch(`${API_URL}/getLivre?isbn=${encodeURIComponent(isbn)}`);
    const data = await response.json();
    const livreData = JSON.parse(data["content"]);
    return livreData[isbn]["titre"];
}

checkLoginAndGetUserInfo().then(() => {
    console.log("USERINFO", userInfo);
    const userName = userInfo[email]["nom"];
    const formattedUserName = userName.charAt(0).toUpperCase() + userName.slice(1);
    document.getElementById('welcome').innerHTML = `<h1 style="padding-top:5vh;"><a href="/index"> Bienvenue sur BookWorm ${formattedUserName} !<a></h1>`;
    GetEmprunts().then(async () => {
        console.log("EMPRUNTS", emprunts);
        const divEmprunt = document.getElementById('emprunts');
        for (const id of Object.keys(emprunts)) {
            const titre = await GetLivreTitre(emprunts[id]["isbn"]);
            const dateStr = emprunts[id]["Date"]; // votre chaîne de caractères au format YYYY-MM-DD
            const [day, month, year] = dateStr.split("/");
            const today = new Date();
            const date = new Date(`${year}-${month}-${day}`);
            const diffInMilliseconds = Math.abs(today - date);
            const diffInDays = Math.ceil(diffInMilliseconds / (1000 * 3600 * 24));
            if (30-diffInDays < 0) {
                divEmprunt.innerHTML += `<li><h5 style='color:red'>${titre} est en retard de ${diffInDays} jour(s)</h5></li>`;
            } else {
                divEmprunt.innerHTML += `<li><h5 style='color:white'> ${titre} retour attendu dans ${30-diffInDays} jour(s)</h5></li>`;
            }
        }
        let divInfo = document.getElementById('infos')
        divInfo.innerHTML = `<li><h5 style='color:white'> Nom : ${userInfo[email]["nom"]}</h5></li>\
        <li><h5 style='color:white'> Prénom : ${userInfo[email]["prénom"]}</h5></li>\
        <li><h5 style='color:white'> Adresse : ${userInfo[email]["adresse"]}</h5></li>\
        <li><h5 style='color:white'> Tel : ${userInfo[email]["tel"]}</h5></li>\
        `
    });
});