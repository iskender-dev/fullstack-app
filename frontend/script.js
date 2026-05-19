const API_URL = window.location.hostname === "localhost"
    ? "http://localhost:5000"
    : "https://fullstack-app-production-e551.up.railway.app/";


async function loadTasks() {
    const response = await fetch(`${API_URL}/api/data`);
    const tasks = await response.json();

    const list = document.getElementById("taskList");
    list.innerHTML = "";

    tasks.forEach(task => {
        const li = document.createElement("li");

        li.innerHTML = `
            ${task.text}
            <button onclick="deleteTask(${task.id})">
                Delete
            </button>
        `;

        list.appendChild(li);
    });
}


async function addTask() {
    const input = document.getElementById("taskInput");

    const text = input.value;

    if (!text) return;

    await fetch(`${API_URL}/api/data`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            text
        })
    });

    input.value = "";

    loadTasks();
}


async function deleteTask(id) {
    await fetch(`${API_URL}/api/data/${id}`, {
        method: "DELETE"
    });

    loadTasks();
}

loadTasks();