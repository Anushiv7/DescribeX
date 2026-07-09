'use client';

interface VideoPreviewProps {
  url: string;
  filename: string;
  onClear: () => void;
}

export default function VideoPreview({ url, filename, onClear }: VideoPreviewProps) {
  return (
    <div className="rounded-2xl overflow-hidden border border-[var(--color-border)] bg-[var(--color-card)]">
      <div className="relative bg-black">
        <button
          onClick={onClear}
          className="absolute top-3 right-3 z-10 px-3 py-1.5 rounded-lg text-xs font-medium bg-black/60 border border-[var(--color-border)] text-[var(--color-fg)] hover:bg-black/80 backdrop-blur-md transition-colors"
        >
          Change Video
        </button>
        <video src={url} controls className="w-full max-h-[520px] object-contain" />
      </div>
      <div className="flex items-center justify-between px-5 py-3 border-t border-[var(--color-border)]">
        <span className="text-xs text-[var(--color-muted)] truncate">{filename}</span>
      </div>
    </div>
  );
}
