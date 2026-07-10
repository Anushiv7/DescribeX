import { useState, useCallback } from 'react';
import { generateCaptions } from '@/services/api';
import { CaptionsResponse } from '@/types/api';

type Status = 'idle' | 'processing' | 'done' | 'error';

const LOADING_MESSAGES = [
  'Uploading video...',
  'Extracting frames...',
  'Analyzing scene...',
  'Generating caption styles...',
  'Almost done...',
];

export function useCaptionGeneration() {
  const [status, setStatus] = useState<Status>('idle');
  const [loadingMessageIndex, setLoadingMessageIndex] = useState(0);
  const [captions, setCaptions] = useState<CaptionsResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const generate = useCallback(async (file?: File | null, videoUrl?: string | null) => {
    setStatus('processing');
    setError(null);
    setCaptions(null);
    setLoadingMessageIndex(0);

    // Simulate progress through messages
    const messageInterval = setInterval(() => {
      setLoadingMessageIndex((prev) => 
        prev < LOADING_MESSAGES.length - 1 ? prev + 1 : prev
      );
    }, 15000); // Change message every 15 seconds

    try {
      const result = await generateCaptions(file || undefined, videoUrl || undefined);
      setCaptions(result);
      setStatus('done');
    } catch (err: any) {
      setError(err.message || 'An unexpected error occurred during generation.');
      setStatus('error');
    } finally {
      clearInterval(messageInterval);
    }
  }, []);

  const reset = useCallback(() => {
    setStatus('idle');
    setCaptions(null);
    setError(null);
    setLoadingMessageIndex(0);
  }, []);

  return {
    status,
    loadingMessage: LOADING_MESSAGES[loadingMessageIndex],
    captions,
    error,
    generate,
    reset
  };
}
