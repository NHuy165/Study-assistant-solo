import type { StudyAssessmentOutput } from '@/features/study-progress/types/study-assessment';
import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc';
import { useState } from 'react';

dayjs.extend(utc);

export const StudyAssessmentItem = ({
  assessment,
}: {
  assessment: StudyAssessmentOutput;
}) => {
  const [showContent, setShowContent] = useState(false);

  return (
    <li>
      Assessment date:{' '}
      {dayjs.utc(assessment.assessment_of).format('YYYY-MM-DD')}
      <button onClick={() => setShowContent(!showContent)}>Show content</button>
      <br />
      {/* Properly displays dummy assessments without content */}
      {showContent &&
        (assessment.content || 'Generating study assessment, please wait.')}
    </li>
  );
};
