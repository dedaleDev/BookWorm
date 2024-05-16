const API_URL = 'http://192.168.1.20:8080'

let decodedCookie = decodeURIComponent(document.cookie).split(';');//decodeURIComponent permet de decoder les caractères spéciaux
for (let i = 0; i < decodedCookie.length; i++) {//on parcourt le tableau de cookies
  let c = decodedCookie[i];
  while (c.charAt(0) === ' ') {
    c = c.substring(1);
  }
  if (c.indexOf('email=') === 0) {
    const email = c.substring("email=".length, c.length);
    const password = c.substring("password=".length, c.length);
  }
}

let reponse = await fetch(`${API_URL}/checkLogin?email=${email}&password=${password}`);
const data = await response.json();
if (data["content"] === 'success') {
    document.getElementById('account').style.display = 'block';
    let reponse = await fetch(`${API_URL}/getUserInfo?email=${email}&password=${password}`);
    let userInfo = await reponse.json();
    console.log(userInfo);
    document.getElementById('welcome').innerHTML = `<h1>Bienvenue ${email}</h1>`;
} else {
    document.getElementById('account').style.display = 'none';
    document.getElementById('Error').innerHTML = '<h1>Oups, cette page est réservée aux membres connectés</h1> <a href="/login">Connectez-vous</a>';
}