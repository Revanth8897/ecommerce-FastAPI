const res = await fetch("http://127.0.0.1:8000/login", {
  method: "POST",
  headers: {
    "Content-Type": "application/x-www-form-urlencoded"
  },
  body: new URLSearchParams({
    username: email,
    password: password
  })
});

const data = await res.json();
// AFTER successful login
localStorage.setItem("token", data.access_token);
localStorage.setItem("is_admin", data.is_admin ? "true" : "false");

console.log("Saved admin:", localStorage.getItem("is_admin"));

window.location.href = "products.html";
