import { FlashcardItem } from '@/features/study-activities/components/study-activity-items/FlashcardItem';
import { FlashcardsCreateForm } from '@/features/study-activities/components/workspaces/FlashcardsCreateForm';
import type { StudyActivityOutputComplete } from '@/features/study-activities/types/study-activity';
import { replaceUnderscore, titleString } from '@/utils/format-string';

export const ReviewWorkspace = ({
  studyActivity,
}: {
  studyActivity: StudyActivityOutputComplete;
}) => {
  return (
    <section>
      {/* Change this if there are more review-type activities in the future. */}
      <h2 className="font-bold text-4xl text-center mb-6">
        {titleString(replaceUnderscore(studyActivity.activity_format))}
      </h2>

      <FlashcardItem studyActivity={studyActivity} />

      <FlashcardsCreateForm reviewActivityId={studyActivity.id} />
    </section>
  );
};
