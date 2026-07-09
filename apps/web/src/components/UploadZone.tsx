'use client';

import { useCallback, useRef, useState } from 'react';
import { MAX_VIDEO_SIZE_MB } from '@/lib/constants';

interface UploadZoneProps {
  onFileSelect: (file: File) => void;
}

export default function UploadZone({ onFileSelect }: UploadZoneProps) {
  const [isDragging, setIsDragging] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragging(false);
      if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
        onFileSelect(e.dataTransfer.files[0]);
      }
    },
    [onFileSelect]
  );

  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      if (e.target.files && e.target.files.length > 0) {
        onFileSelect(e.target.files[0]);
      }
    },
    [onFileSelect]
  );

  return (
    <div
      onClick={() => inputRef.current?.click()}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      className={`group relative cursor-pointer rounded-2xl border border-dashed transition-all duration-200 px-8 py-14 text-center
        ${isDragging
          ? 'border-[var(--color-accent)] bg-[var(--color-accent)]/[0.04] scale-[0.995]'
          : 'border-[var(--color-border)] bg-[var(--color-card)] hover:border-[color-mix(in_oklab,var(--color-border)_60%,var(--color-fg))]'}
      `}
    >
      <input
        type="file"
        ref={inputRef}
        onChange={handleChange}
        accept="video/mp4,video/quicktime,video/x-msvideo,video/webm,video/x-matroska"
        className="hidden"
      />
      <div className="flex flex-col items-center gap-5">
        <div
          className={`w-12 h-12 rounded-full flex items-center justify-center border transition-colors
            ${isDragging
              ? 'border-[var(--color-accent)] text-[var(--color-accent)]'
              : 'border-[var(--color-border)] text-[var(--color-muted)] group-hover:text-[var(--color-fg)]'}
          `}
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 16V4m0 0l-4 4m4-4l4 4M4 20h16" />
          </svg>
        </div>
        <div>
          <p className="text-[15px] font-medium text-[var(--color-fg)] tracking-tight">
            Upload Video
          </p>
          <p className="mt-1.5 text-xs text-[var(--color-muted)]">
            Drag & drop or click · MP4, MOV, WEBM · up to {MAX_VIDEO_SIZE_MB}MB · 2 min max
          </p>
        </div>
      </div>
    </div>
  );
}
