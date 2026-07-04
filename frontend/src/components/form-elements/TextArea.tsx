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
  inputStyle,
  placeholder = '',
}: {
  label: string;
  name: Path<T>;
  register: UseFormRegister<T>;
  error?: FieldError;
  wrapperStyle?: string;
  inputStyle?: string;
  placeholder?: string;
}) => {
  return (
    <label className={`${wrapperStyle}`}>
      <p className="font-semibold mb-3">{label}</p>
      <textarea
        className={`textarea h-32 ${inputStyle}`}
        placeholder={placeholder}
        {...register(name)}
        maxLength={2000}
      />

      <div className="min-h-6 text-error">{error && error.message}</div>
    </label>
  );
};
