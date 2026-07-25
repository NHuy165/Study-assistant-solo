import { FormField } from '@/components/form-elements/FormField';
import { Button } from '@/components/miscellaneous/Button';
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
    <form
      className="card flex flex-col shadow-xl border border border-primary py-6 px-10 mt-6"
      onSubmit={handleSubmit(onSubmit)}
    >
      <h3 className="font-bold text-2xl mb-3">Create a new flashcard.</h3>

      {/* Front */}
      <FormField
        label="Front"
        name="front"
        inputStyle="w-full"
        labelStyle="font-semibold block mb-2"
        register={register}
        error={errors.front}
      />

      {/* Back */}
      <FormField
        label="Back"
        name="back"
        inputStyle="w-full"
        labelStyle="font-semibold block mb-2"
        register={register}
        error={errors.back}
      />

      <Button
        disabled={createFlashcards.isPending}
        style="mt-6"
        text="Create"
        textDisabled="Creating..."
        type="submit"
      />
    </form>
  );
};
