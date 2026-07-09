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
    setTimeout(() => setCopied(false), 1600);
  };

  return (
    <div className="group flex flex-col rounded-2xl border border-[var(--color-border)] bg-[var(--color-card)] overflow-hidden transition-colors focus-within:border-[var(--color-accent)]/60 hover:border-[color-mix(in_oklab,var(--color-border)_60%,var(--color-fg))]">
      <div className="flex items-center justify-between px-5 py-3.5 border-b border-[var(--color-border)]">
        <h3 className="text-sm font-semibold tracking-tight text-[var(--color-fg)]">
          {STYLE_LABELS[styleName]}
        </h3>
        <button
          onClick={handleCopy}
          className="text-xs font-medium text-[var(--color-muted)] hover:text-[var(--color-fg)] transition-colors active:scale-95"
        >
          {copied ? 'Copied' : 'Copy'}
        </button>
      </div>
      <textarea
        value={text}
        onChange={handleChange}
        placeholder={`Enter ${STYLE_LABELS[styleName]} caption...`}
        className="w-full bg-transparent px-5 py-4 text-[15px] leading-relaxed text-[var(--color-fg)] resize-y min-h-[160px] focus:outline-none placeholder:text-[var(--color-muted)]/60"
      />
      <div className="px-5 py-2.5 border-t border-[var(--color-border)] flex justify-end">
        <span className="text-[11px] tracking-wider uppercase text-[var(--color-muted)]">
          {text.length} chars
        </span>
      </div>
    </div>
  );
}
