import { type UserOutput, type UserUpdate } from '@/features/user/types/user';
import { useGetUser } from '@/features/user/api/useGetUser';
import { useState } from 'react';
import { UserFieldUpdateForm } from '@/features/user/components/UserFieldUpdateForm';
import { Button } from '@/components/miscellaneous/Button';

export const ChangeableUserField = ({
  label,
  field,
}: {
  label: string;
  field: keyof UserOutput & keyof UserUpdate;
}) => {
  const getUser = useGetUser();
  const [showUpdateForm, setShowUpdateForm] = useState(false);

  return (
    <div className="border-b">
      <div className="flex items-center min-h-10 max-h-30">
        <span className="font-semibold w-1/3">{label}</span>
        <span className="flex-1 max-h-30 overflow-y-auto break-words whitespace-pre-wrap">
          {getUser.isPending
            ? 'Fetching data...'
            : getUser.isError
              ? 'Failed to fetch data.'
              : getUser.data[field]}
        </span>
        {getUser.isPending || (
          <Button
            text="Update"
            onClick={() => setShowUpdateForm(!showUpdateForm)}
            style="btn-ghost ml-3"
          />
        )}
      </div>
      {showUpdateForm && (
        <UserFieldUpdateForm
          label={`New ${label}`}
          field={field}
          onUpdate={() => setShowUpdateForm(false)}
        />
      )}
    </div>
  );
};
