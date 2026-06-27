import { ChatForm } from '@/features/chat/components/ChatForm';
import { ChatsList } from '@/features/chat/components/ChatsList';
import { DocumentsList } from '@/features/documents/components/DocumentsList';
import { DocumentUploadForm } from '@/features/documents/components/DocumentUploadForm';
import { useParams } from 'react-router-dom';

export const MainInteractionPage = () => {
  const { interactionId } = useParams();

  return (
    <div>
      <h1>INTERACTION #{interactionId}</h1>
      <h1></h1>

      <h2>Documents</h2>
      <DocumentUploadForm interactionId={Number(interactionId)} />
      <DocumentsList interactionId={Number(interactionId)} />

      <h2>Chat</h2>
      <ChatForm interactionId={Number(interactionId)} />
      <ChatsList interactionId={Number(interactionId)} />
    </div>
  );
};
