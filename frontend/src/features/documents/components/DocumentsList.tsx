import { useGetDocuments } from '@/features/documents/api/useGetDocuments';
import { DocumentItem } from '@/features/documents/components/DocumentItem';

export const DocumentsList = ({ interactionId }: { interactionId: number }) => {
  const getDocuments = useGetDocuments(interactionId);

  return (
    <div>
      <h2 className="font-bold text-4xl mb-6">Documents list:</h2>

      {getDocuments.isError && <p>Failed to fetch data.</p>}
      {getDocuments.isPending && <p>Fetching data...</p>}

      {getDocuments.isPending ||
        getDocuments.isError ||
        (getDocuments.data.length > 0 ? (
          <ul className="space-y-3">
            {getDocuments.data?.map((document) => (
              <DocumentItem key={document.id} document={document} />
            ))}
          </ul>
        ) : (
          <span>User has no uploaded document.</span>
        ))}
    </div>
  );
};
