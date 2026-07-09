import { Button } from '@/components/miscellaneous/Button';
import { useCreateChat } from '@/features/chat/api/useCreateChat';
import type { ChatInput } from '@/features/chat/types/chat';

export const ButtonCreateLLMResponse = ({
  interactionId,
  chatInput,
}: {
  interactionId: number;
  chatInput: ChatInput;
}) => {
  const createChat = useCreateChat();

  return (
    <div className="flex justify-center items-center h-20">
      <Button
        text="Chat with LLM"
        textDisabled="Generating..."
        style="h-20 rounded-none shadow-xl w-1/6"
        disabled={createChat.isPending}
        onClick={() => createChat.mutate({ interactionId, chatInput })}
      />
      <div className="shadow-xl border px-3 py-1 h-20 whitespace-pre-wrap overflow-y-auto flex-1">
        <p>
          <span className="font-bold">Prompt: </span> {chatInput.prompt}
        </p>
      </div>
    </div>
  );
};
