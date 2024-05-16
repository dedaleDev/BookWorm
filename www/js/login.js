const API_URL = 'http://192.168.1.20:8080'

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
