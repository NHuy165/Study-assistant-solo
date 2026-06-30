import { useDeleteFlashcard } from '@/features/study-activities/api/useDeleteFlashcard';
import { FlashcardUpdateForm } from '@/features/study-activities/components/study-activity-items/FlashcardUpdateForm';
import { type ReviewItemOutput } from '@/features/study-activities/types/study-activity';
import { ReviewItemContentType } from '@/types/constants';
import { useState } from 'react';

export const FlashcardItem = ({
  reviewItem,
}: {
  reviewItem: ReviewItemOutput;
}) => {
  // Fetches states
  const [showBack, setShowBack] = useState(false);
  const [showUpdateForm, setShowUpdateForm] = useState(false);
  const deleteFlashcard = useDeleteFlashcard();

  const frontContent = reviewItem.contents.find(
    (reviewItemContent) =>
      reviewItemContent.type === ReviewItemContentType.FlashcardFront,
  )?.content as string;
  const backContent = reviewItem.contents.find(
    (reviewItemContent) =>
      reviewItemContent.type === ReviewItemContentType.FlashcardBack,
  )?.content as string;

  return (
    <div>
      Current side:
      <button onClick={() => setShowBack(!showBack)}>
        {showBack ? 'Back' : 'Front'}
      </button>
      <br />
      Content: {showBack ? backContent : frontContent}
      <br />
      <button onClick={() => setShowUpdateForm(!showUpdateForm)}>
        Show update
      </button>
      <button onClick={() => deleteFlashcard.mutate(reviewItem.id)}>
        Delete
      </button>
      {showUpdateForm && (
        <FlashcardUpdateForm
          reviewItem={reviewItem}
          onUpdate={() => setShowUpdateForm(false)}
        />
      )}
    </div>
  );
};
