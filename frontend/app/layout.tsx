import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "DocBot",
  description: "AI assistant for organizational policies and guidelines",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-950 text-white">{children}</body>
    </html>
  );
}

