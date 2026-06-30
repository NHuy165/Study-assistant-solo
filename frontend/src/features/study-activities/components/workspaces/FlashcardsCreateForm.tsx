import { FormField } from '@/components/form-elements';
import { SubmitButton } from '@/components/SubmitButton';
import { useCreateFlashcards } from '@/features/study-activities/api/useCreateFlashcards';
import {
  type FlashcardInputSingle,
  FlashcardInputSingleSchema,
} from '@/features/study-activities/types/study-activity';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm, type SubmitHandler } from 'react-hook-form';

export const FlashcardsCreateForm = ({
  reviewActivityId,
}: {
  reviewActivityId: number;
}) => {
  const createFlashcards = useCreateFlashcards();

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<FlashcardInputSingle>({
    resolver: zodResolver(FlashcardInputSingleSchema),
    defaultValues: {
      front: '',
      back: '',
    },
  });

  const onSubmit: SubmitHandler<FlashcardInputSingle> = (data) => {
    createFlashcards.mutate(
      { reviewActivityId, flashcardsInput: [data] },
      { onSuccess: () => reset() },
    );
  };

  return (
    <div>
      {createFlashcards.isError && <p>{createFlashcards.error.message}</p>}
      {createFlashcards.isPending && <p>Adding flashcard, please wait.</p>}

      <form onSubmit={handleSubmit(onSubmit)}>
        {/* Front */}
        <FormField
          label="Front"
          name="front"
          register={register}
          error={errors.front}
        />

        <br />

        {/* Back */}
        <FormField
          label="Back"
          name="back"
          register={register}
          error={errors.back}
        />

        <br />

        <SubmitButton
          disabled={createFlashcards.isPending}
          text="Create"
          textDisabled="Creating..."
        />
      </form>
    </div>
  );
};
