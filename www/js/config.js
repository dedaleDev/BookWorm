const API_URL = 'http://192.168.1.20:8080'

fetch(`${API_URL}/isAdmin?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if (data.content === "success") {
            console.log("Admin")
        } else {
            window.location.href = "/login";
        }
})