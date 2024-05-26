const API_URL = 'http://192.168.1.20:8080'

//clear cookies IF user not admin only 

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

let isAdmin = fetch(`${API_URL}/isAdmin?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`).then(response => response.json()).then(data => {
    if (data["content"] === 'success') {
        isAdmin = true;
    } else {
        isAdmin = false;
    }
});


const emailInput = document.getElementById("email");
emailInput.addEventListener("blur", function() {
    const email = emailInput.value;
    if (email.length === 0 || email.length > 100 || !email.includes('@') || !email.includes('.')) {
        emailInput.classList.add("is-invalid");
    } else {
        emailInput.classList.remove("is-invalid");
    }
}
);

let mdp ="";
const passwordInput = document.getElementById("mdp");
passwordInput.addEventListener("blur", function() {
    mdp = passwordInput.value;
    if (mdp.length === 0 || mdp.length > 100) {
        passwordInput.classList.add("is-invalid");
    } else {
        passwordInput.classList.remove("is-invalid");
    }
}
);
let mdp2 = "";
const confPasswordInput = document.getElementById("mdp2");
confPasswordInput.addEventListener("blur", function() {
    mdp2  = confPasswordInput.value;
    console.log(mdp2, mdp);
    if (mdp2 !== mdp) {
        confPasswordInput.classList.add("is-invalid");
    } else {
        confPasswordInput.classList.remove("is-invalid");
    }
}
);

const nomInput = document.getElementById("nom");
nomInput.addEventListener("blur", function() {
    const nom = nomInput.value;
    if (nom.length === 1 || nom.length > 20) {
        nomInput.classList.add("is-invaxlid");
    } else {
        nomInput.classList.remove("is-invalid");
    }
}
);

const prenomInput = document.getElementById("prenom");
prenomInput.addEventListener("blur", function() {
    const prenom = prenomInput.value;
    if (prenom.length === 1 || prenom.length > 100) {
        prenomInput.classList.add("is-invalid");
    } else {
        prenomInput.classList.remove("is-invalid");
    }
}
);

const adresseInput = document.getElementById("adresse");
adresseInput.addEventListener("blur", function() {
    const adresse = adresseInput.value;
    if (adresse.length === 1 || adresse.length > 120) {
        adresseInput.classList.add("is-invalid");
    } else {
        adresseInput.classList.remove("is-invalid");
    }
}
);

const telInput = document.getElementById("tel");
telInput.addEventListener("blur", function() {
    const tel = telInput.value;
    if (tel.length === 0 || tel.length > 10) {
        telInput.classList.add("is-invalid");
    } else {
        telInput.classList.remove("is-invalid");
    }
}
);

function validateForm() {
    //return true if all fields are valid, false otherwise
    try {
        const email = document.getElementById('email').value;
        const mdp = document.getElementById('mdp').value;
        const confPassword = document.getElementById('mdp2').value;
        const nom = document.getElementById('nom').value;
        const prenom = document.getElementById('prenom').value;
        const adresse = document.getElementById('adresse').value;
        const tel = document.getElementById('tel').value;
        console.log(email, mdp, confPassword, nom, prenom, adresse, tel);
        if (email.length <= 0 || email.length > 100 || !email.includes('@') || !email.includes('.')) return false;
        if (mdp.length <= 0 || mdp.length > 100) return false;
        if (confPassword !== mdp) return false;
        if (nom.length <= 0 || nom.length > 20) return false;
        if (prenom.length <= 0 || prenom.length > 100) return false;
        if (adresse.length <= 0 || adresse.length > 120) return false;
        if (tel.length <= 0 || tel.length > 10) return false;
        return true;
    } catch (e) {
        console.error(e);
        return false;
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const addButton = document.getElementById('submit');
    addButton.addEventListener('click', async (e) => {
        e.preventDefault();
        if (validateForm()) {
            const email = document.getElementById('email').value;
            const mdp = document.getElementById('mdp').value;
            console.log(mdp);
            const nom = document.getElementById('nom').value;
            const prenom = document.getElementById('prenom').value;
            const adresse = document.getElementById('adresse').value;
            const tel = document.getElementById('tel').value;
            const formData = new FormData();
            formData.append('email', email);
            formData.append('mdp', mdp);
            formData.append('nom', nom);
            formData.append('prenom', prenom);
            formData.append('adresse', adresse);
            formData.append('tel', tel);
            console.log("READY TO SEND")
            const response = await fetch(`${API_URL}/newUser`, {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            console.log(data);
            if (data["content"] === 'success') {
                alert('Le compte a bien été créé. Bienvenue sur BookWorm ! ');
                if (!isAdmin)
                    window.location.href = '/login';
                else {
                    window.location.href = '/config';
                }
            } else {
                alert('Erreur lors de la création du compte' + data["message"]);
            }
        } else {
            alert('Veuillez remplir correctement tous les champs du formulaire');
        }
    });
});