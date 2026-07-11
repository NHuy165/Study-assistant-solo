import { Button } from '@/components/miscellaneous/Button';
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
    <li className="flex flex-col">
      <Button
        style="w-1/1"
        text={`Assessment date: ${dayjs.utc(assessment.assessment_of).format('YYYY-MM-DD')}`}
        onClick={() => setShowContent(!showContent)}
      />
      {/* Properly displays dummy assessments without content */}

      {showContent && (
        <span className="block mt-3 p-6 border border-primary overflow-y-auto min-h-30 max-h-60 whitespace-pre-wrap break-words">
          <h3 className="font-bold text-3xl mb-5">
            Assessment of{' '}
            {`${dayjs.utc(assessment.assessment_of).format('YYYY-MM-DD')}`}
          </h3>
          {assessment.content || 'Study assessment in progress...'}
        </span>
      )}
    </li>
  );
};
