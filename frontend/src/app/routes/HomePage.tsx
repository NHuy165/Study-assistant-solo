import { LogoutButton } from '@/features/auth/components/LogoutButton';
import { InteractionCreateForm } from '@/features/interactions/components/InteractionCreateForm';
import { InteractionsList } from '@/features/interactions/components/InteractionsList';
import { UserPasswordChangeForm } from '@/features/user/components/UserPasswordChangeForm';
import { UserProfile } from '@/features/user/components/UserProfile';

export const HomePage = () => {
  return (
    <div>
      <h1>HOME PAGE</h1>

      <h2>User</h2>
      <LogoutButton />
      <UserPasswordChangeForm />
      <UserProfile />

      <h2>Interactions</h2>
      <InteractionCreateForm />
      <InteractionsList />
    </div>
  );
};
