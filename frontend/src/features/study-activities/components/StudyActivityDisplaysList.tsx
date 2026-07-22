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
      <h2 className="font-bold text-4xl mb-6">Study activities list:</h2>

      {getStudyActivities.isError && <p>Failed to fetch data.</p>}
      {getStudyActivities.isPending && <p>Fetching data...</p>}

      {getStudyActivities.isPending ||
        getStudyActivities.isError ||
        (getStudyActivities.data.length > 0 ? (
          <ul className="space-y-3">
            {getStudyActivities.data?.map((studyActivity) => (
              <StudyActivityDisplayItem
                key={studyActivity.id}
                studyActivity={studyActivity}
              />
            ))}
          </ul>
        ) : (
          <span>User has no study activity.</span>
        ))}
    </div>
  );
};
