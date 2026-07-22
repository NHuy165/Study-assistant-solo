import type { ChatOutput } from '@/features/chat/types/chat';

export const ChatItem = ({ chat }: { chat: ChatOutput }) => {
  return (
    <li className="space-y-3">
      <div>
        <span className="font-bold">User: </span>
        <span>{chat.prompt}</span>
      </div>
      <div>
        <span className="font-bold">Chatbot: </span>
        <span>{chat.answer}</span>
      </div>
      <span className="divider divider-primary"></span>
    </li>
  );
};
