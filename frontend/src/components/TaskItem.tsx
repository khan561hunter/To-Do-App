"use client";

import { CheckCircle2, Circle, Trash2, Clock } from "lucide-react";
import { Task } from "@/services/tasks";

interface TaskItemProps {
  task: Task;
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
}

export default function TaskItem({ task, onToggle, onDelete }: TaskItemProps) {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInMs = now.getTime() - date.getTime();
    const diffInMins = Math.floor(diffInMs / (1000 * 60));
    const diffInHours = Math.floor(diffInMs / (1000 * 60 * 60));
    const diffInDays = Math.floor(diffInMs / (1000 * 60 * 60 * 24));

    if (diffInMins < 60) return `${diffInMins}m ago`;
    if (diffInHours < 24) return `${diffInHours}h ago`;
    if (diffInDays < 7) return `${diffInDays}d ago`;
    return date.toLocaleDateString();
  };

  return (
    <div className={`glass p-5 rounded-2xl shadow-md hover:shadow-xl transition-all duration-300 group animate-slide-up border ${task.is_completed ? 'border-emerald-200 bg-emerald-50/30' : 'border-white/50'} hover:scale-[1.02] relative overflow-hidden`}>
      {/* Completion indicator stripe */}
      {task.is_completed && (
        <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-emerald-400 to-green-500"></div>
      )}

      <div className="flex items-start justify-between space-x-4">
        <div className="flex items-start space-x-4 flex-1 min-w-0">
          <button
            onClick={() => onToggle(task.id)}
            className="relative flex items-center justify-center transition-all duration-300 active:scale-90 hover:scale-110 mt-1 flex-shrink-0"
          >
            {task.is_completed ? (
              <div className="relative">
                <div className="absolute inset-0 bg-emerald-400 rounded-full animate-ping opacity-20"></div>
                <div className="relative bg-gradient-to-br from-emerald-400 to-green-500 p-1 rounded-full shadow-lg">
                  <CheckCircle2 className="w-6 h-6 text-white" />
                </div>
              </div>
            ) : (
              <div className="relative group/checkbox">
                <div className="absolute inset-0 bg-violet-100 rounded-full scale-0 group-hover/checkbox:scale-100 transition-transform duration-300"></div>
                <div className="relative text-gray-300 group-hover/checkbox:text-violet-500 transition-colors duration-300">
                  <Circle className="w-6 h-6" strokeWidth={2.5} />
                </div>
              </div>
            )}
          </button>

          <div className="flex-1 min-w-0">
            <h3 className={`font-bold text-base transition-all duration-300 ${task.is_completed ? "line-through text-gray-400" : "text-gray-800"} break-words`}>
              {task.title}
            </h3>
            {task.description && (
              <p className={`text-sm mt-1.5 transition-all duration-300 ${task.is_completed ? "text-gray-400" : "text-gray-600"} line-clamp-2 break-words`}>
                {task.description}
              </p>
            )}
            <div className="flex items-center space-x-2 mt-2">
              <Clock className={`w-3.5 h-3.5 ${task.is_completed ? 'text-gray-400' : 'text-violet-500'}`} />
              <span className={`text-xs font-medium ${task.is_completed ? 'text-gray-400' : 'text-gray-500'}`}>
                {formatDate(task.created_at)}
              </span>
            </div>
          </div>
        </div>

        <button
          onClick={() => onDelete(task.id)}
          className="opacity-0 group-hover:opacity-100 text-gray-400 hover:text-red-500 hover:bg-red-50 p-2.5 rounded-xl transition-all duration-300 active:scale-90 hover:scale-110 flex-shrink-0"
          title="Delete task"
        >
          <Trash2 className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
}
