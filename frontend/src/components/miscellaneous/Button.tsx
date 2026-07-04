export const Button = ({
  text,
  textDisabled,
  style,
  disabled,
  type = 'button',
  btnError = false,
  onClick,
}: {
  text: string;
  textDisabled?: string;
  style?: string;
  disabled?: boolean;
  type?: React.ButtonHTMLAttributes<HTMLButtonElement>['type'];
  btnError?: boolean;
  onClick?: React.MouseEventHandler<HTMLButtonElement>;
}) => {
  return (
    <button
      className={`btn ${btnError ? 'btn-error' : 'btn-primary'} btn-hover btn-outline ${style}`}
      type={type}
      disabled={disabled}
      onClick={onClick}
    >
      {disabled ? textDisabled : text}
    </button>
  );
};
