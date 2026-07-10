import { useState, useCallback } from 'react';
import { ALLOWED_VIDEO_TYPES, MAX_VIDEO_SIZE_MB } from '@/lib/constants';

export function useFileUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [remoteUrl, setRemoteUrl] = useState<string | null>(null);
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
    setRemoteUrl(null); // Clear remote url if file is selected
    return true;
  }, []);

  const handleUrl = useCallback((url: string) => {
    setError(null);
    if (!url || !url.startsWith('http')) {
      setError('Please provide a valid publicly accessible URL.');
      return false;
    }
    if (!url.toLowerCase().endsWith('.mp4') && !url.includes('mp4')) {
      setError('Please provide a URL to an MP4 video.');
      return false;
    }
    
    setRemoteUrl(url);
    setPreviewUrl(url);
    setFile(null); // Clear local file if url is provided
    return true;
  }, []);

  const clearFile = useCallback(() => {
    setFile(null);
    if (previewUrl && !remoteUrl) {
      URL.revokeObjectURL(previewUrl);
    }
    setPreviewUrl(null);
    setRemoteUrl(null);
    setError(null);
  }, [previewUrl, remoteUrl]);

  return { file, remoteUrl, previewUrl, error, handleFile, handleUrl, clearFile };
}
