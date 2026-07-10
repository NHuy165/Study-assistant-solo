import { FormField } from '@/components/form-elements/FormField';
import { SelectField } from '@/components/form-elements/SelectField';
import { Button } from '@/components/miscellaneous/Button';
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
    <div className="card shadow-xl border py-6 px-10 mx-10 mb-6">
      <h3 className="font-bold text-2xl mb-3">
        Create a new blank flashcard activity.
      </h3>

      <form className="flex flex-col" onSubmit={handleSubmit(onSubmit)}>
        {/* Name */}
        <FormField
          label="Name"
          name="name"
          inputStyle="w-full"
          labelStyle="font-semibold block mb-2"
          register={register}
          error={errors.name}
        />

        {/* Description */}
        <FormField
          label="Description"
          name="description"
          inputStyle="w-full"
          labelStyle="font-semibold block mb-2"
          register={register}
          error={errors.description}
        />

        {/* Subject type */}
        <SelectField
          label="Subject type"
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
          disabled={createFlashcardsActivity.isPending}
          style="mt-6"
          text="Create"
          textDisabled="Creating..."
          type="submit"
        />
      </form>
    </div>
  );
};
