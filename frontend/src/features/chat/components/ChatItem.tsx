import { MarkdownText } from '@/components/miscellaneous/MarkdownText';
import type { ChatOutput } from '@/features/chat/types/chat';

export const ChatItem = ({ chat }: { chat: ChatOutput }) => {
  return (
    <li className="space-y-3">
      <div>
        <span className="font-bold">User: </span>
        <div>{chat.prompt}</div>
      </div>
      <div>
        <span className="font-bold">Chatbot: </span>
        <MarkdownText content={chat.answer} />
      </div>
      <span className="divider divider-primary"></span>
    </li>
  );
};
