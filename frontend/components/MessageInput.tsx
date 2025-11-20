"use client";

import { useState } from "react";
import { ArrowUpCircle } from "lucide-react";

type Props = {
  onSend: (message: string) => Promise<void> | void;
  isLoading?: boolean;
};

export function MessageInput({ onSend, isLoading }: Props) {
  const [value, setValue] = useState("");

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!value.trim()) return;
    await onSend(value.trim());
    setValue("");
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="relative rounded-2xl border border-slate-700 bg-slate-900/60 p-3"
    >
      <textarea
        rows={2}
        value={value}
        onChange={(event) => setValue(event.target.value)}
        placeholder="Ask DocBot anything about your policies..."
        className="w-full resize-none bg-transparent text-sm text-white outline-none"
        disabled={isLoading}
      />
      <button
        type="submit"
        disabled={isLoading || !value.trim()}
        className="absolute bottom-4 right-4 text-emerald-400 transition hover:text-emerald-300 disabled:text-slate-600"
        aria-label="Send message"
      >
        <ArrowUpCircle className="h-6 w-6" />
      </button>
    </form>
  );
}

