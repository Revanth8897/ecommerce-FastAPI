const API_URL = "http://127.0.0.1:8000"; // change only if backend URL is different

async function createProduct() {
  const token = localStorage.getItem("token");

  if (!token) {
    alert("Login required");
    return;
  }

  const product = {
    name: document.getElementById("name").value,
    description: document.getElementById("description").value,
    price: Number(document.getElementById("price").value),
    stock: Number(document.getElementById("stock").value)
  };

  const res = await fetch(`${API_URL}/products/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify(product)
  });

  const data = await res.json();

  if (!res.ok) {
    alert(data.detail || "Failed to add product");
    return;
  }

  alert("Product added successfully");
  loadProducts();
}

async function loadProducts() {
  const res = await fetch(`${API_URL}/products/`);
  const products = await res.json();

  const table = document.getElementById("productTable");
  table.innerHTML = "";

  products.forEach(p => {
  table.innerHTML += `
    <tr>
      <td>${p.id}</td>
      <td>
        <input id="name-${p.id}" value="${p.name}">
      </td>
      <td>
        <input id="price-${p.id}" type="number" value="${p.price}">
      </td>
      <td>
        <input id="stock-${p.id}" type="number" value="${p.stock}">
      </td>
      <td>
        <button onclick="updateProduct(${p.id})">Update</button>
        <button onclick="deleteProduct(${p.id})">Delete</button>
      </td>
    </tr>
  `;
});
}

async function deleteProduct(id) {
  const token = localStorage.getItem("token");

  if (!confirm("Are you sure?")) return;

  const res = await fetch(`${API_URL}/products/${id}`, {
    method: "DELETE",
    headers: {
      "Authorization": `Bearer ${token}`
    }
  });

  if (!res.ok) {
    alert("Delete failed");
    return;
  }

  alert("Product deleted");
  loadProducts();
}

async function updateProduct(id) {
  const token = localStorage.getItem("token");

  const product = {
    name: document.getElementById(`name-${id}`).value,
    price: Number(document.getElementById(`price-${id}`).value),
    stock: Number(document.getElementById(`stock-${id}`).value)
  };

  const res = await fetch(`${API_URL}/products/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify(product)
  });

  if (!res.ok) {
    alert("Update failed");
    return;
  }

  alert("Product updated successfully");
  loadProducts(); // refresh table
}


loadProducts();
