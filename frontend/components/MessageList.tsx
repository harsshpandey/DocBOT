"use client";

import ReactMarkdown from "react-markdown";
import { useChatStore } from "../store/chatStore";
import { SourceDocuments } from "./SourceDocuments";

export function MessageList() {
  const messages = useChatStore((state) => state.messages);

  if (!messages.length) {
    return (
      <div className="flex h-full flex-col items-center justify-center text-center text-slate-500">
        <p className="text-lg font-semibold text-white">Welcome to DocBot</p>
        <p className="mt-2 max-w-md text-sm text-slate-400">
          Upload your policy documents and ask questions like &quot;What is the
          annual leave policy?&quot;
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {messages.map((message) => (
        <div
          key={message.id}
          className={`rounded-2xl border border-slate-800 p-4 ${
            message.role === "assistant"
              ? "bg-slate-900/60"
              : "bg-slate-900/20 text-right"
          }`}
        >
          <div className="text-xs uppercase tracking-wide text-slate-500">
            {message.role === "assistant" ? "DocBot" : "You"}
          </div>
          <div className="text-sm leading-relaxed text-slate-100">
            <ReactMarkdown>{message.content}</ReactMarkdown>
          </div>
          {message.role === "assistant" && (
            <SourceDocuments sources={message.sources} />
          )}
        </div>
      ))}
    </div>
  );
}

