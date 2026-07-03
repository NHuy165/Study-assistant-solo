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
    <div className="min-h-screen flex flex-col items-center justify-center gap-8">
      <h1 className="text-6xl font-bold text-center">AUTHENTICATION</h1>

      {/* The actual forms */}
      <div className="card w-96 p-8 shadow-xl border">
        <Routes>
          <Route path="register" element={<RegisterForm />} />
          <Route path="login" element={<LoginForm />} />
          <Route index element={<Navigate to="login" replace />} />
        </Routes>
      </div>
    </div>
  );
};
