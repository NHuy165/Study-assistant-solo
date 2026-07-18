import type { SelectOption } from '@/types/miscellaneous/custom-component-types';
import { replaceUnderscore, titleString } from '@/utils/format-string';
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
  wrapperStyle,
  labelStyle,
  inputStyle,
  error,
}: {
  label: string;
  name: Path<T>;
  options: SelectOption[];
  includeNoneOption?: boolean;
  register: UseFormRegister<T>;
  wrapperStyle?: string;
  labelStyle?: string;
  inputStyle?: string;
  error?: FieldError;
}) => {
  return (
    <label className={`${wrapperStyle}`}>
      {label && <span className={`${labelStyle}`}>{label}</span>}

      {/* If any value is "", it's changed to null. */}
      <select
        className={`select select-primary ${inputStyle}`}
        {...register(name, {
          setValueAs: (value) => (value === '' ? null : value),
        })}
      >
        {includeNoneOption && <option value="">None</option>}

        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {titleString(replaceUnderscore(option.label))}
          </option>
        ))}
      </select>

      <p className="min-h-6 text-error" role="alert">
        {error && error.message}
      </p>
    </label>
  );
};
