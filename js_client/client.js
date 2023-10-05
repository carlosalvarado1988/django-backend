const loginForm = document.getElementById("login-form");
const baseEndpoint = "http://localhost:8000/api";
if (loginForm) {
  // handle submit
  loginForm.addEventListener("submit", handleLogin);
}

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
    .then((response) => {
      console.log("response:", response);
      return response.json();
    })
    .then((obj) => {
      console.log("obj", obj);
    })
    .catch((error) => {
      console.log(error);
    });
}
