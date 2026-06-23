export const capitalizeString = (s: string): string => {
  if (!s) {
    return s;
  }
  return s.charAt(0).toUpperCase() + s.slice(1).toLowerCase();
};

export const titleString = (s: string): string => {
  return s
    .split(' ')
    .map((word) => capitalizeString(word))
    .join(' ');
};

export const replaceUnderscore = (s: string): string => {
  return s.replaceAll('_', ' ');
};
