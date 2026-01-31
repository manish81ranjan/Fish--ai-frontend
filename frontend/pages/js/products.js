// async function loadProducts() {
//   const products = await apiRequest("/products");

//   const container = document.getElementById("productList");
//   container.innerHTML = "";

//   products.forEach(p => {
//     const card = document.createElement("div");
//     card.className = "bg-white p-4 rounded shadow";

//     card.innerHTML = `
//       <h2 class="font-bold text-lg">${p.name}</h2>
//       <p class="text-sm">${p.description || ""}</p>
//       <p class="mt-2 font-semibold">₹${p.price}</p>
//       <button
//         onclick="addToCart(${p.id})"
//         class="mt-3 bg-green-600 text-white px-3 py-1 rounded">
//         Add to Cart
//       </button>
//     `;

//     container.appendChild(card);
//   });
// }

// async function addToCart(productId) {
//   const response = await apiRequest(
//     "/cart/",
//     "POST",
//     { product_id: productId, quantity: 1 },
//     true
//   );

//   alert(response.message || "Added to cart");
// }

// loadProducts();

const products = [
  {
    name: "Clownfish",
    price: 25,
    img: "https://images.unsplash.com/photo-1553524788-5d53aaf70d65?auto=format&fit=crop&w=400&q=80",
    rating: 4.8
  },
  {
    name: "Betta Fish",
    price: 15,
    img: "https://images.unsplash.com/photo-1600280559421-1b18f799d6fc?auto=format&fit=crop&w=400&q=80",
    rating: 4.6
  },
  {
    name: "Goldfish",
    price: 10,
    img: "https://images.unsplash.com/photo-1587659826277-71d3cf2aa8e8?auto=format&fit=crop&w=400&q=80",
    rating: 4.4
  },
  {
    name: "Angelfish",
    price: 20,
    img: "https://images.unsplash.com/photo-1567443025981-2f6dca4d83a3?auto=format&fit=crop&w=400&q=80",
    rating: 4.7
  }
];

const productList = document.getElementById("productList");

products.forEach(product => {
  const card = document.createElement("div");
  card.className = "bg-white rounded-lg shadow hover:shadow-lg transition p-4 flex flex-col";
  
  card.innerHTML = `
    <img src="${product.img}" alt="${product.name}" class="w-full h-48 object-cover rounded mb-4">
    <h3 class="text-lg font-semibold mb-2">${product.name}</h3>
    <p class="text-blue-600 font-bold mb-2">$${product.price}</p>
    <p class="text-yellow-500 mb-2">${"⭐".repeat(Math.floor(product.rating))}</p>
    <button class="mt-auto bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition">Add to Cart</button>
  `;
  
  productList.appendChild(card);
});
