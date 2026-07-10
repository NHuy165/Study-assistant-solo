import { TextArea } from '@/components/form-elements/TextArea';
import { Button } from '@/components/miscellaneous/Button';
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
    <div className="mt-6">
      <form className="flex items-center" onSubmit={handleSubmit(onSubmit)}>
        <Button
          disabled={createChat.isPending}
          style="w-1/5 rounded-none h-20"
          text="Send"
          textDisabled="Sending text..."
          type="submit"
        />
        <TextArea
          label=""
          name="prompt"
          wrapperStyle="flex items-center w-full h-20"
          inputStyle="w-full rounded-none h-20 whitespace-pre-wrap overflow-y-auto"
          disabled={createChat.isPending}
          register={register}
          error={errors.prompt}
        />
      </form>
    </div>
  );
};
