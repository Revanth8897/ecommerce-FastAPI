const API_URL = "http://127.0.0.1:8000";

async function loadCart() {
  const token = localStorage.getItem("token");

  if (!token) {
    window.location.href = "login.html";
    return;
  }

  const res = await fetch(`${API_URL}/cart`, {
    headers: {
      "Authorization": `Bearer ${token}`
    }
  });

  const cartItems = await res.json();

  const container = document.getElementById("cart-items");
  const totalEl = document.getElementById("total-price");

  container.innerHTML = "";
  let total = 0;

  if (cartItems.length === 0) {
    container.innerHTML = "<h3>Your cart is empty</h3>";
    totalEl.innerText = "₹0";
    return;
  }

  cartItems.forEach(item => {
    total += item.product.price * item.quantity;

    container.innerHTML += `
      <div class="product-card">
        <h3>${item.product.name}</h3>
        <p>₹${item.product.price}</p>

        <div>
          <button onclick="updateQty(${item.id}, ${item.quantity - 1})">-</button>
          <span>${item.quantity}</span>
          <button onclick="updateQty(${item.id}, ${item.quantity + 1})">+</button>
        </div>

        <button onclick="removeItem(${item.id})">Remove</button>
      </div>
    `;
  });

  totalEl.innerText = `₹${total}`;
}

async function updateQty(cartId, qty) {
  if (qty < 1) return;

  const token = localStorage.getItem("token");

  await fetch(`${API_URL}/cart/${cartId}?quantity=${qty}`, {
    method: "PUT",
    headers: {
      "Authorization": `Bearer ${token}`
    }
  });

  loadCart();
}

async function removeItem(cartId) {
  const token = localStorage.getItem("token");

  await fetch(`${API_URL}/cart/${cartId}`, {
    method: "DELETE",
    headers: {
      "Authorization": `Bearer ${token}`
    }
  });

  loadCart();
}

async function placeOrder() {
  const token = localStorage.getItem("token");

  const res = await fetch(`${API_URL}/orders`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`
    }
  });

  const data = await res.json();

  if (!res.ok) {
    alert(data.detail || "Order failed");
    return;
  }

  window.location.href = "payment.html";
}

loadCart();

async function placeOrder() {
  const token = localStorage.getItem("token");

  if (!token) {
    alert("Please login again");
    window.location.href = "login.html";
    return;
  }

  try {
    const res = await fetch(`${API_URL}/orders`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    const data = await res.json();

    if (!res.ok) {
      alert(data.detail || "Order failed");
      return;
    }

    // ✅ SAVE ORDER ID FOR PAYMENT
    localStorage.setItem("order_id", data.id);
    localStorage.setItem("order_amount", data.total_amount);

    // ✅ GO TO PAYMENT PAGE
    window.location.href = "payment.html";

  } catch (err) {
    console.error(err);
    alert("Server error");
  }
}
