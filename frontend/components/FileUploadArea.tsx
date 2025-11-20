"use client";

type Props = {
  onFilesSelected: (files: FileList) => void;
};

export function FileUploadArea({ onFilesSelected }: Props) {
  return (
    <label className="flex cursor-pointer flex-col rounded-xl border border-dashed border-slate-600 p-4 text-center text-sm text-slate-300 transition hover:border-emerald-500 hover:text-white">
      <input
        type="file"
        className="hidden"
        multiple
        onChange={(event) => {
          if (event.target.files?.length) {
            onFilesSelected(event.target.files);
          }
        }}
        accept=".pdf,.docx,.txt,.png,.jpg,.jpeg"
      />
      <span className="font-medium">Drop documents or click to upload</span>
      <span className="text-xs text-slate-500">
        PDF, DOCX, TXT, PNG, JPG (max 50MB each)
      </span>
    </label>
  );
}

