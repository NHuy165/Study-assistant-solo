// ----- SUBJECT TYPE ----- //

export const SubjectType = {
  Maths: 'MATHS',
  Vietnamese: 'VIETNAMESE',
  English: 'ENGLISH',
} as const;

export type SubjectType = (typeof SubjectType)[keyof typeof SubjectType];

// ----- STUDY ACTIVITY ----- //

// === Format === //

export const StudyActivityFormatExercise = {
  MultipleChoiceQuestions: 'MULTIPLE_CHOICE_QUESTIONS',
  OpenEnded: 'OPEN_ENDED',
} as const;

export type StudyActivityFormatExercise =
  (typeof StudyActivityFormatExercise)[keyof typeof StudyActivityFormatExercise];

export const StudyActivityFormatReview = {
  Flashcards: 'FLASHCARDS',
} as const;

export type StudyActivityFormatReview =
  (typeof StudyActivityFormatReview)[keyof typeof StudyActivityFormatReview];

export const StudyActivityFormat = {
  ...StudyActivityFormatExercise,
  ...StudyActivityFormatReview,
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
} as const;

export type ReviewItemContentType =
  (typeof ReviewItemContentType)[keyof typeof ReviewItemContentType];

export const ExerciseItemContentType = {
  MultipleChoiceQuestionChoice: 'MULTIPLE_CHOICE_QUESTIONS_CHOICE',
  OpenEndedCorrect: 'OPEN_ENDED_CORRECT',
} as const;

export type ExerciseItemContentType =
  (typeof ExerciseItemContentType)[keyof typeof ExerciseItemContentType];
