import type { SelectOption } from '@/types/miscellaneous/custom-component-types';
import { replaceUnderscore, titleString } from '@/utils/format-string';
import type React from 'react';
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
  onChange,
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
  onChange?: (e: React.ChangeEvent<HTMLSelectElement>) => void;
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
          onChange: (e) => onChange?.(e),
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
