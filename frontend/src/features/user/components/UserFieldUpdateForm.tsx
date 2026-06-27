import { FormField } from '@/components/FormField';
import { SubmitButton } from '@/components/SubmitButton';
import { useGetUser } from '@/features/user/api/useGetUser';
import { useUpdateUser } from '@/features/user/api/useUpdateUser';
import {
  UserUpdateSchema,
  type UserOutput,
  type UserUpdate,
} from '@/features/user/types/user';
import { replaceUnderscore } from '@/utils/format-string';
import { zodResolver } from '@hookform/resolvers/zod';
import { type SubmitHandler, useForm } from 'react-hook-form';

export const UserFieldUpdateForm = ({
  field,
  onUpdate,
}: {
  field: keyof UserOutput & keyof UserUpdate;
  onUpdate: () => void;
}) => {
  const getUser = useGetUser();
  const data = getUser.data;

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<UserUpdate>({
    resolver: zodResolver(UserUpdateSchema),
    values: data,
  });

  const updateUser = useUpdateUser();

  const onSubmit: SubmitHandler<UserUpdate> = (data) => {
    updateUser.mutate(data, { onSuccess: () => onUpdate() });
  };

  return (
    <div>
      {updateUser.isError && updateUser.error.message}
      {updateUser.isPending && 'Updating field, please wait.'}
      <form onSubmit={handleSubmit(onSubmit)}>
        <FormField
          label={`New ${replaceUnderscore(field.toLowerCase())}`}
          name={field}
          register={register}
          error={errors[field]}
        />

        <SubmitButton
          disabled={updateUser.isPending}
          text="Confirm"
          textDisabled="Updating field..."
        />
      </form>
    </div>
  );
};
