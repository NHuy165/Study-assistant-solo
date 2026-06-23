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
}: {
  label: string;
  name: Path<T>;
  register: UseFormRegister<T>;
  error?: FieldError;
}) => {
  return (
    <label>
      {label}
      <input {...register(name)} />
      {error && error.message}
    </label>
  );
};
