"use client";

import { useState } from "react";
import { FileText, UploadCloud } from "lucide-react";
import { askQuestion, uploadDocuments } from "../lib/api";
import { useChatStore } from "../store/chatStore";
import { FileUploadArea } from "./FileUploadArea";
import { LoadingSpinner } from "./LoadingSpinner";
import { MessageList } from "./MessageList";
import { MessageInput } from "./MessageInput";

export function ChatInterface() {
  const {
    addUserMessage,
    addAssistantMessage,
    isLoading,
    setLoading,
    setError,
    error,
  } = useChatStore();
  const [uploadStatus, setUploadStatus] = useState<string>();

  const handleSend = async (message: string) => {
    addUserMessage(message);
    setLoading(true);
    setError(undefined);
    try {
      const response = await askQuestion(message);
      addAssistantMessage(response.answer, response.sources);
    } catch (err) {
      console.error(err);
      setError("Failed to get response. Please try again.");
      addAssistantMessage(
        "I encountered an error while processing your question."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async (files: FileList) => {
    setLoading(true);
    setUploadStatus(undefined);
    try {
      const response = await uploadDocuments(Array.from(files));
      setUploadStatus(
        `Indexed ${response.documents_indexed} documents (${response.chunks_created} chunks)`
      );
    } catch (err) {
      console.error(err);
      setUploadStatus("Upload failed. Please check file types and size limits.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen flex-col space-y-4 p-4 lg:p-8">
      <header className="rounded-3xl border border-slate-800 bg-slate-900/60 p-6">
        <div className="flex items-center space-x-3">
          <div className="rounded-2xl bg-emerald-500/10 p-3 text-emerald-400">
            <FileText className="h-6 w-6" />
          </div>
          <div>
            <h1 className="text-xl font-semibold text-white">DocBot</h1>
            <p className="text-sm text-slate-400">
              AI assistant for your policy manuals and procurement guides
            </p>
          </div>
        </div>
      </header>

      <section className="grid gap-4 lg:grid-cols-[320px_1fr]">
        <div className="space-y-4">
          <div className="rounded-3xl border border-slate-800 bg-slate-900/50 p-4">
            <div className="flex items-center space-x-2 text-sm font-semibold text-white">
              <UploadCloud className="h-4 w-4 text-emerald-400" />
              <span>Upload Documents</span>
            </div>
            <div className="mt-3">
              <FileUploadArea onFilesSelected={handleUpload} />
            </div>
            {uploadStatus && (
              <p className="mt-3 text-xs text-emerald-400">{uploadStatus}</p>
            )}
          </div>

          <div className="rounded-3xl border border-slate-800 bg-slate-900/50 p-4 text-xs text-slate-400">
            <p className="font-semibold uppercase tracking-wide">Examples</p>
            <ul className="mt-2 space-y-2">
              <li>&quot;What is the annual leave policy?&quot;</li>
              <li>&quot;How do I initiate an equipment procurement?&quot;</li>
              <li>&quot;What are the promotion criteria for Level 4?&quot;</li>
            </ul>
          </div>
        </div>

        <div className="flex flex-col space-y-4">
          <div className="flex-1 overflow-y-auto rounded-3xl border border-slate-800 bg-slate-950/70 p-4">
            <MessageList />
          </div>
          {error && (
            <div className="rounded-2xl border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-200">
              {error}
            </div>
          )}
          {isLoading && <LoadingSpinner />}
          <MessageInput onSend={handleSend} isLoading={isLoading} />
        </div>
      </section>
    </div>
  );
}

