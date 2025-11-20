import { create } from "zustand";
import type { ChatMessage, SourceDocument } from "../lib/types";
import { shortId } from "../lib/utils";

type ChatState = {
  messages: ChatMessage[];
  isLoading: boolean;
  error?: string;
  addUserMessage: (content: string) => void;
  addAssistantMessage: (content: string, sources?: SourceDocument[]) => void;
  setLoading: (value: boolean) => void;
  setError: (message?: string) => void;
  clear: () => void;
};

export const useChatStore = create<ChatState>((set) => ({
  messages: [],
  isLoading: false,
  addUserMessage: (content: string) =>
    set((state) => ({
      messages: [
        ...state.messages,
        {
          id: shortId(),
          role: "user",
          content,
          createdAt: new Date().toISOString(),
        },
      ],
    })),
  addAssistantMessage: (content: string, sources?: SourceDocument[]) =>
    set((state) => ({
      messages: [
        ...state.messages,
        {
          id: shortId(),
          role: "assistant",
          content,
          sources,
          createdAt: new Date().toISOString(),
        },
      ],
    })),
  setLoading: (value: boolean) => set({ isLoading: value }),
  setError: (message?: string) => set({ error: message }),
  clear: () => set({ messages: [], error: undefined }),
}));

