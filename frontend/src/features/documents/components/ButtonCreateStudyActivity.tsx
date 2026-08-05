import { Button } from '@/components/miscellaneous/Button';
import { useCreateStudyActivity } from '@/features/study-activities/api/useCreateStudyActivity';
import type { StudyActivityInput } from '@/features/study-activities/types/study-activity';
import { capitalizeString, replaceUnderscore } from '@/utils/format-string';

export const ButtonCreateStudyActivity = ({
  interactionId,
  studyActivityInput,
}: {
  interactionId: number;
  studyActivityInput: StudyActivityInput;
}) => {
  const createStudyActivity = useCreateStudyActivity();

  return (
    <li className="flex justify-center items-center h-30">
      <Button
        text="Generate activity"
        textDisabled="Generating..."
        style="h-30 rounded-none shadow-xl w-1/6"
        disabled={createStudyActivity.isPending}
        onClick={() =>
          createStudyActivity.mutate({ interactionId, studyActivityInput })
        }
      />
      <div className="shadow-xl border border-primary px-3 py-1 h-30 whitespace-pre-wrap overflow-y-auto flex-1">
        <p>
          <span className="font-bold">Prompt: </span>{' '}
          {studyActivityInput.prompt}
        </p>
        <p>
          <span className="font-bold">Subject type: </span>{' '}
          {capitalizeString(replaceUnderscore(studyActivityInput.subject_type))}
        </p>
        <p>
          <span className="font-bold">Study activity format: </span>{' '}
          {capitalizeString(
            replaceUnderscore(studyActivityInput.activity_format),
          )}
        </p>
      </div>
    </li>
  );
};
