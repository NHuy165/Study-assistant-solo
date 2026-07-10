import { useGetChats } from '@/features/chat/api/useGetChats';
import { ChatItem } from '@/features/chat/components/ChatItem';

export const ChatsList = ({ interactionId }: { interactionId: number }) => {
  const getChats = useGetChats(interactionId);

  return (
    <div className="border border-primary min-h-30 max-h-140 p-3 whitespace-pre-wrap overflow-y-auto space-y-8 break-words">
      {getChats.isError && <p>Failed to fetch data.</p>}
      {getChats.isPending && <p>Fetching data...</p>}

      {getChats.isError ||
        getChats.isPending ||
        (getChats.data && getChats.data.length > 0 ? (
          getChats.data.map((chat) => <ChatItem chat={chat} />)
        ) : (
          <span>No chat history to show.</span>
        ))}
    </div>
  );
};
