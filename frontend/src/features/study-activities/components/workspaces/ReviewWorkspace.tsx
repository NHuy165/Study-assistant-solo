import { FlashcardItem } from '@/features/study-activities/components/study-activity-items/FlashcardItem';
import { FlashcardsCreateForm } from '@/features/study-activities/components/workspaces/FlashcardsCreateForm';
import type {
  ReviewItemOutput,
  StudyActivityOutputComplete,
} from '@/features/study-activities/types/study-activity';
import { StudyActivityFormat } from '@/types/constants';

export const ReviewWorkspace = ({
  studyActivity,
}: {
  studyActivity: StudyActivityOutputComplete;
}) => {
  return (
    <div>
      {/* Change this if there are more review-type activities in the future. */}
      <FlashcardsCreateForm reviewActivityId={studyActivity.id} />

      {studyActivity.items.map((reviewItem) => {
        switch (studyActivity.activity_format) {
          case StudyActivityFormat.Flashcards:
            return (
              <FlashcardItem
                key={reviewItem.id}
                reviewItem={reviewItem as ReviewItemOutput}
              />
            );
        }
      })}
    </div>
  );
};
