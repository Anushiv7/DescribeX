'use client';

import { useState } from 'react';

interface ExportBarProps {
  onExportTxt: () => Promise<void>;
  onExportVideo: () => Promise<void>;
}

export default function ExportBar({ onExportTxt, onExportVideo }: ExportBarProps) {
  const [isExportingTxt, setIsExportingTxt] = useState(false);
  const [isExportingVideo, setIsExportingVideo] = useState(false);

  const handleExportTxt = async () => {
    setIsExportingTxt(true);
    try {
      await onExportTxt();
    } finally {
      setIsExportingTxt(false);
    }
  };

  const handleExportVideo = async () => {
    setIsExportingVideo(true);
    try {
      await onExportVideo();
    } finally {
      setIsExportingVideo(false);
    }
  };

  return (
    <div className="flex flex-col sm:flex-row gap-4 items-center justify-end mt-12 pt-8 border-t border-zinc-800/50">
      <button
        onClick={handleExportTxt}
        disabled={isExportingTxt || isExportingVideo}
        className="w-full sm:w-auto px-8 py-3.5 rounded-xl font-medium text-white bg-zinc-800 hover:bg-zinc-700 disabled:opacity-50 transition-all hover:shadow-lg active:scale-[0.98]"
      >
        {isExportingTxt ? 'Exporting...' : 'Download TXT'}
      </button>
      
      <button
        onClick={handleExportVideo}
        disabled={isExportingTxt || isExportingVideo}
        className="w-full sm:w-auto px-8 py-3.5 rounded-xl font-semibold text-white bg-[#ED1C24] hover:bg-[#E30613] disabled:opacity-50 transition-all hover:shadow-lg hover:shadow-[#ED1C24]/20 active:scale-[0.98] flex items-center justify-center gap-2"
      >
        {isExportingVideo ? (
          <>
            <span className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
            Burning Video...
          </>
        ) : (
          'Burn Captions'
        )}
      </button>
    </div>
  );
}
