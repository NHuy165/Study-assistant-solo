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
  labelStyle,
  inputStyle,
  placeholder = '',
}: {
  label: string;
  name: Path<T>;
  register: UseFormRegister<T>;
  error?: FieldError;
  wrapperStyle?: string;
  labelStyle?: string;
  inputStyle?: string;
  placeholder?: string;
}) => {
  return (
    <label className={`${wrapperStyle}`}>
      {label && <span className={`${labelStyle}`}>{label}</span>}
      <textarea
        className={`textarea ${inputStyle}`}
        placeholder={placeholder}
        {...register(name)}
        maxLength={2000}
      />

      <div className="min-h-6 text-error">{error && error.message}</div>
    </label>
  );
};
