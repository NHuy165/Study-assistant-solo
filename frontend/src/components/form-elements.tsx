import type {
  RadioOption,
  SelectOption,
} from '@/types/miscellaneous/custom-component-types';
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
  disabled = false,
}: {
  label: string;
  name: Path<T>;
  register: UseFormRegister<T>;
  error?: FieldError;
  accept?: string;
  type?: React.HTMLInputTypeAttribute;
  placeholder?: string;
  disabled?: boolean;
}) => {
  return (
    <label>
      {label}
      <br />
      <input
        type={type}
        accept={type === 'file' ? accept : undefined}
        placeholder={placeholder}
        disabled={disabled}
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

      {error && error.message}
    </label>
  );
};

export const RadioGroupField = <T extends FieldValues>({
  label,
  name,
  currentAnswer,
  options,
  register,
  disabled,
  error,
}: {
  label: string;
  name: Path<T>;
  currentAnswer: number;
  options: RadioOption[];
  register: UseFormRegister<T>;
  disabled: boolean;
  error?: FieldError;
}) => {
  return (
    <div>
      <p>{label}</p>

      {options.map((option) => (
        <label key={option.value}>
          <input
            type="radio"
            value={option.value}
            disabled={disabled}
            {...register(name)}
          />
          {option.label}
          {/* If the answer is correct, display a correct sign. Else if the answer is not correct AND the user chose it, display a wrong sign. */}
          {option.isCorrect !== null &&
            (option.isCorrect
              ? ' (Correct answer)'
              : currentAnswer === option.value && ' (Wrong answer)')}
          <br />
        </label>
      ))}

      {error && error.message}
    </div>
  );
};
