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
    <button
      className="btn btn-primary btn-hover my-6"
      type="submit"
      disabled={disabled}
    >
      {disabled ? textDisabled : text}
    </button>
  );
};
