import { useGetStudyActivities } from '@/features/study-activities/api/useGetStudyActivities';
import { StudyActivityDisplayItem } from '@/features/study-activities/components/StudyActivityDisplayItem';

export const StudyActivityDisplaysList = ({
  interactionId,
}: {
  interactionId: number;
}) => {
  const getStudyActivities = useGetStudyActivities(interactionId);

  return (
    <div>
      {getStudyActivities.isError && <p>{getStudyActivities.error.message}</p>}
      {getStudyActivities.isPending && (
        <p>Fetching study activities, please wait.</p>
      )}

      <ul>
        {getStudyActivities.data?.map((studyActivity) => (
          <StudyActivityDisplayItem
            key={studyActivity.id}
            studyActivity={studyActivity}
          />
        ))}
      </ul>
    </div>
  );
};
