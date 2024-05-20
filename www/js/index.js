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
    let response = await fetch(`${API_URL}/checkLogin?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`);
    let data = await response.json();
    if (data["content"] === 'success') {
      document.getElementById("account").src = "../img/account.svg"
      reponse = await fetch(`${API_URL}/isAdmin?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`);
      reponse = await reponse.json();
      console.log(reponse);
      if ( (reponse.content === "success")) {
          document.getElementById('config').innerHTML = `<img src="../img/smallConfig.svg" alt="Config" class="img-fluid" style="width: 60%;">`;
      } else {
          document.getElementById('config').innerHTML = "";
      }
    } else {
      document.getElementById('config').innerHTML = "";
      document.getElementById("account").src = "../img/login.svg"
    }
}
checkLoginAndGetUserInfo()
async function updateBestLivres() {
  await fetch(`${API_URL}/updateBestLivres`);
  console.log('Best livres updated');
}
updateBestLivres();
console.log('searchButton clicked')
searchButton.addEventListener('click', async (e) => {
  console.log('searchButton clicked')
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
