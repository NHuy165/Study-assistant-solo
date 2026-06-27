import type { SelectOption } from '@/types/miscellaneous/select-option';
import {
  type UseFormRegister,
  type Path,
  type FieldValues,
  type FieldError,
} from 'react-hook-form';

export const FormField = <T extends FieldValues>({
  label,
  name,
  register,
  error,
  accept,
  type = 'text',
  placeholder = '',
}: {
  label: string;
  name: Path<T>;
  register: UseFormRegister<T>;
  error?: FieldError;
  accept?: string;
  type?: React.HTMLInputTypeAttribute;
  placeholder?: string;
}) => {
  return (
    <label>
      {label}
      <input
        type={type}
        accept={type === 'file' ? accept : undefined}
        placeholder={placeholder}
        {...register(name, {
          // Converts number field to an actual number, make it null if input is lacking
          setValueAs: (value) => {
            if (type === 'number') {
              return value === '' ? null : Number(value);
            }
            return value;
          },
        })}
      />
      {error && error.message}
    </label>
  );
};

export const SelectField = <T extends FieldValues>({
  label,
  name,
  options,
  register,
  error,
}: {
  label: string;
  name: Path<T>;
  options: SelectOption[];
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
        <option value="">None</option>

        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>

      {error && error.message}
    </label>
  );
};
