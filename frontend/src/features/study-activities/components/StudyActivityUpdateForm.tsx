import { FormField } from '@/components/form-elements/FormField';
import { TextArea } from '@/components/form-elements/TextArea';
import { Button } from '@/components/miscellaneous/Button';
import { useUpdateStudyActivity } from '@/features/study-activities/api/useUpdateStudyActivity';
import {
  StudyActivityUpdateSchema,
  type StudyActivityOutput,
  type StudyActivityUpdate,
} from '@/features/study-activities/types/study-activity';
import { zodResolver } from '@hookform/resolvers/zod';
import { type SubmitHandler, useForm } from 'react-hook-form';

export const StudyActivityUpdateForm = ({
  studyActivity,
  onUpdate,
}: {
  studyActivity: StudyActivityOutput;
  onUpdate: () => void;
}) => {
  // Fetches states
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<StudyActivityUpdate>({
    resolver: zodResolver(StudyActivityUpdateSchema),
    values: {
      name: studyActivity.name,
      description: studyActivity.description,
    },
  });

  const updateStudyActivity = useUpdateStudyActivity();

  // Updates function
  const onSubmit: SubmitHandler<StudyActivityUpdate> = (data) => {
    updateStudyActivity.mutate(
      {
        studyActivityId: studyActivity.id,
        studyActivityUpdate: data,
      },
      { onSuccess: () => onUpdate() },
    );
  };

  return (
    <form
      className="card shadow-xl border border border-primary mt-3 mb-6 p-6"
      onSubmit={handleSubmit(onSubmit)}
    >
      <h3 className="font-bold text-3xl mb-3">Update</h3>

      {/* Name */}
      <FormField
        label="New name"
        name="name"
        inputStyle="w-1/1"
        labelStyle="font-semibold block mb-2"
        register={register}
        error={errors.name}
      />

      {/* Description */}
      <TextArea
        label="New description"
        name="description"
        inputStyle="w-1/1"
        labelStyle="font-semibold block mb-2"
        register={register}
        error={errors.description}
      />

      {/* Submit button */}
      <Button
        disabled={updateStudyActivity.isPending}
        style="mt-3"
        text="Update"
        textDisabled="Updating..."
        type="submit"
      />
    </form>
  );
};
