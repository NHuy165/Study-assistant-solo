import { FormField } from '@/components/form-elements/FormField';
import { SelectField } from '@/components/form-elements/SelectField';
import { SubmitButton } from '@/components/form-elements/SubmitButton';
import { useCreateStudyActivity } from '@/features/study-activities/api/useCreateStudyActivity';
import {
  type StudyActivityInput,
  StudyActivityInputSchema,
} from '@/features/study-activities/types/study-activity';
import { StudyActivityFormat, SubjectType } from '@/types/constants';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm, type SubmitHandler } from 'react-hook-form';

export const StudyActivityCreateForm = ({
  interactionId,
}: {
  interactionId: number;
}) => {
  const createStudyActivity = useCreateStudyActivity();

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<StudyActivityInput>({
    resolver: zodResolver(StudyActivityInputSchema),
    defaultValues: {
      prompt: '',
      activity_format: StudyActivityFormat.MultipleChoiceQuestions,
      subject_type: SubjectType.Maths,
      document_id: null,
    },
  });

  const onSubmit: SubmitHandler<StudyActivityInput> = (data) => {
    createStudyActivity.mutate(
      { interactionId, studyActivityInput: data },
      { onSuccess: () => reset() },
    );
  };

  return (
    <div>
      {createStudyActivity.isError && (
        <p>{createStudyActivity.error.message}</p>
      )}
      {createStudyActivity.isPending && (
        <p>Creating study activity, please wait.</p>
      )}

      <form onSubmit={handleSubmit(onSubmit)}>
        {/* Prompt */}
        <FormField
          label="Prompt"
          name="prompt"
          register={register}
          error={errors.prompt}
        />

        <br />

        {/* Activity Format */}
        <SelectField
          label="Activity format"
          name="activity_format"
          options={Object.entries(StudyActivityFormat).map(([label, value]) => {
            return { label, value };
          })}
          register={register}
          error={errors.activity_format}
        />

        <br />

        {/* Subject Type */}
        <SelectField
          label="Subject Type"
          name="subject_type"
          options={Object.entries(SubjectType).map(([label, value]) => {
            return { label, value };
          })}
          register={register}
          error={errors.subject_type}
        />

        <br />

        <SubmitButton
          disabled={createStudyActivity.isPending}
          text="Create"
          textDisabled="Creating..."
        />
      </form>
    </div>
  );
};
