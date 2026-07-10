import {
  type UseFormRegister,
  type Path,
  type FieldValues,
  type FieldError,
} from 'react-hook-form';

export const TextArea = <T extends FieldValues>({
  label,
  name,
  register,
  error,
  wrapperStyle,
  disabled = false,
  labelStyle,
  inputStyle,
  placeholder = '',
}: {
  label: string;
  name: Path<T>;
  register: UseFormRegister<T>;
  error?: FieldError;
  wrapperStyle?: string;
  disabled?: boolean;
  labelStyle?: string;
  inputStyle?: string;
  placeholder?: string;
}) => {
  return (
    <label className={`${wrapperStyle}`}>
      {label && <span className={`${labelStyle}`}>{label}</span>}
      <textarea
        className={`textarea textarea-primary ${inputStyle}`}
        placeholder={placeholder}
        {...register(name)}
        maxLength={2000}
        disabled={disabled}
      />

      <div className="min-h-6 text-error">{error && error.message}</div>
    </label>
  );
};
