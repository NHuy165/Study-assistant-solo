import { FormField } from '@/components/form-elements/FormField';
import { Button } from '@/components/miscellaneous/Button';
import { useUpdateFlashcard } from '@/features/study-activities/api/useUpdateFlashcard';
import {
  FlashcardUpdateSchema,
  type FlashcardUpdate,
  type ReviewItemOutput,
} from '@/features/study-activities/types/study-activity';
import { ReviewItemContentType } from '@/types/constants';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm, type SubmitHandler } from 'react-hook-form';

export const FlashcardUpdateForm = ({
  reviewItem,
  onUpdate,
}: {
  reviewItem: ReviewItemOutput;
  onUpdate: () => void;
}) => {
  const frontContent = reviewItem.contents.find(
    (reviewItemContent) =>
      reviewItemContent.type === ReviewItemContentType.FlashcardFront,
  )?.content as string;
  const backContent = reviewItem.contents.find(
    (reviewItemContent) =>
      reviewItemContent.type === ReviewItemContentType.FlashcardBack,
  )?.content as string;

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FlashcardUpdate>({
    resolver: zodResolver(FlashcardUpdateSchema),
    values: {
      front: frontContent,
      back: backContent,
    },
  });
  const updateFlashcard = useUpdateFlashcard();

  const onSubmit: SubmitHandler<FlashcardUpdate> = (data) => {
    updateFlashcard.mutate(
      {
        reviewItemId: reviewItem.id,
        flashcardUpdate: data,
      },
      { onSuccess: () => onUpdate() },
    );
  };

  return (
    <div className="card shadow-xl border border border-primary mt-3 mb-6 p-6">
      <form onSubmit={handleSubmit(onSubmit)}>
        {/* Front */}
        <FormField
          label="Front"
          name="front"
          inputStyle="w-1/1"
          labelStyle="font-semibold block mb-2"
          register={register}
          error={errors.front}
        />
        {/* Back */}
        <FormField
          label="Back"
          name="back"
          inputStyle="w-1/1"
          labelStyle="font-semibold block mb-2"
          register={register}
          error={errors.back}
        />
        <Button
          disabled={updateFlashcard.isPending}
          text="Update"
          textDisabled="Updating..."
          type="submit"
        />
      </form>
    </div>
  );
};
