import { useState } from "react";

export default function TodoForm({ onSubmit, submitting }) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!title.trim()) {
      setError("Title is required");
      return;
    }
    setError(null);
    await onSubmit({ title: title.trim(), description: description.trim() || null });
    setTitle("");
    setDescription("");
  };

  return (
    <form className="card" onSubmit={handleSubmit}>
      <div className="card-header">
        <div>
          <p className="eyebrow">Create</p>
          <h2 className="card-title">Add a todo</h2>
        </div>
        <button type="submit" className="btn" disabled={submitting}>
          {submitting ? "Saving..." : "Save"}
        </button>
      </div>
      <div className="field">
        <label htmlFor="title">Title</label>
        <input
          id="title"
          name="title"
          placeholder="What needs to get done?"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
      </div>
      <div className="field">
        <label htmlFor="description">Description</label>
        <textarea
          id="description"
          name="description"
          placeholder="Optional context or steps"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
      </div>
      {error && <p className="error">{error}</p>}
    </form>
  );
}
