import { useGetStudyActivityComplete } from '@/features/study-activities/api/useGetStudyActivityComplete';
import { ExerciseWorkspace } from '@/features/study-activities/components/workspaces/ExerciseWorkspace';
import { ReviewWorkspace } from '@/features/study-activities/components/workspaces/ReviewWorkspace';
import { StudyActivityType } from '@/types/constants';
import { replaceUnderscore, titleString } from '@/utils/format-string';
import { Link } from 'react-router-dom';

export const StudyActivityWorkspace = ({
  studyActivityId,
}: {
  studyActivityId: number;
}) => {
  const getStudyActivityComplete = useGetStudyActivityComplete(studyActivityId);
  const studyActivity = getStudyActivityComplete.data;

  return (
    <div>
      <Link
        className="link link-primary link-hover"
        to={`/interaction/${studyActivity?.interaction_id}`}
      >
        Back to main interaction
      </Link>

      {getStudyActivityComplete.isError && <p>Failed to fetch data.</p>}
      {getStudyActivityComplete.isPending && <p>Fetching data...</p>}

      {getStudyActivityComplete.isError ||
        getStudyActivityComplete.isPending || (
          <div>
            {/* Title */}
            {studyActivity && (
              <div className="space-y-8 mt-6">
                <h1 className="text-4xl font-bold text-center">
                  {studyActivity?.name}
                </h1>
                <p className="px-6">
                  <span className="block font-bold text-xl mb-3">
                    Description:{' '}
                  </span>
                  <span className="block max-h-30 overflow-y-auto break-words whitespace-pre-wrap border border-primary p-3">
                    {studyActivity?.description}
                  </span>
                </p>
              </div>
            )}

            <span className="divider divider-primary"></span>

            {studyActivity?.activity_type === StudyActivityType.Exercise ? (
              <ExerciseWorkspace studyActivity={studyActivity} />
            ) : (
              <ReviewWorkspace studyActivity={studyActivity} />
            )}
          </div>
        )}
    </div>
  );
};
