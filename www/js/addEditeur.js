const API_URL = 'http://192.168.1.20:8080'

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

const nomInput = document.getElementById("nom");
nomInput.addEventListener("blur", function() {
    const nom = nomInput.value;
    if (nom.length < 1 || nom.length > 20) {
        nomInput.classList.add("is-invalid");
    }
    else {
        nomInput.classList.remove("is-invalid");
    }
});

const adresseInput = document.getElementById("adresse");
adresseInput.addEventListener("blur", function() {
    const adresse = adresseInput.value;
    if (adresse.length < 1 || adresse.length > 120) {
        adresseInput.classList.add("is-invalid");
    }
    else {
        adresseInput.classList.remove("is-invalid");
    }
}
);

function validateForm() {
    //return true if all fields are valid, false otherwise
    try {
        const nom = document.getElementById('nom').value;
        const adresse = document.getElementById('adresse').value;
        if (nom.length === 1 || nom.length > 20) return false;
        if (adresse.length === 1 || adresse.length > 120) return false;
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
            const nom = document.getElementById('nom').value;
            const adresse = document.getElementById('adresse').value;
            const formData = new FormData();
            formData.append('nom', nom);
            formData.append('adresse', adresse);
            formData.append('email', email);
            formData.append('password', password);
            const response = await fetch(`${API_URL}/newEditeur`, {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            if (data["content"] === 'success') {
                alert('L\'éditeur a bien été ajouté');
                window.location.href = '/config';
            } else {
                alert('Erreur lors de l\'ajout de l\'éditeur' + data["message"]);
            }
        } else {
            alert('Veuillez remplir correctement tous les champs du formulaire');
        }
    });
});