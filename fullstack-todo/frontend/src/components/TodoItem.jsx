import { useState } from "react";

export default function TodoItem({ todo, onSave, onDelete }) {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(todo.title);
  const [description, setDescription] = useState(todo.description || "");
  const [saving, setSaving] = useState(false);

  const handleToggleComplete = async () => {
    setSaving(true);
    await onSave(todo.id, { completed: !todo.completed });
    setSaving(false);
  };

  const handleEdit = async (event) => {
    event.preventDefault();
    setSaving(true);
    await onSave(todo.id, { title: title.trim(), description: description.trim() || null });
    setSaving(false);
    setIsEditing(false);
  };

  const handleDelete = async () => {
    setSaving(true);
    await onDelete(todo.id);
    setSaving(false);
  };

  return (
    <li className="todo-item">
      <div className="todo-main">
        <button className="chip" onClick={handleToggleComplete} disabled={saving}>
          {todo.completed ? "✓ Done" : "○ Open"}
        </button>
        {isEditing ? (
          <form className="edit-form" onSubmit={handleEdit}>
            <input value={title} onChange={(e) => setTitle(e.target.value)} required />
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Details"
            />
            <div className="actions">
              <button type="submit" className="btn ghost" disabled={saving}>
                Save
              </button>
              <button type="button" className="btn ghost" onClick={() => setIsEditing(false)}>
                Cancel
              </button>
            </div>
          </form>
        ) : (
          <div className="todo-copy">
            <div className="todo-title">{todo.title}</div>
            {todo.description && <p className="todo-desc">{todo.description}</p>}
            <p className="meta">Created {new Date(todo.created_at).toLocaleString()}</p>
          </div>
        )}
      </div>
      <div className="actions">
        {!isEditing && (
          <button className="btn ghost" onClick={() => setIsEditing(true)} disabled={saving}>
            Edit
          </button>
        )}
        <button className="btn ghost danger" onClick={handleDelete} disabled={saving}>
          Delete
        </button>
      </div>
    </li>
  );
}
