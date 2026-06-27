import { FormField } from '@/components/FormField';
import { SubmitButton } from '@/components/SubmitButton';
import { useCreateInteraction } from '@/features/interactions/api/useCreateInteraction';
import {
  type InteractionInput,
  InteractionInputSchema,
} from '@/features/interactions/types/interaction';
import { zodResolver } from '@hookform/resolvers/zod';
import { type SubmitHandler, useForm } from 'react-hook-form';

export const InteractionCreateForm = () => {
  // Fetches states
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<InteractionInput>({
    resolver: zodResolver(InteractionInputSchema),
    defaultValues: {
      name: '',
      description: '',
    },
  });

  const createInteraction = useCreateInteraction();

  const onSubmit: SubmitHandler<InteractionInput> = (data) => {
    createInteraction.mutate(data);
  };

  return (
    <div>
      {createInteraction.isError && <p>{createInteraction.error.message}</p>}
      {createInteraction.isPending && <p>Creating interaction, please wait.</p>}

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

        {/* Submit button */}
        <SubmitButton
          disabled={createInteraction.isPending}
          text="Create"
          textDisabled="Creating..."
        />
      </form>
    </div>
  );
};
