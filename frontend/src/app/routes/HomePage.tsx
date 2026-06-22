import { LogoutButton } from '@/features/auth/components/LogoutButton';
import { InteractionCreateForm } from '@/features/interactions/components/InteractionCreateForm';
import { InteractionsList } from '@/features/interactions/components/InteractionsList';

export const HomePage = () => {
  return (
    <div>
      <h1>HOME PAGE</h1>
      <LogoutButton />

      <h2>Interactions</h2>
      <InteractionCreateForm />
      <InteractionsList />
    </div>
  );
};
