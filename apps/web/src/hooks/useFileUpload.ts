import { useState, useCallback } from 'react';
import { ALLOWED_VIDEO_TYPES, MAX_VIDEO_SIZE_MB } from '@/lib/constants';

export function useFileUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFile = useCallback((selectedFile: File) => {
    setError(null);
    
    if (!ALLOWED_VIDEO_TYPES.includes(selectedFile.type)) {
      setError('Please upload a valid video file (MP4, MOV, AVI, WEBM, MKV).');
      return false;
    }

    if (selectedFile.size > MAX_VIDEO_SIZE_MB * 1024 * 1024) {
      setError(`File size must be less than ${MAX_VIDEO_SIZE_MB}MB.`);
      return false;
    }

    setFile(selectedFile);
    const url = URL.createObjectURL(selectedFile);
    setPreviewUrl(url);
    return true;
  }, []);

  const clearFile = useCallback(() => {
    setFile(null);
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }
    setPreviewUrl(null);
    setError(null);
  }, [previewUrl]);

  return { file, previewUrl, error, handleFile, clearFile };
}
