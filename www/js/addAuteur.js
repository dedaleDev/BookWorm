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
  if (nom.length === 1 || nom.length > 20) {
    nomInput.classList.add("is-invalid");
  } else {
    nomInput.classList.remove("is-invalid");
  }
});

const prenomInput = document.getElementById("prenom");
prenomInput.addEventListener("blur", function() {
  const prenom = prenomInput.value;
  if (prenom.length === 1 || prenom.length > 100) {
    prenomInput.classList.add("is-invalid");
  } else {
    prenomInput.classList.remove("is-invalid");
  }
});

const aliasInput = document.getElementById("alias");
aliasInput.addEventListener("blur", function() {
  const alias = aliasInput.value;
  if (alias.length > 20) {
    aliasInput.classList.add("is-invalid");
  } else {
    aliasInput.classList.remove("is-invalid");
  }
});

const biographieInput = document.getElementById("biographie");
biographieInput.addEventListener("blur", function() {
  const biographie = biographieInput.value;
  if (biographie.length === 1 || biographie.length > 1000) {
    biographieInput.classList.add("is-invalid");
  } else {
    biographieInput.classList.remove("is-invalid");
  }
});

const dateNaissanceInput = document.getElementById("dateNaissance");
dateNaissanceInput.addEventListener("blur", function() {
  const dateNaissance = dateNaissanceInput.value;
  if (dateNaissance.length === 0) {
    dateNaissanceInput.classList.add("is-invalid");
  } else {
    dateNaissanceInput.classList.remove("is-invalid");
  }
});

const dateDecesInput = document.getElementById("dateDeces");
dateDecesInput.addEventListener("blur", function() {
  const dateDeces = dateDecesInput.value;
  if (dateDeces.length === 0) {
    dateDecesInput.classList.add("is-invalid");
  } else {
    dateDecesInput.classList.remove("is-invalid");
  }
});


function validateForm() {
  //return true if all fields are valid, false otherwise
  try {
    const nom = document.getElementById('nom').value;
    const prenom = document.getElementById('prenom').value;
    const alias = document.getElementById('alias').value;
    const biographie = document.getElementById('biographie').value;
    const dateNaissance = document.getElementById('dateNaissance').value;
    const dateDeces = document.getElementById('dateDeces').value;
    if (nom.length === 1 || nom.length > 100) return false;
    if (prenom.length === 1 || prenom.length > 100) return false;
    if (alias.length > 100) return false;
    if (biographie.length === 1 || biographie.length > 1000) return false;
    if (dateNaissance.length === 0) return false;
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
        const nom = document.getElementById('nom').value;
        const prenom = document.getElementById('prenom').value;
        const alias = document.getElementById('alias').value;
        const biographie = document.getElementById('biographie').value;
        const dateNaissance = document.getElementById('dateNaissance').value;
        const dateDeces = document.getElementById('dateDeces').value || null;
        const formData = new FormData();
        formData.append('nom', nom);
        formData.append('prenom', prenom);
        formData.append('alias', alias);
        formData.append('biographie', biographie);
        console.log("DATE DE NAISSANCE: " + dateNaissance)
        formData.append('dateNaissance', dateNaissance);
        formData.append('dateDeces', dateDeces);
        formData.append('email', email);
        formData.append('password', password);
        console.log("REQUEST: " + formData)
        const response = await fetch(`${API_URL}/newAuteur`, {
            method: 'POST',
        body: formData
        });
        const data = await response.json();
        if (data["content"] === 'success') {
          window.location.href = '/config';
        } else {
          alert('Erreur lors de l\'ajout de l\'auteur : ' + data["message"]);
        }
      } else {
        alert('Veuillez remplir correctement tous les champs du formulaire');
      }
    });
});