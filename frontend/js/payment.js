async function loadPayment() {
  const amount = localStorage.getItem("order_amount");

  if (!amount) {
    alert("No order found");
    window.location.href = "cart.html";
    return;
  }

  document.getElementById("amount").innerText =
    `Total Amount: ₹${amount}`;
}

// Frontend Razorpay Checkout
async function payNow() {
  const token = localStorage.getItem("token");
  const orderId = localStorage.getItem("order_id");

  const res = await fetch(`${API_URL}/razorpay/order`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify({ order_id: orderId })
  });

  const data = await res.json();

  const options = {
    key: data.key,
    amount: data.amount,
    currency: data.currency,
    order_id: data.razorpay_order_id,

    // ✅ FIXED HANDLER
    handler: function (response) {
      verifyPayment(response);   // ✅ THIS WAS MISSING
    }
  };

  const rzp = new Razorpay(options);
  rzp.open();
}

async function verifyPayment(response) {
  const token = localStorage.getItem("token");

  await fetch(`${API_URL}/razorpay/verify`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify(response)
  });

  window.location.href = "success.html";
}
