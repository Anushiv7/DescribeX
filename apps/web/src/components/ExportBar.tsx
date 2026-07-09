'use client';

import { useState } from 'react';

interface ExportBarProps {
  onExportTxt: () => Promise<void>;
  onExportVideo: () => Promise<void>;
}

export default function ExportBar({ onExportTxt, onExportVideo }: ExportBarProps) {
  const [isExportingTxt, setIsExportingTxt] = useState(false);
  const [isExportingVideo, setIsExportingVideo] = useState(false);
  const busy = isExportingTxt || isExportingVideo;

  const handleExportTxt = async () => {
    setIsExportingTxt(true);
    try { await onExportTxt(); } finally { setIsExportingTxt(false); }
  };

  const handleExportVideo = async () => {
    setIsExportingVideo(true);
    try { await onExportVideo(); } finally { setIsExportingVideo(false); }
  };

  return (
    <div className="mt-8 py-14 rounded-3xl border border-[var(--color-border)] bg-[var(--color-card)] flex flex-col items-center text-center">
      <h3 className="text-2xl font-semibold tracking-tight text-[var(--color-fg)]">Ready to Export</h3>
      <p className="mt-2 text-sm text-[var(--color-muted)]">
        Download the caption text or burn them directly into your video.
      </p>
      <div className="mt-8 flex flex-col sm:flex-row gap-3">
        <button
          onClick={handleExportTxt}
          disabled={busy}
          className="min-w-[200px] px-7 py-3.5 rounded-xl font-medium text-[var(--color-fg)] border border-[var(--color-border)] bg-transparent hover:bg-[color-mix(in_oklab,var(--color-card)_60%,var(--color-fg)_5%)] disabled:opacity-50 transition-colors active:scale-[0.99]"
        >
          {isExportingTxt ? 'Exporting…' : 'Download TXT'}
        </button>
        <button
          onClick={handleExportVideo}
          disabled={busy}
          className="min-w-[240px] px-7 py-3.5 rounded-xl font-semibold text-white bg-[var(--color-accent)] hover:bg-[var(--color-accent-hover)] disabled:opacity-50 transition-all duration-200 ease-out shadow-[0_10px_40px_-10px_rgba(202,5,5,0.25)] inline-flex items-center justify-center gap-2"
        >
          {isExportingVideo ? (
            <>
              <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              Burning…
            </>
          ) : (
            'Burn Captions Into Video'
          )}
        </button>
      </div>
    </div>
  );
}
