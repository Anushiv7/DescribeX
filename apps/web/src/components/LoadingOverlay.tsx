'use client';

interface LoadingOverlayProps {
  message: string;
}

// NOTE: labels must stay identical to what useCaptionGeneration emits
// so indexOf(message) keeps working.
const PIPELINE_STEPS = [
  'Uploading video...',
  'Extracting frames...',
  'Analyzing scene...',
  'Generating caption styles...',
  'Almost done...',
];

export default function LoadingOverlay({ message }: LoadingOverlayProps) {
  const currentIndex = PIPELINE_STEPS.indexOf(message);

  return (
    <div className="w-full">
      <ol className="space-y-3">
        {PIPELINE_STEPS.map((step, index) => {
          const isCompleted = currentIndex > index;
          const isActive = currentIndex === index;
          return (
            <li
              key={step}
              className={`flex items-center gap-3 text-sm transition-opacity ${
                isActive ? 'opacity-100' : isCompleted ? 'opacity-70' : 'opacity-40'
              }`}
            >
              <span
                className={`w-5 h-5 rounded-full flex items-center justify-center border flex-shrink-0 ${
                  isCompleted
                    ? 'bg-[var(--color-accent)] border-[var(--color-accent)] text-white'
                    : isActive
                    ? 'border-[var(--color-accent)]'
                    : 'border-[var(--color-border)]'
                }`}
              >
                {isCompleted ? (
                  <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={3}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                ) : isActive ? (
                  <span className="w-1.5 h-1.5 rounded-full bg-[var(--color-accent)] animate-pulse" />
                ) : null}
              </span>
              <span className={isActive ? 'text-[var(--color-fg)]' : 'text-[var(--color-muted)]'}>
                {step}
              </span>
            </li>
          );
        })}
      </ol>
      <p className="mt-6 text-xs text-[var(--color-muted)]">Usually takes 1–2 minutes.</p>
    </div>
  );
}
