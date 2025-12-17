const productContainer = document.getElementById("productContainer");
const searchInput = document.getElementById("searchInput");
const sortSelect = document.getElementById("sortSelect");

let allProducts = [];

// Fetch products from API
async function fetchProducts() {
  try {
    const response = await fetch("https://dummyjson.com/products");
    const data = await response.json();
    allProducts = data.products;
    displayProducts(allProducts);
  } catch (error) {
    console.error("Failed to load products", error);
  }
}

// Display products
function displayProducts(products) {
  productContainer.innerHTML = "";

  products.forEach(product => {
    const card = document.createElement("div");
    card.className = "card";

    card.innerHTML = `
      <img src="${product.thumbnail}" alt="${product.title}">
      <h3>${product.title}</h3>
      <p>₹ ${product.price}</p>
    `;

    productContainer.appendChild(card);
  });
}

// Search
searchInput.addEventListener("input", () => {
  const value = searchInput.value.toLowerCase();
  const filtered = allProducts.filter(p =>
    p.title.toLowerCase().includes(value)
  );
  displayProducts(filtered);
});

// Sort
sortSelect.addEventListener("change", () => {
  let sorted = [...allProducts];

  if (sortSelect.value === "low") {
    sorted.sort((a, b) => a.price - b.price);
  } else if (sortSelect.value === "high") {
    sorted.sort((a, b) => b.price - a.price);
  }

  displayProducts(sorted);
});

// Load products
if (productContainer) {
  fetchProducts();
}
