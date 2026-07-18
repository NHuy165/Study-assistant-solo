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
  wrapperStyle,
  labelStyle,
  inputStyle,
  type = 'text',
  placeholder = '',
  disabled = false,
}: {
  label: string;
  name: Path<T>;
  register: UseFormRegister<T>;
  error?: FieldError;
  accept?: string;
  wrapperStyle?: string;
  labelStyle?: string;
  inputStyle?: string;
  type?: React.HTMLInputTypeAttribute;
  placeholder?: string;
  disabled?: boolean;
}) => {
  return (
    <label className={`${wrapperStyle}`}>
      {label && <span className={`${labelStyle}`}>{label}</span>}
      <input
        className={`input input-primary ${inputStyle}`}
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

      <p className="min-h-6 text-error" role="alert">
        {error && error.message}
      </p>
    </label>
  );
};
