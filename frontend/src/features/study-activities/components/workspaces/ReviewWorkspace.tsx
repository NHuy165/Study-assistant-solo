import { FlashcardItem } from '@/features/study-activities/components/study-activity-items/FlashcardItem';
import { FlashcardsCreateForm } from '@/features/study-activities/components/workspaces/FlashcardsCreateForm';
import type { StudyActivityOutputComplete } from '@/features/study-activities/types/study-activity';

export const ReviewWorkspace = ({
  studyActivity,
}: {
  studyActivity: StudyActivityOutputComplete;
}) => {
  return (
    <div>
      {/* Change this if there are more review-type activities in the future. */}

      <FlashcardItem studyActivity={studyActivity} />

      <FlashcardsCreateForm reviewActivityId={studyActivity.id} />
    </div>
  );
};
