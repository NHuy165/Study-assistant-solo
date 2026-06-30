import { FormField } from '@/components/form-elements';
import { SubmitButton } from '@/components/SubmitButton';
import { useChangePassword } from '@/features/user/api/useChangePassword';
import {
  type UserPasswordChange,
  UserPasswordChangeSchema,
} from '@/features/user/types/user';
import { zodResolver } from '@hookform/resolvers/zod';
import { useState } from 'react';
import { type SubmitHandler, useForm } from 'react-hook-form';

export const UserPasswordChangeForm = () => {
  const [showUpdateForm, setShowUpdateForm] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<UserPasswordChange>({
    resolver: zodResolver(UserPasswordChangeSchema),
    defaultValues: { old_password: '', new_password: '' },
  });

  const changePassword = useChangePassword();

  const onSubmit: SubmitHandler<UserPasswordChange> = (data) => {
    changePassword.mutate(data, { onSuccess: () => setShowUpdateForm(false) });
  };

  return (
    <div>
      Change password:
      <button onClick={() => setShowUpdateForm(!showUpdateForm)}>Show</button>
      <br />
      {showUpdateForm && (
        <>
          {changePassword.isError && changePassword.error.message}
          {changePassword.isPending && 'Updating field, please wait.'}
          <form onSubmit={handleSubmit(onSubmit)}>
            <FormField
              label="Old password"
              name="old_password"
              register={register}
              error={errors.old_password}
            />

            <FormField
              label="New password"
              name="new_password"
              register={register}
              error={errors.new_password}
            />

            <SubmitButton
              disabled={changePassword.isPending}
              text="Confirm"
              textDisabled="Updating field..."
            />
          </form>
        </>
      )}
    </div>
  );
};
