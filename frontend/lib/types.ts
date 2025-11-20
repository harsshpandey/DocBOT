export type ChatMessage = {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  sources?: SourceDocument[];
  createdAt: string;
};

export type SourceDocument = {
  name: string;
  relevance_score?: number | null;
  chunk_index?: number | null;
};

export type QueryResponse = {
  answer: string;
  sources: SourceDocument[];
  chunks_used: number;
  model: string;
  confidence?: number;
  processing_time_ms: number;
};

export type UploadResponse = {
  status: string;
  documents_indexed: number;
  chunks_created: number;
  embedding_provider: string;
  llm_provider: string;
  timestamp: string;
};

