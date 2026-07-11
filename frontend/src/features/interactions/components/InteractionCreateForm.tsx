import { FormField } from '@/components/form-elements/FormField';
import { TextArea } from '@/components/form-elements/TextArea';
import { Button } from '@/components/miscellaneous/Button';
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
    reset,
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
    createInteraction.mutate(data, { onSuccess: () => reset() });
  };

  return (
    <div className="card shadow-xl border border border-primary py-6 px-10 mx-10 mb-6">
      <h3 className="font-bold text-2xl mb-3">Create an interaction</h3>

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
        <TextArea
          label="Description"
          name="description"
          inputStyle="w-full"
          labelStyle="font-semibold block mb-2"
          register={register}
          error={errors.description}
        />

        {/* Submit button */}
        <Button
          disabled={createInteraction.isPending}
          style="mt-6"
          text="Create"
          textDisabled="Creating..."
          type="submit"
        />
      </form>
    </div>
  );
};
