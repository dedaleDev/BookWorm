const API_URL = 'http://192.168.1.20:8080'

async function checkLoginAndGetUserInfo() {
  let decodedCookie = decodeURIComponent(document.cookie).split(';');
  let email, password;
  for (let i = 0; i < decodedCookie.length; i++) {
      let c = decodedCookie[i];
      while (c.charAt(0) === ' ') {
          c = c.substring(1);
      }
      if (c.indexOf('email=') === 0) {
          email = c.substring("email=".length, c.length);
      }
      if (c.indexOf('password=') === 0) {
          password = c.substring("password=".length, c.length);
      }
  }
  if (email && password) {
      let response = await fetch(`${API_URL}/checkLogin?email=${email}&password=${password}`);
      const data = await response.json();
      if (data["content"] === 'success') {
        window.location.href = '/account';
      }
  }
}

checkLoginAndGetUserInfo();
const signupButton = document.getElementById('signupButton');
const signinButton = document.getElementById('signinButton');

signinButton.addEventListener('click', async (e) => {
  e.preventDefault(); // evite le rechargement de la page
  const email = document.getElementById('inputEmail3').value;
  const password = document.getElementById('inputPassword3').value;
  if (email && password) {
    try {
      const response = await fetch(`${API_URL}/checkLogin?email=${email}&password=${password}`);
      const data = await response.json();
      console.log(data, data.data);
      if (data["content"] === 'success') {
        console.log('success');
        document.cookie = `email=${email}`;//pas sécurisé mais bon
        document.cookie = `password=${password}`;
        window.location.href = '/account';
      } else {
        document.getElementById('error').innerText =data.message;
        document.getElementById('error').style.display = 'block';
      }
    } catch (error) {
      console.error(error);
    }
  }
})
