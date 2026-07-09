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

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      onFileSelect(e.dataTransfer.files[0]);
    }
  }, [onFileSelect]);

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      onFileSelect(e.target.files[0]);
    }
  }, [onFileSelect]);

  return (
    <div
      className={`relative overflow-hidden border-2 border-dashed rounded-2xl p-16 text-center cursor-pointer transition-all duration-300 ease-out group ${
        isDragging 
          ? 'border-[#ED1C24] bg-[#ED1C24]/5 scale-[0.98]' 
          : 'border-zinc-700 hover:border-zinc-500 hover:bg-zinc-900/30 hover:shadow-2xl hover:shadow-black/50'
      }`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      onClick={() => inputRef.current?.click()}
    >
      <input
        type="file"
        ref={inputRef}
        onChange={handleChange}
        accept="video/mp4,video/quicktime,video/x-msvideo,video/webm,video/x-matroska"
        className="hidden"
      />
      <div className="flex flex-col items-center gap-6 relative z-10 transition-transform duration-300 group-hover:-translate-y-1">
        <div className={`p-4 rounded-full transition-colors duration-300 ${isDragging ? 'bg-[#ED1C24]/20 text-[#ED1C24]' : 'bg-zinc-800 text-zinc-300 group-hover:bg-zinc-700 group-hover:text-white'}`}>
          <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
        </div>
        <div>
          <p className="text-xl font-semibold text-white mb-2 tracking-tight">Click or drag a video to upload</p>
          <p className="text-sm text-zinc-500 font-medium">MP4, MOV, WEBM (Max {MAX_VIDEO_SIZE_MB}MB, Max 2 min)</p>
        </div>
      </div>
    </div>
  );
}
