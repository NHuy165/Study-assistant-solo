import { FormField } from '@/components/form-elements';
import { SubmitButton } from '@/components/SubmitButton';
import { useCreateChat } from '@/features/chat/api/useCreateChat';
import { type ChatInput, ChatInputSchema } from '@/features/chat/types/chat';
import { zodResolver } from '@hookform/resolvers/zod';
import { type SubmitHandler, useForm } from 'react-hook-form';

export const ChatForm = ({ interactionId }: { interactionId: number }) => {
  const createChat = useCreateChat();
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<ChatInput>({
    resolver: zodResolver(ChatInputSchema),
    defaultValues: { prompt: '', document_id: null },
  });

  const onSubmit: SubmitHandler<ChatInput> = (data) => {
    createChat.mutate(
      { interactionId, chatInput: data },
      { onSuccess: () => reset() },
    );
  };

  return (
    <div>
      {createChat.isError && createChat.error.message}
      {createChat.isPending && 'Generating an answer, please wait.'}
      <form onSubmit={handleSubmit(onSubmit)}>
        {/* Prompt */}
        <FormField
          label="Chat prompt"
          name="prompt"
          register={register}
          error={errors.prompt}
        />

        <br />

        <SubmitButton
          disabled={createChat.isPending}
          text="Send"
          textDisabled="Sending text..."
        />
      </form>
    </div>
  );
};
