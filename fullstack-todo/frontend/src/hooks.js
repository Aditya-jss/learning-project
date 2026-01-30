import { useCallback, useEffect, useMemo, useState } from "react";
import { createTodo, deleteTodo, fetchTodos, updateTodo } from "./api/client";

export function useTodos() {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadTodos = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchTodos();
      setTodos(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadTodos();
  }, [loadTodos]);

  const addTodo = useCallback(async (values) => {
    const created = await createTodo(values);
    setTodos((prev) => [created, ...prev]);
  }, []);

  const editTodo = useCallback(async (id, values) => {
    const updated = await updateTodo(id, values);
    setTodos((prev) => prev.map((todo) => (todo.id === id ? updated : todo)));
  }, []);

  const removeTodo = useCallback(async (id) => {
    await deleteTodo(id);
    setTodos((prev) => prev.filter((todo) => todo.id !== id));
  }, []);

  const sortedTodos = useMemo(
    () => [...todos].sort((a, b) => new Date(b.created_at) - new Date(a.created_at)),
    [todos]
  );

  return {
    todos: sortedTodos,
    loading,
    error,
    addTodo,
    editTodo,
    removeTodo,
    refresh: loadTodos,
  };
}
