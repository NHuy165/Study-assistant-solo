import { StudyActivityWorkspace } from '@/features/study-activities/components/StudyActivityWorkspace';
import { useParams } from 'react-router-dom';

export const StudyActivityPage = () => {
  const { studyActivityId } = useParams();

  return <StudyActivityWorkspace studyActivityId={Number(studyActivityId)} />;
};
