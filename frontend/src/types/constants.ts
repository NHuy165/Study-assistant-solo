// ----- SUBJECT TYPE ----- //

export const SubjectType = {
  Maths: 'MATHS',
  Vietnamese: 'VIETNAMESE',
  English: 'ENGLISH',
} as const;

export type SubjectType = (typeof SubjectType)[keyof typeof SubjectType];

// ----- DOCUMENT TYPE ----- //

export const DocumentType = {
  Pdf: 'PDF',
  Image: 'IMAGE',
  Text: 'TEXT',
} as const;

export type DocumentType = (typeof DocumentType)[keyof typeof DocumentType];

// ----- STUDY ACTIVITY ----- //

// === FORMAT === //

export const StudyActivityFormat = {
  MultipleChoiceQuestions: 'MULTIPLE_CHOICE_QUESTIONS',
  OpenEnded: 'OPEN_ENDED',
  Flashcards: 'FLASHCARDS',
  GapFill: 'GAP_FILL',
} as const;

export type StudyActivityFormat =
  (typeof StudyActivityFormat)[keyof typeof StudyActivityFormat];
