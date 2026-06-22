import { LoginForm } from '@/features/auth/components/LoginForm';
import { RegisterForm } from '@/features/auth/components/RegisterForm';
import { useTokenStore } from '@/features/auth/stores/useTokenStore';
import { Navigate, Route, Routes } from 'react-router-dom';

export const AuthPage = () => {
  const token = useTokenStore((state) => state.token);

  if (token) {
    return <Navigate to="/home" replace />;
  }

  return (
    <div>
      <h1>AUTH PAGE</h1>

      <Routes>
        <Route path="register" element={<RegisterForm />} />
        <Route path="login" element={<LoginForm />} />
        <Route index element={<Navigate to="login" replace />} />
      </Routes>
    </div>
  );
};
