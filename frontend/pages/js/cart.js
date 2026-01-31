async function loadCart() {
  const items = await apiRequest("/cart/", "GET", null, true);
  const container = document.getElementById("cartItems");

  container.innerHTML = "";
  let total = 0;

  items.forEach(item => {
    total += item.subtotal;

    const div = document.createElement("div");
    div.className = "bg-white p-4 mb-3 shadow";

    div.innerHTML = `
      <h2>${item.name}</h2>
      <p>Price: ₹${item.price}</p>
      <p>Qty: ${item.quantity}</p>
      <p class="font-bold">Subtotal: ₹${item.subtotal}</p>
      <button
        onclick="removeItem(${item.cart_id})"
        class="text-red-600">
        Remove
      </button>
    `;

    container.appendChild(div);
  });

  const totalDiv = document.createElement("div");
  totalDiv.className = "font-bold mt-4";
  totalDiv.innerText = `Total: ₹${total}`;
  container.appendChild(totalDiv);
}

async function removeItem(cartId) {
  await apiRequest(`/cart/${cartId}`, "DELETE", null, true);
  loadCart();
}

async function checkout() {
  const response = await apiRequest("/orders/", "POST", null, true);

  if (response.order_id) {
    localStorage.setItem("order_id", response.order_id);
    window.location.href = "checkout.html";
  } else {
    alert(response.message || "Checkout failed");
  }
}

loadCart();


function buyNow(id){
 const fish = fishes.find(f=>f.id===id);
 localStorage.setItem("buyNow",JSON.stringify({...fish,qty:1}));
 window.location.href="/checkout";
}
