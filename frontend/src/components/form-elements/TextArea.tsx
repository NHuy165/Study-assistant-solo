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
  placeholder = '',
}: {
  label: string;
  name: Path<T>;
  register: UseFormRegister<T>;
  error?: FieldError;
  placeholder?: string;
}) => {
  return (
    <label>
      <p className="font-bold">{label}</p>
      <textarea
        className="textarea h-32"
        placeholder={placeholder}
        {...register(name)}
        maxLength={2000}
      />

      <div className="min-h-6 text-error">{error && error.message}</div>
    </label>
  );
};
