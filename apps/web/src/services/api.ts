import { API_BASE_URL } from '@/lib/config';
import { CaptionsResponse } from '@/types/api';

export async function generateCaptions(file?: File, videoUrl?: string): Promise<CaptionsResponse> {
  const formData = new FormData();
  if (file) {
    formData.append('video', file);
  }
  if (videoUrl) {
    formData.append('video_url', videoUrl);
  }

  const res = await fetch(`${API_BASE_URL}/caption`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to generate captions');
  }

  return res.json();
}

export async function exportTxt(captions: Record<string, string>): Promise<Blob> {
  const res = await fetch(`${API_BASE_URL}/export/txt`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(captions),
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to export TXT');
  }

  return res.blob();
}

export async function exportVideo(file: File, captionText: string): Promise<Blob> {
  const formData = new FormData();
  formData.append('video', file);
  formData.append('caption_text', captionText);

  const res = await fetch(`${API_BASE_URL}/export/video`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to export video');
  }

  return res.blob();
}
