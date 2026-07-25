import { TextArea } from '@/components/form-elements/TextArea';
import { useAnswerExerciseItem } from '@/features/study-activities/api/useAnswerExerciseItem';
import {
  type ExerciseItemAnswer,
  type ExerciseItemOutput,
  ExerciseItemAnswerSchema,
} from '@/features/study-activities/types/study-activity';
import { zodResolver } from '@hookform/resolvers/zod';
import { useCallback, useEffect, useState } from 'react';
import { type SubmitHandler, useForm, useWatch } from 'react-hook-form';

export const OpenEndedItem = ({
  exerciseItem,
  index,
}: {
  exerciseItem: ExerciseItemOutput;
  index: number;
}) => {
  const { mutate } = useAnswerExerciseItem();
  const [autosaveStatus, setAutosaveStatus] = useState('Autosave successful');

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
      mutate(
        {
          exerciseItemId: exerciseItem.id,
          exerciseItemAnswer: data,
        },
        {
          onSuccess: () => setAutosaveStatus('Autosave successful'),
          onError: () => setAutosaveStatus('Autosave failed'),
        },
      );
    },
    [mutate, exerciseItem.id],
  );

  const executeSubmit = useCallback(
    () => handleSubmit(onSubmit)(),
    [handleSubmit, onSubmit],
  );

  const currentAnswer = useWatch({ control, name: 'attempt' });

  // Debouncing (timed window of inactivity until answer request is sent)
  useEffect(() => {
    const resetAutosave = async () => {
      setAutosaveStatus('Autosave in progress');
    };

    // Makes sure to not send when the user hasn't typed anything because of the default conversion from null to '' by react hook form.
    if (currentAnswer === (exerciseItem.attempt ?? '')) {
      return;
    }

    resetAutosave();

    const timeoutId = setTimeout(() => {
      executeSubmit();
    }, 1000);

    return () => clearTimeout(timeoutId);
  }, [currentAnswer, executeSubmit, exerciseItem.attempt]);

  return (
    <li>
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
        {exerciseItem.user_score === null && (
          <span
            className={`block flex justify-end ${autosaveStatus === 'Autosave successful' ? 'text-success' : 'text-error'}`}
          >
            {autosaveStatus}
          </span>
        )}
        {exerciseItem.user_score !== null && (
          <span className="block text-success font-semibold text-lg mb-3">
            Score: {`${exerciseItem.user_score}/${exerciseItem.max_score}`}
          </span>
        )}
      </form>
      {exerciseItem.explanation && (
        <p>
          <span className="block font-bold mb-1">Explanation:</span>
          <span className="block h-30 border border-primary px-2 py-1 overflow-y-auto break-words whitespace-pre-wrap">
            {exerciseItem.explanation}
          </span>
        </p>
      )}
    </li>
  );
};
