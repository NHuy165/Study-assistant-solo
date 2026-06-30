import { useSubmitExercise } from '@/features/study-activities/api/useSubmitExercise';
import { MultipleChoiceQuestionItem } from '@/features/study-activities/components/study-activity-items/MultipleChoiceQuestionItem';
import { OpenEndedItem } from '@/features/study-activities/components/study-activity-items/OpenEndedItem';
import type {
  ExerciseItemOutput,
  StudyActivityOutputComplete,
} from '@/features/study-activities/types/study-activity';
import { StudyActivityFormat } from '@/types/constants';

export const ExerciseWorkspace = ({
  studyActivity,
}: {
  studyActivity: StudyActivityOutputComplete;
}) => {
  const submitExercise = useSubmitExercise();

  const handleClick = () => {
    submitExercise.mutate(studyActivity.id);
  };

  return (
    <div>
      {studyActivity.items.map((exerciseItem) => {
        switch (studyActivity.activity_format) {
          case StudyActivityFormat.MultipleChoiceQuestions:
            return (
              <MultipleChoiceQuestionItem
                key={exerciseItem.id}
                exerciseItem={exerciseItem as ExerciseItemOutput}
              />
            );
          case StudyActivityFormat.OpenEnded:
            return (
              <OpenEndedItem
                key={exerciseItem.id}
                exerciseItem={exerciseItem as ExerciseItemOutput}
              />
            );
        }
      })}

      <br />

      <button onClick={handleClick} disabled={studyActivity.is_submitted}>
        {submitExercise.isPending ? 'Submitting...' : 'Submit exercise'}
      </button>

      {submitExercise.isError && <p>{submitExercise.error.message}</p>}
      {submitExercise.isPending && (
        <p>Submitting study activity, please wait.</p>
      )}
    </div>
  );
};
