const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

async function handleResponse(response) {
  if (!response.ok) {
    const detail = await response.json().catch(() => ({}));
    const message = detail?.detail || `Request failed with status ${response.status}`;
    throw new Error(message);
  }
  if (response.status === 204) return null;
  return response.json();
}

export async function fetchTodos() {
  const res = await fetch(`${API_BASE_URL}/api/todos/`);
  return handleResponse(res);
}

export async function createTodo(payload) {
  const res = await fetch(`${API_BASE_URL}/api/todos/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return handleResponse(res);
}

export async function updateTodo(id, payload) {
  const res = await fetch(`${API_BASE_URL}/api/todos/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return handleResponse(res);
}

export async function deleteTodo(id) {
  const res = await fetch(`${API_BASE_URL}/api/todos/${id}`, {
    method: "DELETE",
  });
  return handleResponse(res);
}
