export const SubmitButton = ({
  disabled,
  text,
  textDisabled,
}: {
  disabled: boolean;
  text: string;
  textDisabled: string;
}) => {
  return (
    <button type="submit" disabled={disabled}>
      {disabled ? textDisabled : text}
    </button>
  );
};
