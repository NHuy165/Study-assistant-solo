import { type UserOutput, type UserUpdate } from '@/features/user/types/user';
import { useGetUser } from '@/features/user/api/useGetUser';

export const StaticUserField = ({
  label,
  field,
}: {
  label: string;
  field: Exclude<keyof UserOutput, keyof UserUpdate>;
}) => {
  const getUser = useGetUser();

  return (
    <div className="flex items-center border-b min-h-10">
      <span className="font-semibold w-1/3">{label}</span>
      <span className="flex-1">
        {getUser.isPending
          ? 'Fetching data...'
          : getUser.isError
            ? 'Failed to fetch data.'
            : getUser.data[field]}
      </span>
    </div>
  );
};
