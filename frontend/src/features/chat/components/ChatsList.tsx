import { useGetChats } from '@/features/chat/api/useGetChats';
import { ChatItem } from '@/features/chat/components/ChatItem';

export const ChatsList = ({ interactionId }: { interactionId: number }) => {
  const getChats = useGetChats(interactionId);

  return (
    <div>
      {getChats.isError && <p>{getChats.error.message}</p>}
      {getChats.isPending && <p>Fetching conversations, please wait.</p>}

      {getChats.data?.map((chat) => (
        <ChatItem chat={chat} />
      ))}
    </div>
  );
};
