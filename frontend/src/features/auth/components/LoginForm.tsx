import { useLogin } from '@/features/auth/api/useLogin';
import { Link } from 'react-router-dom';
import { useForm, type SubmitHandler } from 'react-hook-form';
import { type LoginInput, LoginInputSchema } from '@/features/auth/types/login';
import { zodResolver } from '@hookform/resolvers/zod';
import { Button } from '@/components/miscellaneous/Button';
import { FormField } from '@/components/form-elements/FormField';

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
  const onSubmit: SubmitHandler<LoginInput> = (data) => {
    login.mutate(data);
  };

  return (
    <div className="flex flex-col">
      <h2 className="text-2xl font-bold text-center">Login</h2>

      <form onSubmit={handleSubmit(onSubmit)}>
        <FormField
          label="Email:"
          name="username"
          register={register}
          error={errors.username}
        />

        <FormField
          label="Password:"
          name="password"
          register={register}
          error={errors.password}
        />

        <Button
          text="Log in"
          textDisabled="Logging in..."
          style="w-full my-6"
          disabled={login.isPending}
          type="submit"
        />
      </form>

      <div className="link link-primary link-hover">
        <Link to="/auth/register">Register an account</Link>
      </div>
    </div>
  );
};
