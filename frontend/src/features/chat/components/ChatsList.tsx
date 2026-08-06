import { useGetChats } from '@/features/chat/api/useGetChats';
import { ChatItem } from '@/features/chat/components/ChatItem';

export const ChatsList = ({ interactionId }: { interactionId: number }) => {
  const getChats = useGetChats(interactionId);

  return (
    <section className="border border-primary min-h-30 max-h-140 p-3 overflow-y-auto space-y-8 break-words">
      {getChats.isError && <p>Failed to fetch data.</p>}
      {getChats.isPending && <p>Fetching data...</p>}

      {getChats.isError ||
        getChats.isPending ||
        (getChats.data && getChats.data.length > 0 ? (
          <ol>
            {getChats.data.map((chat) => (
              <ChatItem key={chat.id} chat={chat} />
            ))}
          </ol>
        ) : (
          <span>No chat history to show.</span>
        ))}
    </section>
  );
};
