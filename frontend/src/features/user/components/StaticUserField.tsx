import { type UserOutput, type UserUpdate } from '@/features/user/types/user';
import { useGetUser } from '@/features/user/api/useGetUser';
import { capitalizeString, replaceUnderscore } from '@/utils/format-string';

export const StaticUserField = ({
  field,
}: {
  field: Exclude<keyof UserOutput, keyof UserUpdate>;
}) => {
  const value = useGetUser().data?.[field];

  return (
    <div>
      {capitalizeString(replaceUnderscore(field))}: {value}
    </div>
  );
};
