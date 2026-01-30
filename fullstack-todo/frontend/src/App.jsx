import { useMemo } from "react";
import TodoForm from "./components/TodoForm.jsx";
import TodoList from "./components/TodoList.jsx";
import { useTodos } from "./hooks.js";

export default function App() {
  const { todos, loading, error, addTodo, editTodo, removeTodo } = useTodos();

  const stats = useMemo(() => {
    const total = todos.length;
    const done = todos.filter((t) => t.completed).length;
    return { total, done, open: total - done };
  }, [todos]);

  const handleSave = async (id, values) => editTodo(id, values);

  const handleDelete = async (id) => removeTodo(id);

  return (
    <div className="page">
      <header className="hero">
        <p className="eyebrow">Python + React Starter</p>
        <h1>Todos with FastAPI</h1>
        <p className="muted">Full-stack CRUD with a minimal, opinionated setup.</p>
        <div className="pill-group">
          <span className="pill">Total: {stats.total}</span>
          <span className="pill">Open: {stats.open}</span>
          <span className="pill">Done: {stats.done}</span>
        </div>
      </header>

      <main className="grid">
        <section>
          <TodoForm onSubmit={addTodo} submitting={false} />
        </section>
        <section className="panel">
          <div className="panel-header">
            <div>
              <p className="eyebrow">Todos</p>
              <h2>Your list</h2>
            </div>
            {loading && <span className="badge">Loading…</span>}
          </div>
          {error && <div className="error">{error}</div>}
          {!loading && <TodoList todos={todos} onSave={handleSave} onDelete={handleDelete} />}
        </section>
      </main>
    </div>
  );
}
