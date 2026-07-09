'use client';

import { useState } from 'react';
import { CaptionStyle, STYLE_LABELS } from '@/types/caption';

interface CaptionCardProps {
  styleName: CaptionStyle;
  initialText: string;
  onUpdate: (styleName: CaptionStyle, text: string) => void;
}

export default function CaptionCard({ styleName, initialText, onUpdate }: CaptionCardProps) {
  const [text, setText] = useState(initialText);
  const [copied, setCopied] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setText(e.target.value);
    onUpdate(styleName, e.target.value);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="flex flex-col bg-zinc-900/50 border border-zinc-800 rounded-2xl overflow-hidden transition-all hover:border-zinc-600 focus-within:border-zinc-500 shadow-sm">
      <div className="flex items-center justify-between px-5 py-4 border-b border-zinc-800/50 bg-black/20">
        <h3 className="font-semibold text-white tracking-tight">{STYLE_LABELS[styleName]}</h3>
        <div className="flex items-center gap-3">
          <span className="text-xs text-zinc-600 font-medium">{text.length} chars</span>
          <button
            onClick={handleCopy}
            className="text-xs font-medium bg-zinc-800 hover:bg-zinc-700 text-zinc-300 hover:text-white px-3 py-1.5 rounded-md transition-colors active:scale-95"
          >
            {copied ? 'Copied!' : 'Copy'}
          </button>
        </div>
      </div>
      <textarea
        value={text}
        onChange={handleChange}
        className="w-full bg-transparent p-5 text-zinc-300 resize-y min-h-[140px] focus:outline-none leading-relaxed"
        placeholder={`Enter ${STYLE_LABELS[styleName]} caption...`}
      />
    </div>
  );
}
