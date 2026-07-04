import { LogoutButton } from '@/features/auth/components/LogoutButton';
import { InteractionCreateForm } from '@/features/interactions/components/InteractionCreateForm';
import { InteractionsList } from '@/features/interactions/components/InteractionsList';
import { StudyAssessments } from '@/features/study-progress/components/StudyAssessments';
import { StudyProgressSummarization } from '@/features/study-progress/components/StudyProgressSummarization';
import { UserPasswordChangeForm } from '@/features/user/components/UserPasswordChangeForm';
import { UserProfile } from '@/features/user/components/UserProfile';

export const HomePage = () => {
  return (
    <div className="max-w-3xl mx-auto py-6 space-y-8">
      <h1 className="text-6xl font-bold text-center">HOME PAGE</h1>

      {/* User info */}
      <div className="card shadow-xl border p-8">
        <h2 className="text-2xl font-bold text-center">User profile</h2>

        <UserProfile />
        <UserPasswordChangeForm />
        <LogoutButton />
      </div>

      {/* Study assessments */}
      <div className="card shadow-xl border p-8">
        <h2 className="text-2xl font-bold text-center">Study assessments</h2>
        <StudyAssessments />
      </div>

      {/* Interactions */}
      <div className="card shadow-xl border p-8">
        <h2 className="text-2xl font-bold text-center">Interactions</h2>
        <InteractionCreateForm />
        <InteractionsList />
      </div>

      {/* Study progress */}
      <div className="card shadow-xl border p-8">
        <h2 className="text-2xl font-bold text-center">Study progress</h2>
        <StudyProgressSummarization />
      </div>
    </div>
  );
};
