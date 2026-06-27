import { FormField } from '@/components/FormField';
import { SubmitButton } from '@/components/SubmitButton';
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
    <div>
      <h2>Register</h2>

      {registerUser.isError && <p>{registerUser.error.message}</p>}
      {registerUser.isPending && <p>Registering user, please wait</p>}

      <form onSubmit={handleSubmit(onSubmit)}>
        {/* Username */}
        <FormField
          label="Username"
          name="username"
          register={register}
          error={errors.username}
        />

        <br />

        {/* Email */}
        <FormField
          label="Email"
          name="email"
          register={register}
          error={errors.email}
        />

        <br />

        {/* Password */}
        <FormField
          label="Password"
          name="password"
          register={register}
          error={errors.password}
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
          disabled={registerUser.isPending}
          text="Register"
          textDisabled="Registering..."
        />
      </form>

      <br />

      <Link to="/auth/login">Log into an account</Link>
    </div>
  );
};
