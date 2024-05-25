const API_URL = 'http://192.168.1.20:8080';
const searchInput = document.querySelector('input.form-control');
const searchButton = document.querySelector('button#searchButton');

let email, password;

async function getCookieValue(name) {
    const cookieString = decodeURIComponent(document.cookie);
    const cookies = cookieString.split(';');
    for (let cookie of cookies) {
        let [key, value] = cookie.trim().split('=');
        if (key === name) {
            return value;
        }
    }
    return null;
}

async function checkLoginAndGetUserInfo() {
    try {
        email = await getCookieValue('email');
        password = await getCookieValue('password');
        const response = await fetch(`${API_URL}/checkLogin?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`);
        const data = await response.json();
        if (data.content === 'success') {
            document.getElementById("account").src = "../img/account.svg";
            const adminResponse = await fetch(`${API_URL}/isAdmin?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`);
            const adminData = await adminResponse.json();
            if (adminData.content === "success") {
                document.getElementById('config').innerHTML = `<img src="../img/smallConfig.svg" alt="Config" class="img-fluid" style="width: 60%;">`;
            } else {
                document.getElementById('config').innerHTML = "";
            }
        } else {
            document.getElementById('config').innerHTML = "";
            document.getElementById("account").src = "../img/login.svg";
        }
    } catch (error) {
        console.error('Error checking login and fetching user info:', error);
        document.getElementById('config').innerHTML = "";
        document.getElementById("account").src = "../img/login.svg";
    }
}

async function updateBestLivres() {
    try {
        await fetch(`${API_URL}/updateBestLivres`);
        console.log('Best livres updated');
    } catch (error) {
        console.error('Error updating best livres:', error);
    }
}

function initialize() {
    checkLoginAndGetUserInfo();
    updateBestLivres();
}

searchButton.addEventListener('click', async (e) => {
    e.preventDefault();
    const searchValue = searchInput.value.trim();
    if (searchValue) {
        try {
            window.location.href = `search?search=${encodeURIComponent(searchValue)}&type=Livre`;
        } catch (error) {
            console.error('Error navigating to search:', error);
        }
    }
});

initialize();