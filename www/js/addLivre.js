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

const isbnInput = document.getElementById("isbn");
isbnInput.addEventListener("blur", function() {
  const isbn = isbnInput.value;
  let isValid = false;
  if (isbn.length === 10 || isbn.length === 13) {
    for (let i = 0; i < isbn.length; i++) {
      if (isNaN(parseInt(isbn[i]))) {
        isValid = false;
        break;
      } else {
        isValid = true;
      }
    }
  }
  if (!isValid) {
    isbnInput.classList.add("is-invalid");
  } else {
    isbnInput.classList.remove("is-invalid");
  }
});

const titreInput = document.getElementById("titre");
titreInput.addEventListener("blur", function() {
  const titre = titreInput.value;
  if (titre.length === 1 || titre.length > 100) {
    titreInput.classList.add("is-invalid");
  } else {
    titreInput.classList.remove("is-invalid");
  }
});

const descriptionInput = document.getElementById("description");
descriptionInput.addEventListener("blur", function() {
  const description = descriptionInput.value;
  if (description.length === 1 || description.length > 1000) {
    descriptionInput.classList.add("is-invalid");
  } else {
    descriptionInput.classList.remove("is-invalid");
  }
});

const noteInput = document.getElementById("note");
noteInput.addEventListener("blur", function() {
  const note = noteInput.value;
  if (note < 0 || note > 10) {
    noteInput.classList.add("is-invalid");
  } else {
    noteInput.classList.remove("is-invalid");
  }
});


const prixInput = document.getElementById("prix");
prixInput.addEventListener("blur", function() {
  const prix = prixInput.value;
  if (prix < 0) {
    prixInput.classList.add("is-invalid");
  } else {
    prixInput.classList.remove("is-invalid");
  }
});

function validateForm() {
  //return true if all fields are valid, false otherwise
  try {
    console.log("VALIDATING FORM")
    const isbn = document.getElementById('isbn').value;
    const titre = document.getElementById('titre').value;
    const auteur = document.getElementById('auteur').value;
    const description = document.getElementById('description').value;
    const note = document.getElementById('note').value;
    const dateParution = document.getElementById('dateParution').value;
    const statut = document.getElementById('statut').value;
    const genre = document.getElementById('genre').value;
    const format = document.getElementById('format').value;
    const prix = document.getElementById('prix').value;
    const pointDeVente = document.getElementById('pointDeVente').value;
    const editeur = document.getElementById('editeur').value;
    const image = document.getElementById('image').files[0];
    console.log(isbn, titre, auteur, description, note, dateParution, statut, genre, format, prix, pointDeVente, editeur, image)
    // Vérifiez chaque valeur et retournez false si l'une d'elles est invalide
    console.log(isbn.length)
    if (isbn.length < 10 || isbn.length > 13) return false;
    console.log(titre.length)
    if (titre.length < 1 || titre.length > 100) return false;
    console.log(description.length)
    if (description.length < 1 || description.length > 1000) return false;
    console.log(note)
    if (note < 0 || note > 10) return false;
    console.log(prix)
    if (prix < 0) return false;
    console.log(auteur, dateParution, statut, genre, format, pointDeVente, editeur, image)
    if (!auteur || !dateParution || !statut || !genre || !format || !pointDeVente || !editeur || !image) return false;
    console.log("VALID FORM")
    return true;
  } catch (e) {
    console.error(e);
    return false;
  }
}



document.addEventListener("DOMContentLoaded", function() {
    const dropzone = document.querySelector(".dropzone");
    const input = document.querySelector("#image");
    const preview = document.querySelector("#image-preview");
  
    dropzone.addEventListener("dragover", function(event) {
      event.preventDefault();
      dropzone.classList.add("dz-dragging");
    });
  
    dropzone.addEventListener("dragleave", function(event) {
      dropzone.classList.remove("dz-dragging");
    });
  
    dropzone.addEventListener("drop", function(event) {
      event.preventDefault();
      dropzone.classList.remove("dz-dragging");
      const file = event.dataTransfer.files[0];
      input.files = event.dataTransfer.files;
      previewImage(file);
    });
  
    input.addEventListener("change", function(event) {
      const file = input.files[0];
      previewImage(file);
    });
  
    function previewImage(file) {
      const reader = new FileReader();
      reader.onload = function(event) {
        const img = document.createElement("img");
        img.src = event.target.result;
        preview.innerHTML = "";
        preview.appendChild(img);
      };
      reader.readAsDataURL(file);
    }
  });

_templateEltDropDown = `<option value="{{ elt }}">{{ elt }}</option>`

async function form() {
    let response = await fetch(`${API_URL}/getAllNomAuteur`);
    let data = await response.json();
    const auteurs = JSON.parse(data["content"]);
    response = await fetch(`${API_URL}/getAllPointDeVentes`);
    data = await response.json();
    const pointDeVentes = JSON.parse(data["content"]);
    response = await fetch(`${API_URL}/getAllEditeurs`);
    data = await response.json();
    const editeurs = JSON.parse(data["content"]);
    let allAuteur = "";
    Object.keys(auteurs).forEach(id => {
        if (auteurs[id]["alias"] == null) {
            allAuteur += _templateEltDropDown.replace("{{ elt }}",id).replace("{{ elt }}",auteurs[id]["prénom"] +" " + auteurs[id]["nom"]);
        } else {
            allAuteur += _templateEltDropDown.replace("{{ elt }}",id).replace("{{ elt }}",auteurs[id]["alias"]);
        }
    });
    document.getElementById("auteur").innerHTML += allAuteur;
    let allPointDeVentes = "";
    Object.keys(pointDeVentes).forEach(adresse => {
        allPointDeVentes += _templateEltDropDown.replace("{{ elt }}",adresse).replace("{{ elt }}",pointDeVentes[adresse]["nom"]+ " - " +adresse);
    });
    document.getElementById("pointDeVente").innerHTML += allPointDeVentes;
    let allEditeurs = "";
    console.log(editeurs)
    Object.keys(editeurs).forEach(nom => {
      allEditeurs += _templateEltDropDown.replace("{{ elt }}",nom).replace("{{ elt }}",nom);
    });
    document.getElementById("editeur").innerHTML += allEditeurs;
    const addButton = document.getElementById('submit');
    addButton.addEventListener('click', async (e) => {
      e.preventDefault();
      console.log("CLICKED")
      if (validateForm()) {
        const isbn = document.getElementById('isbn').value;
        const titre = document.getElementById('titre').value;
        const auteur = document.getElementById('auteur').value;
        const description = document.getElementById('description').value;
        const note = document.getElementById('note').value;
        const dateParution = document.getElementById('dateParution').value;
        const statut = document.getElementById('statut').value;
        const genre = document.getElementById('genre').value;
        const format = document.getElementById('format').value;
        const prix = document.getElementById('prix').value;
        const pointDeVente = document.getElementById('pointDeVente').value;
        const editeur = document.getElementById('editeur').value;
        const image = document.getElementById('image').files[0];
        const formData = new FormData();
        formData.append('isbn', isbn);
        formData.append('titre', titre);
        formData.append('auteur', auteur);
        formData.append('description', description);
        formData.append('note', note);
        formData.append('dateParution', dateParution);
        formData.append('statut', statut);
        formData.append('genre', genre);
        formData.append('format', format);
        formData.append('prix', prix);
        formData.append('pointDeVente', pointDeVente);
        formData.append('editeur', editeur);
        formData.append('image', image);
        formData.append('email', email);
        formData.append('password', password);
        console.log("READY TO SEND FORM DATA")
        const response = await fetch(`${API_URL}/newLivre`, {
          method: 'POST',
          body: formData
        });
        const data = await response.json();
        console.log(data);
        if (data["content"] === 'success') {
          alert('Le livre a bien été ajouté');
          window.location.href = '/config';
        } else {
          alert('Erreur lors de l\'ajout du livre : ' + data["message"]);
        }
      } else {
        alert('Veuillez remplir correctement tous les champs du formulaire');
      }
    });
}
form();