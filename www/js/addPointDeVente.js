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
    console.log(nom, nom.length);
    if (nom.length === 1 || nom.length > 20) {
        nomInput.classList.add("is-invalid");
    } else {
        nomInput.classList.remove("is-invalid");
    }
});

const urlInput = document.getElementById("url");
urlInput.addEventListener("blur", function() {
    const url = urlInput.value;
    if (url.length === 1 || url.length > 50) {
        urlInput.classList.add("is-invalid");
    } else {
        urlInput.classList.remove("is-invalid");
    }
});

const telInput = document.getElementById("tel");
telInput.addEventListener("blur", function() {
    const tel = telInput.value;
    if (tel.length === 0 || tel.length > 10) {
        telInput.classList.add("is-invalid");
    } else {
        telInput.classList.remove("is-invalid");
    }
});

function validateForm() {
    //return true if all fields are valid, false otherwise
    try {
        const adresse = document.getElementById('adresse').value;
        const nom = document.getElementById('nom').value;
        const url = document.getElementById('url').value;
        const tel = document.getElementById('tel').value || null;
        if (adresse.length === 1 || adresse.length > 120) return false;
        if (nom.length === 1 || nom.length > 20) return false;
        if (url.length === 1 || url.length > 50) return false;
        return true;
    } catch (e) {
        console.error(e);
        return false;
    }
}

document.addEventListener("DOMContentLoaded", function() {
    const addButton = document.getElementById('submit');
    addButton.addEventListener('click', async (e) => {
        e.preventDefault();
        if (validateForm()) {
            const adresse = document.getElementById('adresse').value;
            const nom = document.getElementById('nom').value;
            const url = document.getElementById('url').value;
            const tel = document.getElementById('tel').value || null;
            const formData = new FormData();
            formData.append('adresse', adresse);
            formData.append('nom', nom);
            formData.append('url', url);
            formData.append('tel', tel);
            formData.append('email', email);
            formData.append('password', password);
            console.log("READY TO SEND", formData)
            const response = await fetch(`${API_URL}/newPointDeVente`, {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            if (data["content"] === 'success') {
                alert('Le point de vente a bien été ajouté');
                window.location.href = '/config';
            } else {
                alert('Erreur lors de l\'ajout du point de vente' + data["message"]);
            }
        } else {
            alert('Veuillez remplir correctement tous les champs du formulaire');
        }
    });
});