import { type UserOutput, type UserUpdate } from '@/features/user/types/user';
import { useGetUser } from '@/features/user/api/useGetUser';
import { capitalizeString, replaceUnderscore } from '@/utils/format-string';
import { useState } from 'react';
import { UserFieldUpdateForm } from '@/features/user/components/UserFieldUpdateForm';

export const ChangeableUserField = ({
  field,
}: {
  field: keyof UserOutput & keyof UserUpdate;
}) => {
  const value = useGetUser().data?.[field];
  const [showUpdateForm, setShowUpdateForm] = useState(false);

  return (
    <div>
      {capitalizeString(replaceUnderscore(field))}: {value}
      <button onClick={() => setShowUpdateForm(!showUpdateForm)}>Update</button>
      {showUpdateForm && (
        <UserFieldUpdateForm
          field={field}
          onUpdate={() => setShowUpdateForm(false)}
        />
      )}
    </div>
  );
};
