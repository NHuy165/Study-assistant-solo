import { TextArea } from '@/components/form-elements/TextArea';
import { useAnswerExerciseItem } from '@/features/study-activities/api/useAnswerExerciseItem';
import {
  type ExerciseItemAnswer,
  type ExerciseItemOutput,
  ExerciseItemAnswerSchema,
} from '@/features/study-activities/types/study-activity';
import { zodResolver } from '@hookform/resolvers/zod';
import { useCallback, useEffect } from 'react';
import { type SubmitHandler, useForm, useWatch } from 'react-hook-form';

export const OpenEndedItem = ({
  exerciseItem,
  index,
}: {
  exerciseItem: ExerciseItemOutput;
  index: number;
}) => {
  const answerExerciseItem = useAnswerExerciseItem();

  const {
    register,
    handleSubmit,
    control,
    formState: { errors },
  } = useForm<ExerciseItemAnswer>({
    resolver: zodResolver(ExerciseItemAnswerSchema),
    values: {
      attempt: exerciseItem.attempt ? exerciseItem.attempt : '',
    },
  });

  const onSubmit = useCallback<SubmitHandler<ExerciseItemAnswer>>(
    (data) => {
      answerExerciseItem.mutate({
        exerciseItemId: exerciseItem.id,
        exerciseItemAnswer: data,
      });
    },
    [answerExerciseItem, exerciseItem.id],
  );

  const executeSubmit = useCallback(
    () => handleSubmit(onSubmit)(),
    [handleSubmit, onSubmit],
  );

  const currentAnswer = useWatch({ control, name: 'attempt' });

  // Debouncing (timed window of inactivity until answer request is sent)
  useEffect(() => {
    // Makes sure to not send when the user hasn't typed anything because of the default conversion from null to '' by react hook form.
    if (currentAnswer === (exerciseItem.attempt ?? '')) {
      return;
    }

    const timeoutId = setTimeout(() => {
      executeSubmit();
    }, 1000);

    return () => clearTimeout(timeoutId);
  }, [currentAnswer, executeSubmit, exerciseItem.attempt]);

  return (
    <form>
      <TextArea
        label={`${index + 1}. ${exerciseItem.question}`}
        name="attempt"
        wrapperStyle="mb-0"
        labelStyle="font-semibold text-xl"
        inputStyle="block border border-primary w-full whitespace-pre-wrap h-30 overflow-y-auto break-words mt-3"
        register={register}
        disabled={exerciseItem.user_score !== null}
        error={errors.attempt}
      />
      {exerciseItem.user_score !== null && (
        <span className="block text-success font-semibold text-lg mb-3">
          Score: {`${exerciseItem.user_score}/${exerciseItem.max_score}`}
        </span>
      )}

      {exerciseItem.explanation && (
        <div>
          <span className="block font-bold mb-1">Explanation:</span>
          <span className="block h-30 border border-primary px-2 py-1 overflow-y-auto break-words whitespace-pre-wrap">
            {exerciseItem.explanation}
          </span>
        </div>
      )}
    </form>
  );
};
