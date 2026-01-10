import { apiFetch } from "./api";

export interface Task {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  is_completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface TaskListResponse {
  tasks: Task[];
  total: number;
}

export const taskService = {
  async getTasks(is_completed?: boolean) {
    const query = is_completed !== undefined ? `?is_completed=${is_completed}` : "";
    const response = await apiFetch(`/api/tasks${query}`);
    if (!response.ok) throw new Error("Failed to fetch tasks");
    return response.json();
  },

  async createTask(title: string, description?: string) {
    const response = await apiFetch("/api/tasks", {
      method: "POST",
      body: JSON.stringify({ title, description }),
    });
    if (!response.ok) throw new Error("Failed to create task");
    return response.json();
  },

  async updateTask(id: string, title?: string, description?: string) {
    const response = await apiFetch(`/api/tasks/${id}`, {
      method: "PUT",
      body: JSON.stringify({ title, description }),
    });
    if (!response.ok) throw new Error("Failed to update task");
    return response.json();
  },

  async deleteTask(id: string) {
    const response = await apiFetch(`/api/tasks/${id}`, {
      method: "DELETE",
    });
    if (!response.ok) throw new Error("Failed to delete task");
  },

  async toggleCompletion(id: string) {
    const response = await apiFetch(`/api/tasks/${id}/complete`, {
      method: "PATCH",
    });
    if (!response.ok) throw new Error("Failed to toggle completion");
    return response.json();
  },
};
