const mainTitle = document.getElementById('title');

const searchContainer = document.getElementById('search-container');
const searchInput = document.getElementById('search-input');
const searchButton = document.getElementById('search-button');
const searchResults = document.getElementById('search-results')
const searchLoading = document.getElementById('search-loading')
const searchLoader = document.querySelector('.loader');
const searchLoaderBig = document.querySelector('.loader-big');

function main() {
  searchInput.addEventListener('keyup', function(e) {
    if (e.keyCode == 13) {
      searchButton.click();
    }
  })

  searchButton.onclick = function() {
    if (searchInput.value.length > 1) {
      mainTitle.style.marginTop = '40px';

      searchButton.style.display = 'none';
      searchResults.style.display = 'none';
      searchLoading.style.display = 'block';
      searchLoader.style.display = 'block';
      searchLoaderBig.style.display = 'block';
      searchInput.setAttribute('readonly', 'readonly');

      axios.get(`http://localhost:8080/search/?term=${searchInput.value}`)
        .then(response => {
          searchLoader.style.display = 'none';
          searchLoaderBig.style.display = 'none';
          searchLoading.style.display = 'none';
          searchButton.style.display = 'block';
          searchResults.style.display = 'block';
          searchInput.value = '';
          searchInput.removeAttribute('readonly');

          const { term, results, totalDocuments, totalURLs, uniqueTokens } = response.data;

          const searchTermDOM = document.getElementById('search-term');
          const URLsFoundDOM = document.getElementById('urls-found');
          const totalTokensDOM = document.getElementById('total-tokens');
          const totalDocumentsDOM = document.getElementById('total-documents');

          searchTermDOM.innerHTML = term;
          URLsFoundDOM.innerHTML = totalURLs;
          totalTokensDOM.innerHTML = uniqueTokens;
          totalDocumentsDOM.innerHTML = totalDocuments;

          while (searchResults.lastChild.id !== 'search-info-container') {
              searchResults.removeChild(searchResults.lastChild);
          }

          console.log(response);
          for (let i = 0; i < results.length; ++i) {
            let item = document.createElement('li');
            let URLs = document.createElement('h3');
            let TFIDF = document.createElement('h3');

            const url = results[i][0];
            const tfidf = results[i][1];
            URLs.innerHTML = `URL: <a href='https://${url}'>${url}</a>`;
            TFIDF.innerHTML = `TF-IDF: <span>${tfidf}</span>`;

            item.appendChild(URLs);
            item.append(TFIDF);

            searchResults.appendChild(item);
          }
        })
      .catch(err => console.log(err))
    }
  }
}

searchContainer.style.display = 'none';
searchLoading.style.display = 'block';
searchLoaderBig.style.display = 'block';
mainTitle.style.marginTop = '100px';

axios.get('http://localhost:8080/search/load').then(response => {
  if (response.data.success) {
    mainTitle.style.marginTop = '200px';
    searchContainer.style.display = 'flex';
    searchLoading.style.display = 'none';
    searchLoaderBig.style.display = 'none';
    console.log('loaded...');
    main();
  }
}).catch(err => console.log(err))
