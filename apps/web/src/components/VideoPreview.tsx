'use client';

interface VideoPreviewProps {
  url: string;
  filename: string;
  onClear: () => void;
}

export default function VideoPreview({ url, filename, onClear }: VideoPreviewProps) {
  return (
    <div className="relative rounded-xl overflow-hidden bg-zinc-900 border border-zinc-800">
      <div className="absolute top-4 right-4 z-10">
        <button
          onClick={onClear}
          className="bg-black/60 hover:bg-black/80 text-white backdrop-blur-md px-3 py-1.5 rounded-lg text-sm font-medium transition-colors border border-zinc-700"
        >
          Change Video
        </button>
      </div>
      <video
        src={url}
        controls
        className="w-full max-h-[400px] object-contain bg-black"
      />
      <div className="p-4 border-t border-zinc-800 flex items-center justify-between">
        <span className="text-sm font-medium text-zinc-300 truncate max-w-full">
          {filename}
        </span>
      </div>
    </div>
  );
}
