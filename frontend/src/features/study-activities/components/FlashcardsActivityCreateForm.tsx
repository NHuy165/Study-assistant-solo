import { FormField, SelectField } from '@/components/form-elements';
import { SubmitButton } from '@/components/SubmitButton';
import { useCreateFlashcardsActivity } from '@/features/study-activities/api/useCreateFlashcardsActivity';
import {
  type FlashcardsActivityInput,
  FlashcardsActivityInputSchema,
} from '@/features/study-activities/types/study-activity';
import { SubjectType } from '@/types/constants';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm, type SubmitHandler } from 'react-hook-form';

export const FlashcardsActivityCreateForm = ({
  interactionId,
}: {
  interactionId: number;
}) => {
  const createFlashcardsActivity = useCreateFlashcardsActivity();

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<FlashcardsActivityInput>({
    resolver: zodResolver(FlashcardsActivityInputSchema),
    defaultValues: {
      name: '',
      description: '',
      subject_type: SubjectType.Maths,
    },
  });

  const onSubmit: SubmitHandler<FlashcardsActivityInput> = (data) => {
    createFlashcardsActivity.mutate(
      {
        interactionId,
        flashcardsActivityInput: data,
      },
      { onSuccess: () => reset() },
    );
  };

  return (
    <div>
      {createFlashcardsActivity.isError && (
        <p>{createFlashcardsActivity.error.message}</p>
      )}
      {createFlashcardsActivity.isPending && (
        <p>Creating study activity, please wait.</p>
      )}

      <form onSubmit={handleSubmit(onSubmit)}>
        {/* Name */}
        <FormField
          label="Name"
          name="name"
          register={register}
          error={errors.name}
        />

        <br />

        {/* Description */}
        <FormField
          label="Description"
          name="description"
          register={register}
          error={errors.description}
        />

        <br />

        {/* Subject type */}
        <SelectField
          label="Subject type"
          name="subject_type"
          options={Object.entries(SubjectType).map(([label, value]) => {
            return { label, value };
          })}
          register={register}
          error={errors.subject_type}
        />

        <br />

        <SubmitButton
          disabled={createFlashcardsActivity.isPending}
          text="Create"
          textDisabled="Creating..."
        />
      </form>
    </div>
  );
};
