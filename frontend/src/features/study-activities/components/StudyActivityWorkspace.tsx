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
      <Link to={`/interaction/${studyActivity?.interaction_id}`}>
        Back to interaction
      </Link>
      {getStudyActivityComplete.isError && (
        <p>{getStudyActivityComplete.error.message}</p>
      )}
      {getStudyActivityComplete.isPending && (
        <p>Fetching study activity, please wait.</p>
      )}

      {studyActivity && (
        <h1>
          {titleString(replaceUnderscore(studyActivity?.activity_format))}:{' '}
          {studyActivity.name}
        </h1>
      )}

      {studyActivity &&
        (studyActivity.activity_type === StudyActivityType.Exercise ? (
          <ExerciseWorkspace studyActivity={studyActivity} />
        ) : (
          <ReviewWorkspace studyActivity={studyActivity} />
        ))}
    </div>
  );
};
