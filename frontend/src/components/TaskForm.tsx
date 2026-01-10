"use client";

import { useState } from "react";
import { Plus, Sparkles } from "lucide-react";

interface TaskFormProps {
  onSubmit: (title: string, description?: string) => void;
  loading: boolean;
}

export default function TaskForm({ onSubmit, loading }: TaskFormProps) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;
    onSubmit(title, description);
    setTitle("");
    setDescription("");
  };

  return (
    <form onSubmit={handleSubmit} className="glass p-8 rounded-3xl shadow-xl hover:shadow-2xl transition-all duration-500 border border-white/50 relative overflow-hidden group">
      {/* Animated gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-br from-violet-50/50 via-blue-50/50 to-cyan-50/50 opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"></div>

      <div className="space-y-5 relative z-10">
        <div className="flex items-center space-x-3 mb-6">
          <div className="p-2 bg-gradient-to-r from-violet-500 to-cyan-500 rounded-xl">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <h3 className="text-xl font-black text-gradient">New Task</h3>
        </div>

        <div className="flex flex-col space-y-2">
          <label className="text-sm font-bold text-gray-700 ml-1">Task Title</label>
          <input
            type="text"
            placeholder="What will you accomplish?"
            className="w-full px-4 py-3.5 bg-white/70 backdrop-blur-sm border-2 border-gray-200 rounded-xl focus:bg-white focus:border-violet-400 focus:ring-4 focus:ring-violet-100 outline-none transition-all duration-300 font-medium placeholder:text-gray-400"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </div>

        <div className="flex flex-col space-y-2">
          <label className="text-sm font-bold text-gray-700 ml-1">Description (Optional)</label>
          <textarea
            placeholder="Add details, notes or context..."
            className="w-full px-4 py-3.5 bg-white/70 backdrop-blur-sm border-2 border-gray-200 rounded-xl focus:bg-white focus:border-violet-400 focus:ring-4 focus:ring-violet-100 outline-none transition-all duration-300 resize-none font-medium placeholder:text-gray-400"
            rows={3}
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </div>

        <button
          type="submit"
          disabled={loading || !title.trim()}
          className="w-full bg-gradient-to-r from-violet-600 via-blue-600 to-cyan-600 hover:from-violet-700 hover:via-blue-700 hover:to-cyan-700 text-white py-4 rounded-xl font-bold text-sm shadow-lg shadow-violet-200 hover:shadow-xl hover:shadow-violet-300 transition-all duration-300 disabled:opacity-50 disabled:shadow-none flex items-center justify-center space-x-2 active:scale-95 hover:scale-[1.02] relative overflow-hidden group/button"
        >
          <div className="absolute inset-0 bg-gradient-to-r from-cyan-600 via-blue-600 to-violet-600 opacity-0 group-hover/button:opacity-100 transition-opacity duration-500"></div>
          {loading ? (
            <>
              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin relative z-10" />
              <span className="relative z-10">Creating...</span>
            </>
          ) : (
            <>
              <Plus className="w-5 h-5 relative z-10" />
              <span className="relative z-10">Create Task</span>
            </>
          )}
        </button>
      </div>
    </form>
  );
}
