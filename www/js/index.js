const API_URL = '';
const searchInput = document.querySelector('input.form-control');
const searchButton = document.querySelector('button#searchButton');

searchButton.addEventListener('click', async (e) => {
  console.log("searchButton clicked");
  e.preventDefault(); // prevent default form submission
  console.log("searchInput.value : ", searchInput.value);
  const searchValue = searchInput.value.trim();
  if (searchValue) {
    try {
      console.log("API_URL : ", API_URL);
      const response = await fetch("/search", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ searchValue })
      });
    } catch (error) {
      console.error(error);
    }
  }
});