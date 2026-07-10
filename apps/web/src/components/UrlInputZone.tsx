'use client';

import { useState } from 'react';

interface UrlInputZoneProps {
  onUrlSubmit: (url: string) => void;
}

export default function UrlInputZone({ onUrlSubmit }: UrlInputZoneProps) {
  const [url, setUrl] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (url.trim()) {
      onUrlSubmit(url.trim());
    }
  };

  return (
    <div className="rounded-2xl border border-[var(--color-border)] bg-[var(--color-card)] px-8 py-10 transition-all duration-200 hover:border-[color-mix(in_oklab,var(--color-border)_60%,var(--color-fg))]">
      <div className="flex flex-col items-center gap-5">
        <div className="w-12 h-12 rounded-full flex items-center justify-center border border-[var(--color-border)] text-[var(--color-muted)] transition-colors group-hover:text-[var(--color-fg)]">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
          </svg>
        </div>
        
        <div className="text-center w-full max-w-md">
          <p className="text-[15px] font-medium text-[var(--color-fg)] tracking-tight">
            Video URL
          </p>
          <p className="mt-1.5 text-xs text-[var(--color-muted)] mb-6">
            Paste a publicly accessible MP4 URL.
          </p>
          
          <form onSubmit={handleSubmit} className="flex gap-2">
            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://example.com/video.mp4"
              className="flex-1 bg-transparent border border-[var(--color-border)] rounded-xl px-4 py-2 text-sm text-[var(--color-fg)] placeholder:text-[var(--color-muted)] focus:outline-none focus:border-[var(--color-accent)] focus:ring-1 focus:ring-[var(--color-accent)] transition-all"
              required
            />
            <button
              type="submit"
              disabled={!url.trim()}
              className="px-4 py-2 bg-[var(--color-fg)] text-[var(--color-bg)] rounded-xl text-sm font-medium hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed transition-opacity"
            >
              Set URL
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
