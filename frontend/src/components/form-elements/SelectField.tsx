import type { SelectOption } from '@/types/miscellaneous/custom-component-types';
import {
  type UseFormRegister,
  type Path,
  type FieldValues,
  type FieldError,
} from 'react-hook-form';

export const SelectField = <T extends FieldValues>({
  label,
  name,
  options,
  includeNoneOption = false,
  register,
  error,
}: {
  label: string;
  name: Path<T>;
  options: SelectOption[];
  includeNoneOption?: boolean;
  register: UseFormRegister<T>;
  error?: FieldError;
}) => {
  return (
    <label>
      {label}

      {/* If any value is "", it's changed to null. */}
      <select
        {...register(name, {
          setValueAs: (value) => (value === '' ? null : value),
        })}
      >
        {includeNoneOption && <option value="">None</option>}

        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>

      <div className="min-h-6 text-error">{error && error.message}</div>
    </label>
  );
};
