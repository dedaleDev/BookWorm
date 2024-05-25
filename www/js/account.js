const API_URL = 'http://192.168.1.20:8080';

let userInfo = "";
let email, password;

async function checkLoginAndGetUserInfo() {
    try {
        let decodedCookie = decodeURIComponent(document.cookie).split(';');
        for (let cookie of decodedCookie) {
            let c = cookie.trim();
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
            let userInfoResponse = await fetch(`${API_URL}/getUserInfo?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`);
            let userInfoData = await userInfoResponse.json();
            userInfo = JSON.parse(userInfoData["content"]);
            let adminResponse = await fetch(`${API_URL}/isAdmin?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`);
            let adminData = await adminResponse.json();
            if (adminData.content === "success") {
                document.getElementById('config').innerHTML = `<img src="../img/bigConfig.svg" class="img-fluid" style="width:40%; padding-top: 2vh;">`;
            }
        } else {
            window.location.href = '/login';
        }
    } catch (error) {
        console.error('Error checking login and fetching user info:', error);
        window.location.href = '/login';
    }
}

let emprunts = "";
async function getEmprunts() {
    try {
        const response = await fetch(`${API_URL}/getEmprunt?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`);
        const data = await response.json();
        if (data["status"] === "error") {
            emprunts = {};
            return;
        }
        emprunts = JSON.parse(data["content"]);
    } catch (error) {
        console.error('Error fetching emprunts:', error);
    }
}

async function getLivreTitre(isbn) {
    try {
        const response = await fetch(`${API_URL}/getLivre?isbn=${encodeURIComponent(isbn)}`);
        const data = await response.json();
        const livreData = JSON.parse(data["content"]);
        return livreData[isbn]["titre"];
    } catch (error) {
        console.error(`Error fetching book title for ISBN ${isbn}:`, error);
        return 'Unknown Title';
    }
}

checkLoginAndGetUserInfo().then(() => {
    try {
        console.log("USERINFO", userInfo);
        const userName = userInfo[email]["nom"];
        const formattedUserName = userName.charAt(0).toUpperCase() + userName.slice(1);
        document.getElementById('welcome').innerHTML = `<h1 style="padding-top:5vh;"><a href="/index"> Bienvenue sur BookWorm ${formattedUserName} !</a></h1>`;
        getEmprunts().then(async () => {
            console.log("EMPRUNTS", emprunts);
            const divEmprunt = document.getElementById('emprunts');
            if (Object.keys(emprunts).length === 0) {
                divEmprunt.innerHTML = `<li><h5 style='color:white'> Vous n'avez pas d'emprunt en cours</h5></li>`;
            } else {
                for (const id of Object.keys(emprunts)) {
                    const titre = await getLivreTitre(emprunts[id]["isbn"]);
                    const dateStr = emprunts[id]["Date"];
                    const [day, month, year] = dateStr.split("/");
                    const today = new Date();
                    const date = new Date(`${year}-${month}-${day}`);
                    const diffInMilliseconds = Math.abs(today - date);
                    const diffInDays = Math.ceil(diffInMilliseconds / (1000 * 3600 * 24));
                    if (30 - diffInDays < 0) {
                        divEmprunt.innerHTML += `<li><h5 style='color:red'>${titre} est en retard de ${diffInDays} jour(s)</h5></li>`;
                    } else {
                        divEmprunt.innerHTML += `<li><h5 style='color:white'> ${titre} retour attendu dans ${30 - diffInDays} jour(s)</h5></li>`;
                    }
                }
            }
            let divInfo = document.getElementById('infos');
        divInfo.innerHTML = `<li><h5 style='color:white'> Nom : ${userInfo[email]["nom"]}</h5></li>\
        <li><h5 style='color:white'> Prénom : ${userInfo[email]["prénom"]}</h5></li>\
        <li><h5 style='color:white'> Adresse : ${userInfo[email]["adresse"]}</h5></li>\
        <li><h5 style='color:white'> Tel : ${userInfo[email]["tel"]}</h5></li>\
        `
        });
    } catch (error) {
        console.log(error)
    }
});

logout.addEventListener('click', () => {
    document.cookie = "email=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/";
    document.cookie = "password=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/";
    console.log("deconnexion")
    window.location.href = '/index'
})