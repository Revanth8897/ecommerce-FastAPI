

/* ================= LOGIN ================= */
async function login() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const formData = new FormData();
  formData.append("username", email);
  formData.append("password", password);

  const res = await fetch(`${API_URL}/login`, {
    method: "POST",
    body: formData
  });

  const data = await res.json();

  if (!res.ok) {
    alert(data.detail || "Login failed");
    return;
  }

localStorage.setItem("token", data.access_token);
localStorage.setItem("is_admin", data.is_admin ? "true" : "false");

console.log("Saved admin:", localStorage.getItem("is_admin"));
window.location.href = "products.html";
}

/* ================= LOGOUT ================= */
function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("cart");
  window.location.href = "login.html";
}

/* ================= REGISTER ================= */
async function register() {
  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const message = document.getElementById("message");

  message.innerText = "";

  if (!name || !email || !password) {
    message.style.color = "red";
    message.innerText = "All fields are required";
    return;
  }

  const response = await fetch(`${API_URL}/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email, password })
  });

  const data = await response.json();

  if (!response.ok) {
    message.style.color = "red";
    message.innerText = data.detail || "Registration failed";
    return;
  }

  message.style.color = "green";
  message.innerText = "Registration successful! Redirecting...";

  setTimeout(() => {
    window.location.href = "login.html";
  }, 1500);
}
