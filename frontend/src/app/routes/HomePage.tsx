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
      <section className="card shadow-xl border border border-primary p-8">
        <h2 className="text-5xl font-bold text-center mb-10">User profile</h2>

        <UserProfile />
        <UserPasswordChangeForm />
        <LogoutButton />
      </section>

      {/* Study assessments */}
      <section className="card shadow-xl border border border-primary p-8">
        <h2 className="text-5xl font-bold text-center mb-10">
          Study assessments
        </h2>
        <StudyAssessments />
      </section>

      {/* Interactions */}
      <section className="card shadow-xl border border border-primary p-8">
        <h2 className="text-5xl font-bold text-center mb-10">Interactions</h2>
        <InteractionCreateForm />
        <InteractionsList />
      </section>

      {/* Study progress */}
      <section className="card shadow-xl border border border-primary p-8">
        <h2 className="text-5xl font-bold text-center mb-10">Study progress</h2>
        <StudyProgressSummarization />
      </section>
    </div>
  );
};
