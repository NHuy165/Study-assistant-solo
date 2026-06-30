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

// === Format === //

export const StudyActivityFormat = {
  MultipleChoiceQuestions: 'MULTIPLE_CHOICE_QUESTIONS',
  OpenEnded: 'OPEN_ENDED',
  Flashcards: 'FLASHCARDS',
} as const;

export type StudyActivityFormat =
  (typeof StudyActivityFormat)[keyof typeof StudyActivityFormat];

// === Study Activity Type === //

export const StudyActivityType = {
  Exercise: 'EXERCISE',
  Review: 'REVIEW',
} as const;

export type StudyActivityType =
  (typeof StudyActivityType)[keyof typeof StudyActivityType];

// === Study Activity Item Content Type === //

export const ReviewItemContentType = {
  FlashcardFront: 'FLASHCARDS_FRONT',
  FlashcardBack: 'FLASHCARDS_BACK',
};

export const ExerciseItemContentType = {
  MultipleChoiceQuestionChoice: 'MULTIPLE_CHOICE_QUESTIONS_CHOICE',
  OpenEndedCorrect: 'OPEN_ENDED_CORRECT',
};
