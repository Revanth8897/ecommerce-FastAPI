
async function addToCart(productId) {
  const token = localStorage.getItem("token");

  if (!token) {
    alert("Please login first");
    window.location.href = "login.html";
    return;
  }

  const res = await fetch(`${API_URL}/cart`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify({
      product_id: productId,
      quantity: 1
    })
  });

  const data = await res.json();

  if (!res.ok) {
    alert(data.detail || "Failed to add to cart");
    return;
  }

  alert("Added to cart 🛒");
}

function goToCart() {
  window.location.href = "cart.html";
}

// for products visible

async function loadProducts() {
  const res = await fetch(`${API_URL}/products/`);
  const products = await res.json();

  const container = document.getElementById("products");
  container.innerHTML = "";

  products.forEach(p => {
    container.innerHTML += `
      <div class="product">
        <h3>${p.name}</h3>
        <p>₹${p.price}</p>
        <button onclick="addToCart(${p.id})">Add to Cart</button>
      </div>
    `;
  });
}

loadProducts(); 
