export type SelectOption = {
  label: string;
  value: string | number;
};

export type RadioOption = {
  label: string;
  value: number;
  isCorrect: boolean | null;
};
