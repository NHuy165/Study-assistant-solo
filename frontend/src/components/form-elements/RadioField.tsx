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
  optionTextStyle,
  optionsWrapperStyle,
  labelStyle,
  optionStyle,
  disabled,
  error,
}: {
  label: string;
  name: Path<T>;
  currentAnswer: number;
  options: RadioOption[];
  register: UseFormRegister<T>;
  wrapperStyle?: string;
  optionTextStyle?: string;
  optionsWrapperStyle?: string;
  labelStyle?: string;
  optionStyle?: string;
  disabled: boolean;
  error?: FieldError;
}) => {
  return (
    <div className={`${wrapperStyle}`}>
      {label && <span className={`${labelStyle}`}>{label}</span>}

      <div className={`${optionsWrapperStyle}`}>
        {options.map((option) => (
          <label className={`block ${optionStyle}`} key={option.value}>
            <input
              className={`radio radio-primary`}
              type="radio"
              value={option.value}
              disabled={disabled}
              {...register(name)}
            />
            <span className={`${optionTextStyle}`}>
              {option.label}{' '}
              {option.isCorrect !== null &&
                (option.isCorrect ? (
                  <span className="text-success ml-3">Correct answer</span>
                ) : (
                  currentAnswer === option.value && (
                    <span className="text-error ml-3">Wrong answer</span>
                  )
                ))}
            </span>
            {/* If the answer is correct, display a correct sign. Else if the answer is not correct AND the user chose it, display a wrong sign. */}
          </label>
        ))}
      </div>

      <p className="min-h-6 text-error">{error && error.message}</p>
    </div>
  );
};
