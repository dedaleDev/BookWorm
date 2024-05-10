
const API_URL = 'http://127.0.0.1:8080'
const searchInput = document.querySelector('input.form-control');
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
