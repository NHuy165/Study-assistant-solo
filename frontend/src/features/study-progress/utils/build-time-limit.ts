import {
  CriterionAttribute,
  CriterionOperator,
} from '@/features/study-progress/types/constants';
import type { CriterionInput } from '@/features/study-progress/types/study-progress';
import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc';

dayjs.extend(utc);

export const builtTimeLimit = (
  days: number,
  months: number,
  years: number,
): CriterionInput | null => {
  if (days === 0 && months === 0 && years === 0) {
    return null;
  }

  const timeCriterion: CriterionInput = {
    attribute: CriterionAttribute.CreatedAt,
    value: dayjs
      .utc()
      .subtract(days, 'days')
      .subtract(months, 'months')
      .subtract(years, 'years')
      .toISOString()
      .slice(0, 10),
    operator: CriterionOperator.GreaterThanEquals,
  };

  return timeCriterion;
};
