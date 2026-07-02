import { AggregateTarget } from '@/features/study-progress/types/constants';
import {
  StudyProgressOutputSchema,
  type CriteriaInput,
  type StudyProgressOutput,
} from '@/features/study-progress/types/study-progress';
import { apiFetchProtected } from '@/lib/api';
import { ResponseErrorSchema } from '@/types/error';

export const fetchStudyProgressRequest = async ({
  target,
  criteria,
}: {
  target: AggregateTarget;
  criteria: CriteriaInput;
}): Promise<StudyProgressOutput> => {
  // Sends the request and catches operational errors
  const options = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(criteria),
  };

  const response = await apiFetchProtected(
    `/study-progress?target=${target}`,
    options,
  );
  const rawData = await response.json();

  // Catches backend response errors
  if (!response.ok) {
    const validatedError = ResponseErrorSchema.parse(rawData);
    throw new Error(validatedError.message);
  }

  // Returns
  const validatedData = StudyProgressOutputSchema.parse(rawData);
  return validatedData;
};
