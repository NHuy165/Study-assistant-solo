import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
  Outlet,
} from 'react-router-dom';
import { AuthPage } from '@/app/routes/AuthPage';
import { useTokenStore } from '@/features/auth/stores/useTokenStore';
import { HomePage } from '@/app/routes/HomePage';

// Redirects to auth if token is null
export const ProtectedRoute = () => {
  const token = useTokenStore((state) => state.token);

  if (!token) {
    return <Navigate to="/auth" replace />;
  }

  return <Outlet />;
};

// Main router
export const AppRouter = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route index element={<Navigate to="/home" replace />} />

        {/* Public routes */}
        <Route path="/auth/*" element={<AuthPage />} />

        {/* Protected routes */}
        <Route element={<ProtectedRoute />}>
          <Route path="/home" element={<HomePage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};
