
const input = document.getElementById("todoInput");
const addBtn = document.getElementById("addBtn");
const list = document.getElementById("todoList");

// Load todos from localStorage
let todos = JSON.parse(localStorage.getItem("todos")) || [];

// Save to localStorage
const saveTodos = () => {
  localStorage.setItem("todos", JSON.stringify(todos));
};

// Render todos
const renderTodos = () => {
  list.innerHTML = "";

  todos.forEach((todo, index) => {
    const li = document.createElement("li");

    const textSpan = document.createElement("span");
    textSpan.textContent = todo;

    const actions = document.createElement("div");
    actions.className = "actions";

    // ✏️ Edit button
    const editBtn = document.createElement("button");
    editBtn.textContent = "edit";
    editBtn.onclick = () => {
      const newText = prompt("Edit task:", todo);
      if (newText) {
        todos[index] = newText;
        saveTodos();
        renderTodos();
      }
    };

    // ❌ Delete button
    const delBtn = document.createElement("button");
    delBtn.textContent = "delete";
    delBtn.onclick = () => {
      todos.splice(index, 1);
      saveTodos();
      renderTodos();
    };

    actions.append(editBtn, delBtn);
    li.append(textSpan, actions);
    list.appendChild(li);
  });
};

// Add todo
addBtn.addEventListener("click", () => {
  const text = input.value.trim();
  if (!text) return;

  todos.push(text);
  input.value = "";
  saveTodos();
  renderTodos();
});

// Enter key support
input.addEventListener("keypress", (e) => {
  if (e.key === "Enter") addBtn.click();
});

renderTodos();
