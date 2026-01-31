async function loadOrders() {
  const orders = await apiRequest("/orders/", "GET", null, true);
  const container = document.getElementById("ordersList");

  container.innerHTML = "";

  if (!orders.length) {
    container.innerHTML = "<p>No orders found</p>";
    return;
  }

  orders.forEach(order => {
    const div = document.createElement("div");
    div.className = "bg-white p-4 mb-3 shadow";

    div.innerHTML = `
      <p><strong>Order ID:</strong> ${order.id}</p>
      <p><strong>Total:</strong> ₹${order.total_amount}</p>
      <p><strong>Status:</strong> ${order.status}</p>
      <p><strong>Date:</strong> ${order.created_at}</p>
    `;

    container.appendChild(div);
  });
}

loadOrders();
