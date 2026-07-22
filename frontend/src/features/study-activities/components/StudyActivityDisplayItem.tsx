import { Button } from '@/components/miscellaneous/Button';
import { useDeleteStudyActivity } from '@/features/study-activities/api/useDeleteStudyActivity';
import { StudyActivityUpdateForm } from '@/features/study-activities/components/StudyActivityUpdateForm';
import type { StudyActivityOutput } from '@/features/study-activities/types/study-activity';
import { StudyActivityType } from '@/types/constants';
import { capitalizeString, replaceUnderscore } from '@/utils/format-string';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export const StudyActivityDisplayItem = ({
  studyActivity,
}: {
  studyActivity: StudyActivityOutput;
}) => {
  const [showDetails, setShowDetails] = useState(false);
  const [showUpdateForm, setShowUpdateForm] = useState(false);
  const deleteStudyActivity = useDeleteStudyActivity();
  const navigate = useNavigate();

  return (
    <li>
      <div>
        {/* Main study activity */}
        <Button
          style="w-2/3"
          text={`#${studyActivity.id} ${studyActivity.name}`}
          onClick={() => navigate(`/study-activity/${studyActivity.id}`)}
        />
        {/* More details */}
        <Button
          style="w-1/9"
          text="Details"
          onClick={() => setShowDetails(!showDetails)}
        />
        {/* Show update form */}
        <Button
          style="w-1/9"
          text="Update"
          onClick={() => setShowUpdateForm(!showUpdateForm)}
        />
        {/* Delete */}
        <Button
          style="w-1/9"
          text="Delete"
          textDisabled="Deleting..."
          btnError={true}
          onClick={() => deleteStudyActivity.mutate(studyActivity.id)}
        />
      </div>

      {/* Details */}
      {showDetails && (
        <section className="card shadow-xl border mt-3 p-6">
          <h3 className="font-bold text-3xl mb-3">Details</h3>
          <div className="max-h-50 overflow-y-auto break-words whitespace-pre-wrap">
            <p>
              <span className="font-bold">Created at:</span>{' '}
              {studyActivity.created_at}
            </p>
            <p>
              <span className="font-bold">Description:</span>{' '}
              {studyActivity.description}
            </p>
            <p>
              <span className="font-bold">Subject type:</span>{' '}
              {capitalizeString(studyActivity.subject_type)}
            </p>
            <p>
              <span className="font-bold">Format type:</span>{' '}
              {capitalizeString(
                replaceUnderscore(studyActivity.activity_format),
              )}
            </p>
            <p>
              <span className="font-bold">Creation prompt:</span>{' '}
              {studyActivity.prompt || (
                <span className="text-error">
                  This activity has no creation prompt.
                </span>
              )}
            </p>
            {studyActivity.activity_type === StudyActivityType.Exercise && (
              <>
                <p>
                  <span className="font-bold">Submission status:</span>{' '}
                  {studyActivity.is_submitted ? 'Submitted' : 'Not submitted'}
                </p>
                <p>
                  <span className="font-bold">Submitted at:</span>{' '}
                  {studyActivity.submitted_at || '-'}
                </p>
              </>
            )}
          </div>
        </section>
      )}

      {/* Update form */}
      {showUpdateForm && (
        <StudyActivityUpdateForm
          studyActivity={studyActivity}
          onUpdate={() => setShowUpdateForm(false)}
        />
      )}
    </li>
  );
};
