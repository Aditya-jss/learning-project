import TodoItem from "./TodoItem.jsx";

export default function TodoList({ todos, onSave, onDelete }) {
  if (!todos.length) {
    return <p className="muted">No todos yet. Create your first one above.</p>;
  }

  return (
    <ul className="todo-list">
      {todos.map((todo) => (
        <TodoItem key={todo.id} todo={todo} onSave={onSave} onDelete={onDelete} />
      ))}
    </ul>
  );
}
