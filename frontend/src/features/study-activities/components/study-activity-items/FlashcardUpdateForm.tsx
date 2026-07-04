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
    <div>
      {updateFlashcard.isError && <p>{updateFlashcard.error.message}</p>}
      {updateFlashcard.isPending && <p>Updating the flashcard, please wait.</p>}
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
        <Button
          disabled={updateFlashcard.isPending}
          text="Update"
          textDisabled="Updating"
        />
      </form>
    </div>
  );
};
