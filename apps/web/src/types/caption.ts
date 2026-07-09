export type CaptionStyle = 'formal' | 'sarcastic' | 'humorous_tech' | 'humorous_non_tech';

export const CAPTION_STYLES: CaptionStyle[] = [
  'formal',
  'sarcastic',
  'humorous_tech',
  'humorous_non_tech'
];

export const STYLE_LABELS: Record<CaptionStyle, string> = {
  formal: 'Formal',
  sarcastic: 'Sarcastic',
  humorous_tech: 'Humorous (Tech)',
  humorous_non_tech: 'Humorous (Non-Tech)',
};
