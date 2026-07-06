import type { RadioOption } from '@/types/miscellaneous/custom-component-types';
import {
  type UseFormRegister,
  type Path,
  type FieldValues,
  type FieldError,
} from 'react-hook-form';

export const RadioGroupField = <T extends FieldValues>({
  label,
  name,
  currentAnswer,
  options,
  register,
  wrapperStyle,
  labelStyle,
  inputStyle,
  disabled,
  error,
}: {
  label: string;
  name: Path<T>;
  currentAnswer: number;
  options: RadioOption[];
  register: UseFormRegister<T>;
  wrapperStyle?: string;
  labelStyle?: string;
  inputStyle?: string;
  disabled: boolean;
  error?: FieldError;
}) => {
  return (
    <div className={`${wrapperStyle}`}>
      {label && <span className={`${labelStyle}`}>{label}</span>}

      {options.map((option) => (
        <label key={option.value}>
          <input
            type="radio"
            value={option.value}
            disabled={disabled}
            {...register(name)}
          />
          <span className={`input ${inputStyle}`}>{option.label}</span>
          {/* If the answer is correct, display a correct sign. Else if the answer is not correct AND the user chose it, display a wrong sign. */}
          {option.isCorrect !== null &&
            (option.isCorrect
              ? ' (Correct answer)'
              : currentAnswer === option.value && ' (Wrong answer)')}
          <br />
        </label>
      ))}

      <div className="min-h-6 text-error">{error && error.message}</div>
    </div>
  );
};
