import { FormField } from '@/components/form-elements/FormField';
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
}: {
  exerciseItem: ExerciseItemOutput;
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
    () => handleSubmit(onSubmit)(), // Handle submit inserts form data for us
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
      <FormField
        label={`${exerciseItem.question} (Score: ${exerciseItem.user_score || 'X'}/${exerciseItem.max_score})`}
        name="attempt"
        register={register}
        disabled={exerciseItem.user_score !== null}
        error={errors.attempt}
      />

      {exerciseItem.explanation && (
        <>
          <br /> {exerciseItem.explanation}
        </>
      )}
    </form>
  );
};
