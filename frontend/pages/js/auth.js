async function login() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const response = await apiRequest("/auth/login", "POST", {
    email,
    password
  });

  if (response.token) {
    setToken(response.token);
    window.location.href = "marketplace.html";
  } else {
    alert(response.message || "Login failed");
  }
}

async function signup() {
  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const response = await apiRequest("/auth/signup", "POST", {
    name,
    email,
    password
  });

  if (response.message) {
    alert("Signup successful! Login now.");
    window.location.href = "login.html";
  } else {
    alert("Signup failed");
  }
}
