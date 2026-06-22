import { useTokenStore } from '@/features/auth/stores/useTokenStore';
import { useNavigate } from 'react-router-dom';

export const LogoutButton = () => {
  const setToken = useTokenStore((state) => state.setToken);
  const navigate = useNavigate();

  const handleClick = () => {
    setToken(null);
    navigate('/auth');
  };

  return <button onClick={handleClick}>Logout</button>;
};
