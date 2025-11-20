import axios from "axios";
import type { QueryResponse, UploadResponse } from "./types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

export const uploadDocuments = async (files: File[]) => {
  const formData = new FormData();
  files.forEach((file) => formData.append("files", file));
  const { data } = await client.post<UploadResponse>("/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
};

export const askQuestion = async (question: string) => {
  const { data } = await client.post<QueryResponse>("/query", null, {
    params: { question },
  });
  return data;
};

export const healthCheck = async () => {
  const { data } = await client.get("/health");
  return data;
};

