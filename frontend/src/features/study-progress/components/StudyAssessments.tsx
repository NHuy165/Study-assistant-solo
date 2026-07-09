import { FormField } from '@/components/form-elements/FormField';
import { Button } from '@/components/miscellaneous/Button';
import { useCreateStudyAssessment } from '@/features/study-progress/api/study-assessment/useCreateStudyAssessment';
import { useGetStudyAssessments } from '@/features/study-progress/api/study-assessment/useGetStudyAssessments';
import { StudyAssessmentItem } from '@/features/study-progress/components/StudyAssessmentItem';
import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc';
import { useEffect } from 'react';
import { useForm, useWatch } from 'react-hook-form';

dayjs.extend(utc);

export const StudyAssessments = () => {
  const getStudyAssessments = useGetStudyAssessments();
  const createStudyAssessment = useCreateStudyAssessment();
  const { mutate } = useCreateStudyAssessment();
  const yesterday = dayjs.utc().subtract(1, 'day').format('YYYY-MM-DD');

  useEffect(() => {
    mutate();
  }, [mutate]);

  const { register, control, setValue } = useForm<{ date: string }>({
    defaultValues: { date: '' },
  });

  const searchDate = useWatch({ control, name: 'date' });

  const yesterdayAssessment = getStudyAssessments.data?.find(
    (assessment) =>
      dayjs.utc(assessment.assessment_of).format('YYYY-MM-DD') === yesterday,
  );

  const filteredStudyAssessment = getStudyAssessments.data?.filter(
    (assessment) => !searchDate || assessment.assessment_of === searchDate,
  );

  return (
    <div>
      {getStudyAssessments.isPending && <p>'Fetching data...'</p>}
      {getStudyAssessments.isError && <p>'Failed to fetch data.'</p>}
      {createStudyAssessment.isPending && (
        <p>'Study assessment in progress...'</p>
      )}
      {createStudyAssessment.isError && (
        <p>'Failed to generate study assessment'</p>
      )}

      {getStudyAssessments.isPending ||
        getStudyAssessments.isError ||
        createStudyAssessment.isPending ||
        createStudyAssessment.isError || (
          <div>
            {/* Yesterday assessment */}
            <div className="mb-6">
              <h3 className="font-bold">Yesterday's assessment:</h3>
              {/* Properly displays dummy assessments without content */}
              <span>
                {yesterdayAssessment
                  ? yesterdayAssessment.content ||
                    'Study assessment in progress...'
                  : "User didn't log in yesterday."}
              </span>
            </div>

            {/* Assessments history */}
            <div>
              <h3 className="font-bold">Study assessments history:</h3>
              <div className="flex mt-3 h-12">
                <FormField
                  label=""
                  name="date"
                  wrapperStyle="w-1/4 mr-3"
                  inputStyle=""
                  register={register}
                  type="date"
                />
                <Button
                  text="All"
                  style="w-1/8"
                  onClick={() => setValue('date', '')}
                />
              </div>

              {filteredStudyAssessment && filteredStudyAssessment.length > 0 ? (
                <ul className="space-y-3 mt-3">
                  {filteredStudyAssessment.map((assessment) => (
                    <StudyAssessmentItem
                      key={assessment.assessment_of}
                      assessment={assessment}
                    />
                  ))}
                </ul>
              ) : (
                <span>No study assessment found.</span>
              )}
            </div>
          </div>
        )}
    </div>
  );
};
