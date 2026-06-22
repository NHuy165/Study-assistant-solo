import { useLoginStore } from '@/features/auth/stores/useLoginStore';
import { useLogin } from '@/features/auth/api/useLogin';
import { Link } from 'react-router-dom';

export const LoginForm = () => {
  const { username, password, setUsername, setPassword } = useLoginStore();
  const login = useLogin();

  const handleSubmit = (e: React.SubmitEvent<HTMLFormElement>) => {
    e.preventDefault();
    login.mutate({ username, password });
  };

  return (
    <div>
      <h2>Login</h2>

      {login.isError && <p>{login.error.message}</p>}
      {login.isPending && <p>Logging in, please wait</p>}

      <form onSubmit={handleSubmit}>
        <label>
          Email:
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </label>

        <br />

        <label>
          Password:
          <input
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </label>
        <button type="submit">Login</button>
      </form>

      <br />

      <Link to="/auth/register">Register an account</Link>
    </div>
  );
};
