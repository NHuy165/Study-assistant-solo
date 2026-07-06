import { FormField } from '@/components/form-elements/FormField';
import { Button } from '@/components/miscellaneous/Button';
import { TextArea } from '@/components/form-elements/TextArea';
import { useRegister } from '@/features/auth/api/useRegister';
import {
  type RegisterInput,
  RegisterInputSchema,
} from '@/features/auth/types/register';
import { zodResolver } from '@hookform/resolvers/zod';
import { type SubmitHandler, useForm } from 'react-hook-form';
import { Link } from 'react-router-dom';

export const RegisterForm = () => {
  // Fetches state
  const registerUser = useRegister();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterInput>({
    resolver: zodResolver(RegisterInputSchema),
    defaultValues: {
      username: '',
      email: '',
      password: '',
      description: '',
    },
  });

  // Registers
  const onSubmit: SubmitHandler<RegisterInput> = (data) => {
    registerUser.mutate(data);
  };

  return (
    <div className="flex flex-col">
      <h2 className="text-2xl font-bold text-center">Register</h2>

      <form onSubmit={handleSubmit(onSubmit)}>
        {/* Username */}
        <FormField
          label="Username"
          name="username"
          labelStyle="font-semibold block mb-2"
          register={register}
          error={errors.username}
        />

        {/* Email */}
        <FormField
          label="Email"
          name="email"
          labelStyle="font-semibold block mb-2"
          register={register}
          error={errors.email}
        />

        {/* Password */}
        <FormField
          label="Password"
          name="password"
          labelStyle="font-semibold block mb-2"
          register={register}
          error={errors.password}
        />

        {/* Description */}
        <TextArea
          label="Description"
          name="description"
          labelStyle="font-semibold block mb-2"
          register={register}
          placeholder="Tell us a few things about yourself (academic background, achievements...)"
          error={errors.description}
        />

        {/* Submit button */}
        <Button
          text="Register"
          textDisabled="Registering..."
          style="w-full my-6"
          disabled={registerUser.isPending}
          type="submit"
        />
      </form>

      <div className="link link-primary link-hover">
        <Link to="/auth/login">Log into an account</Link>
      </div>
    </div>
  );
};
