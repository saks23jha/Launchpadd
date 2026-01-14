async function loadUsers() {
  const res = await fetch("/api/users");
  const users = await res.json();

  const ul = document.getElementById("users");
  ul.innerHTML = "";

  users.forEach(user => {
    const li = document.createElement("li");
    li.textContent = `${user.name} — ${
      user.available ? "Available " : "Unavailable "
    }`;
    li.className = user.available ? "available" : "unavailable";
    ul.appendChild(li);
  });
}
