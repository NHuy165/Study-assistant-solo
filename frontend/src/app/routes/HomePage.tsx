import { LogoutButton } from '@/features/auth/components/LogoutButton';
import { InteractionCreateForm } from '@/features/interactions/components/InteractionCreateForm';
import { InteractionsList } from '@/features/interactions/components/InteractionsList';
import { StudyAssessments } from '@/features/study-progress/components/StudyAssessments';
import { StudyProgressSummarization } from '@/features/study-progress/components/StudyProgressSummarization';
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

      <h2>Study assessments</h2>
      <StudyAssessments />

      <h2>Interactions</h2>
      <InteractionCreateForm />
      <InteractionsList />

      <h2>Study progress</h2>
      <StudyProgressSummarization />
    </div>
  );
};
