import { ChangeableUserField } from '@/features/user/components/ChangeableUserField';
import { StaticUserField } from '@/features/user/components/StaticUserField';

export const UserProfile = () => {
  return (
    <div>
      <StaticUserField field="id" />
      <StaticUserField field="created_at" />
      <StaticUserField field="login_streak" />
      <StaticUserField field="longest_login_streak" />
      <ChangeableUserField field="username" />
      <ChangeableUserField field="email" />
      <ChangeableUserField field="description" />
    </div>
  );
};
