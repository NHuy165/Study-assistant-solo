import { useGetDocuments } from '@/features/documents/api/useGetDocuments';
import { DocumentItem } from '@/features/documents/components/DocumentItem';

export const DocumentsList = ({ interactionId }: { interactionId: number }) => {
  const getDocuments = useGetDocuments(interactionId);

  return (
    <div>
      {getDocuments.isError && <p>{getDocuments.error.message}</p>}
      {getDocuments.isPending && <p>Fetching documents, please wait.</p>}

      <ul>
        {getDocuments.data?.map((document) => (
          <DocumentItem key={document.id} document={document} />
        ))}
      </ul>
    </div>
  );
};
