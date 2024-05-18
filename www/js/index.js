const API_URL = 'http://192.168.1.20:8080'
const searchInput = document.querySelector('input.form-control');
const searchButton = document.querySelector('button#searchButton');


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
      document.getElementById("account").src = "../img/account.svg"
    }
}
checkLoginAndGetUserInfo()
async function updateBestLivres() {
  await fetch(`${API_URL}/updateBestLivres`);
}
updateBestLivres();
searchButton.addEventListener('click', async (e) => {
  e.preventDefault(); // evite le rechargement de la page
  const searchValue = searchInput.value.trim();// recupere la valeur de l'input sans les espaces
  if (searchValue) {
    try {
        window.location.href = `search?search=${searchValue}&type=Livre`;
    } catch (error) {
      console.error(error);
    }
  }
});
