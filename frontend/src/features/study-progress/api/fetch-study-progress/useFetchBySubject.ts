import { fetchStudyProgressRequest } from '@/features/study-progress/api/fetch-study-progress/fetch-study-progress-request';
import {
  AggregateTarget,
  CriterionAttribute,
  CriterionOperator,
} from '@/features/study-progress/types/constants';
import {
  type CriterionInput,
  type ObjectsGroupBySubject,
} from '@/features/study-progress/types/study-progress';
import { builtTimeLimit } from '@/features/study-progress/utils/build-time-limit';
import { SubjectType } from '@/types/constants';
import { useQuery } from '@tanstack/react-query';

export const useFetchBySubject = (
  aggregateTarget: AggregateTarget,
  days: number = 0,
  months: number = 0,
  years: number = 0,
) => {
  // Establishes target and basic criteria
  const groupBySubject: CriterionInput = {
    attribute: CriterionAttribute.SubjectType,
    value: null,
    operator: CriterionOperator.GroupBy,
  };

  // Function for fetching study activities by subject
  const fetch = async (): Promise<ObjectsGroupBySubject> => {
    const criteria: CriterionInput[] = [groupBySubject];

    // Time limit building
    const timeCriterion = builtTimeLimit(days, months, years);
    if (timeCriterion) {
      criteria.push(timeCriterion);
    }

    const backendData = await fetchStudyProgressRequest({
      target: aggregateTarget,
      criteria: criteria,
    });

    // subject: 0
    const defaultValues = Object.fromEntries(
      Object.values(SubjectType).map((subject) => [subject, 0]),
    );

    // Backend data
    const formattedBackendData = Object.fromEntries(
      backendData.map(([count, subject]) => [subject, count]),
    );

    // Backend data, missing subjects will be auto-filled with 0
    const finalValues = {
      ...defaultValues,
      ...formattedBackendData,
    } as ObjectsGroupBySubject;

    return finalValues;
  };

  return useQuery({
    queryKey: [
      'study-progress',
      aggregateTarget,
      [groupBySubject],
      [days, months, years],
    ],
    queryFn: fetch,
  });
};
