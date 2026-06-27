import { FormField } from '@/components/FormField';
import { SubmitButton } from '@/components/SubmitButton';
import { useUpdateInteraction } from '@/features/interactions/api/useUpdateInteraction';
import {
  type InteractionUpdate,
  type InteractionOutput,
  InteractionUpdateSchema,
} from '@/features/interactions/types/interaction';
import { zodResolver } from '@hookform/resolvers/zod';
import { type SubmitHandler, useForm } from 'react-hook-form';

export const InteractionUpdateForm = ({
  interaction,
  onUpdate,
}: {
  interaction: InteractionOutput;
  onUpdate: () => void;
}) => {
  // Fetches states
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<InteractionUpdate>({
    resolver: zodResolver(InteractionUpdateSchema),
    values: {
      name: interaction.name,
      description: interaction.description,
    },
  });

  const updateInteraction = useUpdateInteraction();

  // Updates function
  const onSubmit: SubmitHandler<InteractionUpdate> = (data) => {
    updateInteraction.mutate(
      {
        id: interaction.id,
        interactionUpdate: data,
      },
      { onSuccess: () => onUpdate() },
    );
  };

  return (
    <div>
      {updateInteraction.isError && <p>{updateInteraction.error.message}</p>}
      {updateInteraction.isPending && (
        <p>Updating the interaction, please wait.</p>
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

        {/* Submit button */}
        <SubmitButton
          disabled={updateInteraction.isPending}
          text="Update"
          textDisabled="Updating..."
        />
      </form>
    </div>
  );
};
