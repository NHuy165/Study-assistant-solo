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
    </div>
  );
};
