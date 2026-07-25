import { Button } from '@/components/miscellaneous/Button';
import { useDeleteFlashcard } from '@/features/study-activities/api/useDeleteFlashcard';
import { FlashcardUpdateForm } from '@/features/study-activities/components/study-activity-items/FlashcardUpdateForm';
import {
  type ReviewItemOutput,
  type StudyActivityOutputComplete,
} from '@/features/study-activities/types/study-activity';
import { ReviewItemContentType } from '@/types/constants';
import { useState } from 'react';

export const FlashcardItem = ({
  studyActivity,
}: {
  studyActivity: StudyActivityOutputComplete;
}) => {
  // Fetches states
  const [showBack, setShowBack] = useState(false);
  const [showUpdateForm, setShowUpdateForm] = useState(false);
  const [currentIndex, setCurrentIndex] = useState(0);
  const deleteFlashcard = useDeleteFlashcard();

  const frontContent = studyActivity.items
    .at(currentIndex)
    ?.contents.find(
      (reviewItemContent) =>
        reviewItemContent.type === ReviewItemContentType.FlashcardFront,
    )?.content as string | undefined;
  const backContent = studyActivity.items
    .at(currentIndex)
    ?.contents.find(
      (reviewItemContent) =>
        reviewItemContent.type === ReviewItemContentType.FlashcardBack,
    )?.content as string | undefined;

  return (
    <>
      {studyActivity.items.length > 0 ? (
        <>
          <section>
            <span className="block mb-1 font-bold text-center">
              Current card index: {currentIndex + 1}/
              {studyActivity.items.length}
            </span>
            <div className="flex max-w-full">
              <Button
                text="Previous"
                style="h-100 w-1/6 rounded-none"
                textStyle="font-bold text-2xl"
                onClick={() => {
                  setCurrentIndex(currentIndex > 0 ? currentIndex - 1 : 0);
                  setShowBack(false);
                }}
                disabled={currentIndex === 0}
                textDisabled="Previous"
              />

              <Button
                text={
                  showBack ? (backContent as string) : (frontContent as string)
                }
                onClick={() => setShowBack(!showBack)}
                style={`block flex-1 h-100 mx-auto whitespace-pre-wrap overflow-y-auto break-words rounded-none ${showBack ? 'bg-red-300' : 'bg-green-300'}`}
                textStyle="block text-2xl"
              />

              <Button
                text="Next"
                style="h-100 w-1/6 rounded-none"
                textStyle="font-bold text-2xl"
                onClick={() => {
                  setCurrentIndex(
                    currentIndex < studyActivity.items.length - 1
                      ? currentIndex + 1
                      : studyActivity.items.length - 1,
                  );
                  setShowBack(false);
                }}
                disabled={currentIndex === studyActivity.items.length - 1}
                textDisabled="Next"
              />
            </div>
          </section>
          <section>
            <Button
              text="Update current flashcard"
              style="w-full mt-4"
              onClick={() => setShowUpdateForm(!showUpdateForm)}
            ></Button>

            {showUpdateForm && (
              <FlashcardUpdateForm
                reviewItem={
                  studyActivity.items[currentIndex] as ReviewItemOutput
                }
                onUpdate={() => setShowUpdateForm(false)}
              />
            )}
            <Button
              text="Delete current flashcard"
              textDisabled="Deleting..."
              style="w-full mt-2"
              btnError={true}
              disabled={deleteFlashcard.isPending}
              onClick={() =>
                deleteFlashcard.mutate(studyActivity.items[currentIndex].id, {
                  onSuccess: () => {
                    setShowUpdateForm(false);
                    if (currentIndex === studyActivity.items.length - 1) {
                      setCurrentIndex(
                        Math.max(studyActivity.items.length - 2, 0),
                      );
                    }
                  },
                })
              }
            />
          </section>
        </>
      ) : (
        <section className="flex justify-center items-center border border-primary w-2/3 h-100 mx-auto s rounded-none">
          <span className="font-bold text-3xl">No flashcard to show</span>
        </section>
      )}
    </>
  );
};
