import type { ChatOutput } from '@/features/chat/types/chat';

export const ChatItem = ({ chat }: { chat: ChatOutput }) => {
  return (
    <div className="space-y-3">
      <span className="block">
        <span className="font-bold">User: </span>
        {chat.prompt}
      </span>
      <span className="block">
        <span className="font-bold">Chatbot: </span>
        {chat.answer}
      </span>
    </div>
  );
};
