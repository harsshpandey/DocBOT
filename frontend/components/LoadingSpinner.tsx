"use client";

export function LoadingSpinner() {
  return (
    <div className="flex items-center space-x-2 text-sm text-slate-300">
      <div className="h-3 w-3 animate-ping rounded-full bg-emerald-400" />
      <span>Thinking...</span>
    </div>
  );
}

