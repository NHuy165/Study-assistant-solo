import { RadioGroupField } from '@/components/form-elements/RadioField';
import { useAnswerExerciseItem } from '@/features/study-activities/api/useAnswerExerciseItem';
import {
  type ExerciseItemAnswer,
  type ExerciseItemOutput,
  ExerciseItemAnswerSchema,
} from '@/features/study-activities/types/study-activity';
import { zodResolver } from '@hookform/resolvers/zod';
import { type SubmitHandler, useForm, useWatch } from 'react-hook-form';

export const MultipleChoiceQuestionItem = ({
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
      attempt: exerciseItem.attempt ? exerciseItem.attempt : '', // Needs to stay a string because so the default choice works (HTML radio button value is always a string)
    },
  });

  const onSubmit: SubmitHandler<ExerciseItemAnswer> = (data) => {
    answerExerciseItem.mutate({
      exerciseItemId: exerciseItem.id,
      exerciseItemAnswer: { ...data, attempt: Number(data.attempt) },
    });
  };

  // Real input will only be a number
  const currentAnswer = Number(useWatch({ control, name: 'attempt' }));

  return (
    <form onChange={() => handleSubmit(onSubmit)()}>
      <RadioGroupField
        label={`${index + 1}. ${exerciseItem.question}`}
        name="attempt"
        labelStyle="font-semibold text-xl"
        optionStyle="m-0"
        optionTextStyle="ml-3"
        optionsWrapperStyle="flex flex-col gap-1 mt-2"
        currentAnswer={currentAnswer}
        // The label is the content, the value is the id
        options={exerciseItem.contents.map((exerciseItemContent) => {
          return {
            label: exerciseItemContent.content as string,
            value: exerciseItemContent.id,
            isCorrect: exerciseItemContent.is_correct,
          };
        })}
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
          <span className="block h-20 border border-primary px-2 py-1 overflow-y-auto break-words whitespace-pre-wrap">
            {exerciseItem.explanation}
          </span>
        </div>
      )}
    </form>
  );
};
