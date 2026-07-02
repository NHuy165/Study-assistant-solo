import { useTokenStore } from '@/features/auth/stores/useTokenStore';
import { useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';

export const LogoutButton = () => {
  const setToken = useTokenStore((state) => state.setToken);
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const handleClick = () => {
    setToken(null);
    queryClient.clear();
    navigate('/auth');
  };

  return <button onClick={handleClick}>Logout</button>;
};
