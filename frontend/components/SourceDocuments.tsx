"use client";

import type { SourceDocument } from "../lib/types";

type Props = {
  sources?: SourceDocument[];
};

export function SourceDocuments({ sources }: Props) {
  if (!sources?.length) return null;

  return (
    <div className="mt-3 rounded-lg border border-slate-800 bg-slate-900/50 p-3">
      <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
        Sources
      </p>
      <ul className="mt-2 space-y-1 text-sm text-slate-300">
        {sources.map((source, index) => (
          <li key={`${source.name}-${index}`} className="flex items-center">
            <span className="mr-2 h-1 w-1 rounded-full bg-emerald-400"></span>
            <span>{source.name}</span>
            {typeof source.relevance_score === "number" && (
              <span className="ml-auto text-xs text-slate-500">
                {(source.relevance_score * 100).toFixed(0)}%
              </span>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

