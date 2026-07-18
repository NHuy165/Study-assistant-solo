import { ChangeableUserField } from '@/features/user/components/ChangeableUserField';
import { StaticUserField } from '@/features/user/components/StaticUserField';

export const UserProfile = () => {
  return (
    <dl>
      <StaticUserField label="User ID" field="id" />
      <StaticUserField label="Account creation time" field="created_at" />
      <StaticUserField label="Current login streak" field="login_streak" />
      <StaticUserField
        label="Longest login streak"
        field="longest_login_streak"
      />
      <ChangeableUserField label="Username" field="username" />
      <ChangeableUserField label="Email" field="email" />
      <ChangeableUserField label="Description" field="description" />
    </dl>
  );
};
