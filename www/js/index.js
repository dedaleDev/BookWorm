const API_URL = 'http://127.0.0.1:8092/api';
const searchInput = document.querySelector('input.form-control');
const searchButton = document.querySelector('button#searchButton');

searchButton.addEventListener('click', async (e) => {
    e.preventDefault(); // prevent default form submission
    const searchValue = searchInput.value.trim();
    if (searchValue) {
      try {
        const response = await fetch(`${API_URL}/search`, {
          method: 'GET',
          params: { search: searchValue }
        });
        const data = await response.json();
        console.log(data); // handle the response data
      } catch (error) {
        console.error(error);
      }
    }
  });