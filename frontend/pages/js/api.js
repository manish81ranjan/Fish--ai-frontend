const API_BASE = "http://127.0.0.1:5000/api";

// Get token
function getToken() {
  return localStorage.getItem("token");
}

// Set token
function setToken(token) {
  localStorage.setItem("token", token);
}

// Clear token
function logout() {
  localStorage.removeItem("token");
  window.location.href = "login.html";
}

// Generic API request
async function apiRequest(endpoint, method = "GET", data = null, auth = false) {
  const headers = { "Content-Type": "application/json" };

  if (auth && getToken()) {
    headers["Authorization"] = `Bearer ${getToken()}`;
  }

  const options = {
    method,
    headers
  };

  if (data) {
    options.body = JSON.stringify(data);
  }

  const response = await fetch(`${API_BASE}${endpoint}`, options);
  return response.json();
}
