import { useLogin } from '@/features/auth/api/useLogin';
import { Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { type LoginInput, LoginInputSchema } from '@/features/auth/types/login';
import { zodResolver } from '@hookform/resolvers/zod';
import { FormField } from '@/components/FormField';
import { SubmitButton } from '@/components/SubmitButton';

export const LoginForm = () => {
  // Fetches states
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginInput>({
    resolver: zodResolver(LoginInputSchema),
    defaultValues: {
      username: '',
      password: '',
    },
  });

  const login = useLogin();

  // Logins
  const onSubmit = (data: LoginInput) => {
    login.mutate(data);
  };

  return (
    <div>
      <h2>Login</h2>

      {login.isError && <p>{login.error.message}</p>}
      {login.isPending && <p>Logging in, please wait</p>}

      <form onSubmit={handleSubmit(onSubmit)}>
        <FormField
          label="Email"
          name="username"
          register={register}
          error={errors.username}
        />

        <br />

        <FormField
          label="Password"
          name="password"
          register={register}
          error={errors.password}
        />

        <br />

        <SubmitButton
          disabled={login.isPending}
          text="Log in"
          textDisabled="Logging in..."
        />
      </form>

      <br />

      <Link to="/auth/register">Register an account</Link>
    </div>
  );
};
