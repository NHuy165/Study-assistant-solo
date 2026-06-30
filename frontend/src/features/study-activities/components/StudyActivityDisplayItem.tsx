import { useDeleteStudyActivity } from '@/features/study-activities/api/useDeleteStudyActivity';
import type { StudyActivityOutput } from '@/features/study-activities/types/study-activity';
import { capitalizeString } from '@/utils/format-string';
import { Link } from 'react-router-dom';

export const StudyActivityDisplayItem = ({
  studyActivity,
}: {
  studyActivity: StudyActivityOutput;
}) => {
  const deleteStudyActivity = useDeleteStudyActivity();
  return (
    <li>
      <>
        #{studyActivity.id} ({studyActivity.created_at}) {studyActivity.name}{' '}
        (Subject:{' '}
        {studyActivity.subject_type
          ? capitalizeString(studyActivity.subject_type)
          : 'Other'}
        ) (Material type: {studyActivity.activity_format}) (Activity type:{' '}
        {studyActivity.activity_type}):{' '}
      </>
      <Link to={`/study-activity/${studyActivity.id}`}> Enter</Link>
      <button onClick={() => deleteStudyActivity.mutate(studyActivity.id)}>
        Delete
      </button>
      <br />
      {deleteStudyActivity.isError && (
        <p>{deleteStudyActivity.error.message}</p>
      )}
      {deleteStudyActivity.isPending && (
        <p>Deleting study activity, please wait.</p>
      )}
      Description: {studyActivity.description}
    </li>
  );
};
