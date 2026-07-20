import { FormField } from '@/components/form-elements/FormField';
import { TextArea } from '@/components/form-elements/TextArea';
import { Button } from '@/components/miscellaneous/Button';
import { useGetUser } from '@/features/user/api/useGetUser';
import { useUpdateUser } from '@/features/user/api/useUpdateUser';
import {
  UserUpdateSchema,
  type UserOutput,
  type UserUpdate,
} from '@/features/user/types/user';
import { zodResolver } from '@hookform/resolvers/zod';
import { type SubmitHandler, useForm } from 'react-hook-form';

export const UserFieldUpdateForm = ({
  label,
  field,
  onUpdate,
}: {
  label: string;
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
    values: data, // Fine since this form will only show when user data has been fetched
  });

  const updateUser = useUpdateUser();

  const onSubmit: SubmitHandler<UserUpdate> = (data) => {
    updateUser.mutate(data, { onSuccess: () => onUpdate() });
  };

  return (
    <form
      className="card shadow-xl border border-primary mt-3 mb-6 p-6"
      onSubmit={handleSubmit(onSubmit)}
    >
      {field === 'description' ? (
        <TextArea
          label={label}
          name={field}
          wrapperStyle="w-full"
          labelStyle="font-semibold block mb-2"
          inputStyle="w-full"
          register={register}
          placeholder="Tell us a few things about yourself (academic background, achievements...)"
          error={errors.description}
        />
      ) : (
        <FormField
          label={label}
          name={field}
          wrapperStyle="w-full"
          labelStyle="font-semibold block mb-2"
          inputStyle="w-full"
          register={register}
          error={errors[field]}
        />
      )}

      <Button
        disabled={updateUser.isPending}
        text="Confirm"
        textDisabled="Updating..."
        type="submit"
      />
    </form>
  );
};
