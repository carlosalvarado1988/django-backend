const loginForm = document.getElementById("login-form");
const searchForm = document.getElementById("search-form");
const contentContainer = document.getElementById("content-container");

const baseEndpoint = "http://localhost:8000/api";
if (loginForm) {
  // handle submit
  loginForm.addEventListener("submit", handleLogin);
}

if (searchForm) {
  // handle submit
  searchForm.addEventListener("submit", handleSearch);
}

// at the load moment.
validateToken();

// Login functions
function handleLogin(event) {
  event.preventDefault();
  let loginDataString = JSON.stringify(
    Object.fromEntries(new FormData(loginForm))
  ); // this methods builds an object for all the elements in the form, very handy as oppose the extract elementById in each one.
  const loginEndpoint = `${baseEndpoint}/token/`;
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: loginDataString,
  };
  fetch(loginEndpoint, options) // request.POST for python
    .then((response) => response.json())
    .then((authData) => {
      handleAuthData(authData, getProductList);
    })
    .catch((error) => {
      console.log(error);
    });
}

// JWT Functions to fetch
function refreshToken() {
  const refreshEndpoint = `${baseEndpoint}/token/refresh`;
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      refresh: localStorage.getItem("refresh"),
    }),
  };
  fetch(refreshEndpoint, options)
    .then((res) => {
      return res.json();
    })
    .then((authData) => {
      if (authData.code && authData.code === "token_not_valid") {
        console.log("🚀 ~ file: client.js:61 ~ .then ~ authData:", authData);
        alert("login again");
      } else {
        handleAuthData(authData, getProductList);
      }
    })
    .catch((error) => {
      console.log(error);
    });
}

function validateToken() {
  console.log("into validateToken");
  const verifyEndpoint = `${baseEndpoint}/token/verify`;
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      token: localStorage.getItem("access"),
    }),
  };
  fetch(verifyEndpoint, options)
    .then((res) => res.json())
    .then((authData) => {
      if (authData.code && authData.code === "token_not_valid") {
        refreshToken();
      } else {
        getProductList();
      }
    })
    .catch((error) => {
      console.log(error);
    });
}

function isTokenNotValid(jsonData) {
  if (jsonData.code && jsonData.code === "token_not_valid") {
    // run refresh token query
    refreshToken();
    return false;
  }
  return true;
}

// Local storage handlers
function handleAuthData(authData, cb) {
  localStorage.setItem("access", authData.access);
  if (authData.refresh) {
    localStorage.setItem("refresh", authData.refresh);
  }
  if (cb) {
    cb();
  }
}

// fetch handlers
function getFetchOptions(method, body) {
  return {
    method: method || "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("access")}`,
    },
    body: body ? body : null,
  };
}

// Product functions
function getProductList() {
  const productsEndpoint = `${baseEndpoint}/products/`;
  const options = getFetchOptions();
  fetch(productsEndpoint, options)
    .then((res) => res.json())
    .then(writeToContainer)
    .catch(console.log);
}

function writeToContainer(data) {
  if (contentContainer) {
    contentContainer.innerHTML =
      "<pre>" + JSON.stringify(data, null, 4) + "</pre>";
  }
}

// handle all regarding search
function handleSearch(event) {
  event.preventDefault();

  let data = Object.fromEntries(new FormData(searchForm));
  let searchParams = new URLSearchParams(data);
  const loginEndpoint = `${baseEndpoint}/search/?${searchParams}`;
  // in this example, authorization is not required.

  const headers = {
    "Content-Type": "application/json",
  };

  // we could  add something to include authorization like this. (in case logged in users can have access to more data, this will depend on the server)
  const authToken = localStorage.getItem("access");
  if (authToken) {
    headers["Authorization"] = `Bearer ${authToken}`;
  }
  const options = {
    method: "GET",
    headers,
  };

  fetch(loginEndpoint, options) // request.POST for python
    .then((res) => {
      return res.json();
    })
    .then((data) => {
      console.log("htis", data.hits);
      // writeToContainer(data);
      // here we improve the render
      const validData = isTokenNotValid(data);
      if (validData && contentContainer) {
        if (data && data.hits) {
          let htmlStr = "";
          for (let results of data.hits) {
            htmlStr += `<li>${result.title}</li>`;
          }
          contentContainer.innerHTML = htmlStr;
          if (data.hits.lenght === 0) {
            contentContainer.innerHTML = "<p>No results found</p>";
          }
        } else {
          contentContainer.innerHTML = "<p>No results found</p>";
        }
      }
    })
    .catch((error) => {
      console.log(error);
    });
}

// instantSearchJS - code snippet copied from their installation guide
// Security issue here, just for testing purposes will leave keys expose like this.
// you should implement an API call to retreive those, or use .env variables
const ALGOLIA_KEYS = {
  id: "G2JJN53YMA",
  key: "50dbba7310ce045d426d9cbcdd1a79aa",
  index_name: "cfe_Product",
};

const searchClient = algoliasearch(ALGOLIA_KEYS.id, ALGOLIA_KEYS.key);

const search = instantsearch({
  indexName: ALGOLIA_KEYS.index_name,
  searchClient,
});

search.addWidgets([
  instantsearch.widgets.searchBox({
    container: "#searchbox",
  }),

  instantsearch.widgets.refinementList({
    container: "#public-filter",
    attribute: "public",
  }),

  instantsearch.widgets.refinementList({
    container: "#owner-filter",
    attribute: "owner",
  }),

  instantsearch.widgets.clearRefinements({
    container: "#clear-filters",
  }),

  instantsearch.widgets.hits({
    container: "#hits",
    templates: {
      item: `<div> {{title}} <p>{{public}}</p> <p>\${{price}}</p> </div>`,
    },
  }),
]);

search.start();
