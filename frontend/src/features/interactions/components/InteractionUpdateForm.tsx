import { FormField } from '@/components/form-elements/FormField';
import { TextArea } from '@/components/form-elements/TextArea';
import { Button } from '@/components/miscellaneous/Button';
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
        disabled={updateInteraction.isPending}
        style="mt-3"
        text="Update"
        textDisabled="Updating..."
        type="submit"
      />
    </form>
  );
};
