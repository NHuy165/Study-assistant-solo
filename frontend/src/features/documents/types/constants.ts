export const DocumentType = {
  Pdf: 'PDF',
  Image: 'IMAGE',
  Text: 'TEXT',
} as const;

export type DocumentType = (typeof DocumentType)[keyof typeof DocumentType];
