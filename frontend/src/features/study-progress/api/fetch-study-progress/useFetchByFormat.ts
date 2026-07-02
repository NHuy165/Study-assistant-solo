import { fetchStudyProgressRequest } from '@/features/study-progress/api/fetch-study-progress/fetch-study-progress-request';
import {
  AggregateTarget,
  CriterionAttribute,
  CriterionOperator,
} from '@/features/study-progress/types/constants';
import {
  type CriterionInput,
  type ObjectsGroupByFormat,
} from '@/features/study-progress/types/study-progress';
import { builtTimeLimit } from '@/features/study-progress/utils/build-time-limit';
import { StudyActivityFormat } from '@/types/constants';
import { useQuery } from '@tanstack/react-query';

export const useFetchByFormat = (
  aggregateTarget: AggregateTarget,
  days: number = 0,
  months: number = 0,
  years: number = 0,
) => {
  // Establishes target and basic criteria
  const groupByFormat: CriterionInput = {
    attribute: CriterionAttribute.ActivityFormat,
    value: null,
    operator: CriterionOperator.GroupBy,
  };

  // Function for fetching study activities by format
  const fetch = async (): Promise<ObjectsGroupByFormat> => {
    const criteria: CriterionInput[] = [groupByFormat];

    // Time limit building
    const timeCriterion = builtTimeLimit(days, months, years);
    if (timeCriterion) {
      criteria.push(timeCriterion);
    }

    const backendData = await fetchStudyProgressRequest({
      target: aggregateTarget,
      criteria: criteria,
    });

    // format: 0
    const defaultValues = Object.fromEntries(
      Object.values(StudyActivityFormat).map((format) => [format, 0]),
    );

    // Backend data
    const formattedBackendData = Object.fromEntries(
      backendData.map(([count, format]) => [format, count]),
    );

    // Backend data, missing subjects will be auto-filled with 0
    const finalValues = {
      ...defaultValues,
      ...formattedBackendData,
    } as ObjectsGroupByFormat;

    return finalValues;
  };

  return useQuery({
    queryKey: [
      'study-progress',
      aggregateTarget,
      [groupByFormat],
      [days, months, years],
    ],
    queryFn: fetch,
  });
};
