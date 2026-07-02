import { FormField } from '@/components/form-elements';
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

  const { register, control } = useForm<{ date: string }>({
    defaultValues: { date: dayjs.utc().format('YYYY-MM-DD') },
  });

  const searchDate = useWatch({ control, name: 'date' });

  const yesterdayAssessment = getStudyAssessments.data?.find(
    (assessment) =>
      dayjs.utc(assessment.assessment_of).format('YYYY-MM-DD') === yesterday,
  );

  const searchAssessment = getStudyAssessments.data?.find(
    (assessment) =>
      dayjs.utc(assessment.assessment_of).format('YYYY-MM-DD') === searchDate,
  );

  return (
    <div>
      {getStudyAssessments.isError && (
        <p>{getStudyAssessments.error.message}</p>
      )}
      {getStudyAssessments.isPending && (
        <p>Fetching study assessments, please wait.</p>
      )}

      {createStudyAssessment.isError && (
        <p>{createStudyAssessment.error.message}</p>
      )}
      {createStudyAssessment.isPending && (
        <p>Updating study assessments, please wait.</p>
      )}

      {!getStudyAssessments.isPending && !getStudyAssessments.isError && (
        <>
          <h3>Yesterday's assessment:</h3>
          {/* Properly displays dummy assessments without content */}
          {yesterdayAssessment
            ? yesterdayAssessment.content ||
              'Generating study assessment, please wait.'
            : "You didn't log in yesterday"}

          <h3>All study assessments:</h3>
          <ul>
            {getStudyAssessments.data.map((assessment) => (
              <StudyAssessmentItem
                key={assessment.assessment_of}
                assessment={assessment}
              />
            ))}
          </ul>

          <h3>Search assessment by date</h3>
          <FormField label="Date" name="date" register={register} type="date" />
          <br />
          {/* Properly displays dummy assessments without content */}
          {searchAssessment
            ? searchAssessment.content ||
              'Generating study assessment, please wait'
            : 'No study assessment found on this date'}
        </>
      )}
    </div>
  );
};
