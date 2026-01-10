"use client";

import { useEffect, useState } from "react";
import TaskForm from "@/components/TaskForm";
import TaskList from "@/components/TaskList";
import { taskService, Task } from "@/services/tasks";

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchTasks = async () => {
    try {
      const data = await taskService.getTasks();
      setTasks(data.tasks);
    } catch (err) {
      setError("Could not load tasks. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const handleCreateTask = async (title: string, description?: string) => {
    setActionLoading(true);
    try {
      const newTask = await taskService.createTask(title, description);
      setTasks((prev) => [newTask, ...prev]);
    } catch (err) {
      setError("Failed to create task.");
    } finally {
      setActionLoading(false);
    }
  };

  const handleToggleTask = async (id: string) => {
    try {
      const updatedTask = await taskService.toggleCompletion(id);
      setTasks((prev) =>
        prev.map((t) => (t.id === id ? updatedTask : t))
      );
    } catch (err) {
      setError("Failed to update task.");
    }
  };

  const handleDeleteTask = async (id: string) => {
    if (!confirm("Are you sure you want to delete this task?")) return;
    try {
      await taskService.deleteTask(id);
      setTasks((prev) => prev.filter((t) => t.id !== id));
    } catch (err) {
      setError("Failed to delete task.");
    }
  };

  return (
    <div className="min-h-screen p-6 md:p-10 max-w-7xl mx-auto">
      <div className="space-y-10 animate-scale-in">
        {/* Header with gradient */}
        <header className="relative overflow-hidden glass p-8 md:p-10 rounded-3xl shadow-2xl border border-white/50">
          <div className="absolute top-0 right-0 w-96 h-96 bg-gradient-to-br from-violet-200 to-cyan-200 rounded-full blur-3xl opacity-30 -z-10"></div>

          <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 relative z-10">
            <div className="space-y-3">
              <div className="inline-block">
                <h1 className="text-5xl md:text-6xl font-black text-gradient mb-2">My Tasks</h1>
                <div className="h-2 w-32 bg-gradient-to-r from-violet-600 via-blue-600 to-cyan-600 rounded-full"></div>
              </div>
              <p className="text-xl text-gray-600 font-medium">Capture your ideas and get things done.</p>
            </div>

            <div className="flex flex-wrap gap-3">
              <div className="glass px-5 py-3 rounded-2xl border border-white/50 shadow-lg">
                <div className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-1">Total</div>
                <div className="text-2xl font-black text-gradient">{tasks.length}</div>
              </div>
              <div className="glass px-5 py-3 rounded-2xl border border-white/50 shadow-lg">
                <div className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-1">Completed</div>
                <div className="text-2xl font-black text-emerald-600">{tasks.filter(t => t.is_completed).length}</div>
              </div>
              <div className="glass px-5 py-3 rounded-2xl border border-white/50 shadow-lg">
                <div className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-1">Active</div>
                <div className="text-2xl font-black text-violet-600">{tasks.filter(t => !t.is_completed).length}</div>
              </div>
            </div>
          </div>
        </header>

        {error && (
          <div className="p-5 text-sm font-medium text-red-600 glass border border-red-200 rounded-2xl flex justify-between items-center shadow-lg animate-slide-down">
            <div className="flex items-center space-x-3">
              <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse" />
              <span>{error}</span>
            </div>
            <button onClick={() => setError("")} className="hover:bg-red-100 p-2 rounded-xl transition-all duration-200 active:scale-90">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" /></svg>
            </button>
          </div>
        )}

        <div className="grid gap-8 lg:grid-cols-[420px_1fr]">
          {/* Sidebar */}
          <aside className="space-y-6">
            <TaskForm onSubmit={handleCreateTask} loading={actionLoading} />

            {/* Pro Tips Card */}
            <div className="relative overflow-hidden glass p-8 rounded-3xl border border-white/50 shadow-xl group hover:shadow-2xl transition-all duration-500">
              <div className="absolute inset-0 bg-gradient-to-br from-violet-500/10 via-blue-500/10 to-cyan-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>

              <div className="relative z-10 space-y-4">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-gradient-to-br from-violet-500 to-cyan-500 rounded-xl shadow-lg">
                    <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                    </svg>
                  </div>
                  <h3 className="font-black text-xl text-gradient">Pro Tips</h3>
                </div>

                <ul className="space-y-3">
                  <li className="flex items-start space-x-2">
                    <span className="text-violet-500 font-bold mt-1">•</span>
                    <span className="text-gray-700 text-sm leading-relaxed">Break large goals into smaller, actionable tasks</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-blue-500 font-bold mt-1">•</span>
                    <span className="text-gray-700 text-sm leading-relaxed">Set realistic deadlines and celebrate small wins</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-cyan-500 font-bold mt-1">•</span>
                    <span className="text-gray-700 text-sm leading-relaxed">Review your tasks regularly to stay on track</span>
                  </li>
                </ul>
              </div>
            </div>
          </aside>

          {/* Main Content */}
          <section className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-black text-gray-800 flex items-center space-x-3">
                <div className="w-1 h-8 bg-gradient-to-b from-violet-500 to-cyan-500 rounded-full"></div>
                <span>Your Tasks</span>
              </h2>
              <div className="text-xs font-bold uppercase tracking-wider text-gray-500 bg-white/50 backdrop-blur-sm px-4 py-2 rounded-full border border-gray-200">
                Sorted by Recent
              </div>
            </div>

            <div className="min-h-[500px]">
              <TaskList
                tasks={tasks}
                loading={loading}
                onToggle={handleToggleTask}
                onDelete={handleDeleteTask}
              />
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}
