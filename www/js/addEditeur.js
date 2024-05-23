const API_URL = 'http://192.168.1.20:8080'
//Editeur : Nom address

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

const addressInput = document.getElementById("address");
addressInput.addEventListener("blur", function() {
    const address = addressInput.value;
    if (address.length < 1 || address.length > 120) {
        addressInput.classList.add("is-invalid");
    }
    else {
        addressInput.classList.remove("is-invalid");
    }
}
);

function validateForm() {
    //return true if all fields are valid, false otherwise
    try {
        const nom = document.getElementById('nom').value;
        const address = document.getElementById('address').value;
        if (nom.length === 1 || nom.length > 20) return false;
        if (address.length === 1 || address.length > 120) return false;
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
            const address = document.getElementById('address').value;
            const formData = new FormData();
            formData.append('nom', nom);
            formData.append('address', address);
            formData.append('email', email);
            formData.append('password', password);
            const response = await fetch(`${API_URL}/newEditeur`, {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            if (data["content"] === 'success') {
                alert('L\'éditeur a bien été ajouté');
                //window.location.href = '/config';
            } else {
                alert('Erreur lors de l\'ajout de l\'éditeur' + data["message"]);
            }
        } else {
            alert('Veuillez remplir correctement tous les champs du formulaire');
        }
    });
});