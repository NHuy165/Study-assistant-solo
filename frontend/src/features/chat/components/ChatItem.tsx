import type { ChatOutput } from '@/features/chat/types/chat';
import { useState } from 'react';

export const ChatItem = ({ chat }: { chat: ChatOutput }) => {
  const [showContent, setShowContent] = useState(false);
  return (
    <div>
      ({chat.created_at})
      <button onClick={() => setShowContent(!showContent)}>Show content</button>
      {showContent && (
        <div>
          Question: {chat.prompt}
          <br />
          Answer: {chat.answer}
        </div>
      )}
    </div>
  );
};
