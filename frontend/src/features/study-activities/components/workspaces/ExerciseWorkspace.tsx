import { Button } from '@/components/miscellaneous/Button';
import { useSubmitExercise } from '@/features/study-activities/api/useSubmitExercise';
import { MultipleChoiceQuestionItem } from '@/features/study-activities/components/study-activity-items/MultipleChoiceQuestionItem';
import { OpenEndedItem } from '@/features/study-activities/components/study-activity-items/OpenEndedItem';
import type {
  ExerciseItemOutput,
  StudyActivityOutputComplete,
} from '@/features/study-activities/types/study-activity';
import { StudyActivityFormat } from '@/types/constants';
import { titleString, replaceUnderscore } from '@/utils/format-string';

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
    <section className="border border-primary p-4 space-y-6">
      <h2 className="font-bold text-4xl text-center mb-6">
        {titleString(replaceUnderscore(studyActivity.activity_format))}
      </h2>
      <ol>
        {studyActivity.items.map((exerciseItem, index) => {
          switch (studyActivity.activity_format) {
            case StudyActivityFormat.MultipleChoiceQuestions:
              return (
                <MultipleChoiceQuestionItem
                  key={exerciseItem.id}
                  exerciseItem={exerciseItem as ExerciseItemOutput}
                  index={index}
                />
              );
            case StudyActivityFormat.OpenEnded:
              return (
                <OpenEndedItem
                  key={exerciseItem.id}
                  exerciseItem={exerciseItem as ExerciseItemOutput}
                  index={index}
                />
              );
          }
        })}
      </ol>

      <Button
        style="w-full"
        text="Submit"
        textDisabled={studyActivity.is_submitted ? 'Submitted' : 'Submitting'}
        disabled={submitExercise.isPending || studyActivity.is_submitted}
        onClick={handleClick}
      />
    </section>
  );
};
