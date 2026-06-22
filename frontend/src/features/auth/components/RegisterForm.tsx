import { useRegister } from '@/features/auth/api/useRegister';
import { useRegisterStore } from '@/features/auth/stores/useRegisterStore';
import { Link } from 'react-router-dom';

export const RegisterForm = () => {
  const {
    username,
    email,
    password,
    description,
    setUsername,
    setEmail,
    setPassword,
    setDescription,
  } = useRegisterStore();
  const register = useRegister();

  const handleSubmit = (e: React.SubmitEvent<HTMLFormElement>) => {
    e.preventDefault();
    register.mutate({ username, email, password, description });
  };

  return (
    <div>
      <h2>Register</h2>

      {register.isError && <p>{register.error.message}</p>}
      {register.isPending && <p>Registering user, please wait</p>}

      <form onSubmit={handleSubmit}>
        {/* Username */}
        <label>
          Username:
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </label>

        <br />

        {/* Email */}
        <label>
          Email:
          <input value={email} onChange={(e) => setEmail(e.target.value)} />
        </label>

        <br />

        {/* Password */}
        <label>
          Password:
          <input
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </label>

        <br />

        {/* Description */}
        <label>
          Description:
          <input
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </label>

        {/* Submit button */}
        <button type="submit">Register</button>
      </form>

      <br />

      <Link to="/auth/login">Log into an account</Link>
    </div>
  );
};
