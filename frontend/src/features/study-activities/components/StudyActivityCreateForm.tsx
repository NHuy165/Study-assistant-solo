import { SelectField } from '@/components/form-elements/SelectField';
import { TextArea } from '@/components/form-elements/TextArea';
import { Button } from '@/components/miscellaneous/Button';
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
    <div className="card shadow-xl border border border-primary py-6 px-10 mx-10 mb-6">
      <h3 className="font-bold text-2xl mb-3">Create a study activity</h3>

      <form className="flex flex-col" onSubmit={handleSubmit(onSubmit)}>
        {/* Prompt */}
        <TextArea
          label="Prompt"
          name="prompt"
          inputStyle="w-full"
          labelStyle="font-semibold block mb-2"
          register={register}
          error={errors.prompt}
        />

        {/* Activity Format */}
        <SelectField
          label="Activity format"
          name="activity_format"
          inputStyle="w-full"
          labelStyle="font-semibold block mb-2"
          options={Object.entries(StudyActivityFormat).map(([label, value]) => {
            return { label, value };
          })}
          register={register}
          error={errors.activity_format}
        />

        {/* Subject Type */}
        <SelectField
          label="Subject Type"
          name="subject_type"
          inputStyle="w-full"
          labelStyle="font-semibold block mb-2"
          options={Object.entries(SubjectType).map(([label, value]) => {
            return { label, value };
          })}
          register={register}
          error={errors.subject_type}
        />

        <Button
          disabled={createStudyActivity.isPending}
          style="mt-6"
          text="Create"
          textDisabled="Creating..."
          type="submit"
        />
      </form>
    </div>
  );
};
