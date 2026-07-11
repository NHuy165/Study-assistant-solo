import { FormField } from '@/components/form-elements/FormField';
import { Button } from '@/components/miscellaneous/Button';
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
      <Button
        text="Change password"
        onClick={() => setShowUpdateForm(!showUpdateForm)}
        style="w-full mt-6"
      />
      {showUpdateForm && (
        <div className="card shadow-xl border border-primary mt-6 p-6">
          {changePassword.isError && changePassword.error.message}
          {changePassword.isPending && 'Updating field, please wait.'}
          <form onSubmit={handleSubmit(onSubmit)}>
            <FormField
              label="Old password"
              name="old_password"
              labelStyle="font-semibold block mb-2"
              register={register}
              error={errors.old_password}
            />

            <FormField
              label="New password"
              name="new_password"
              labelStyle="font-semibold block mb-2"
              register={register}
              error={errors.new_password}
            />

            <Button
              text="Confirm"
              textDisabled="Updating field..."
              disabled={changePassword.isPending}
            />
          </form>
        </div>
      )}
    </div>
  );
};
