"use client";

import TaskItem from "./TaskItem";
import { Task } from "@/services/tasks";
import { Inbox, Loader2 } from "lucide-react";

interface TaskListProps {
  tasks: Task[];
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
  loading: boolean;
}

export default function TaskList({ tasks, onToggle, onDelete, loading }: TaskListProps) {
  if (loading && tasks.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-16 space-y-4">
        <Loader2 className="w-12 h-12 text-violet-500 animate-spin" />
        <p className="text-gray-500 font-medium">Loading your tasks...</p>
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-20 glass rounded-3xl border-2 border-dashed border-gray-300 space-y-4 animate-scale-in">
        <div className="p-4 bg-gradient-to-br from-violet-100 to-cyan-100 rounded-2xl">
          <Inbox className="w-12 h-12 text-violet-600" />
        </div>
        <div className="text-center space-y-1">
          <h3 className="text-xl font-bold text-gray-800">No tasks yet</h3>
          <p className="text-gray-500 max-w-sm">Your task list is empty. Create your first task to get started on your productivity journey!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {tasks.map((task, index) => (
        <div
          key={task.id}
          style={{
            animationDelay: `${index * 50}ms`,
          }}
          className="animate-slide-up"
        >
          <TaskItem
            task={task}
            onToggle={onToggle}
            onDelete={onDelete}
          />
        </div>
      ))}
    </div>
  );
}
