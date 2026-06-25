import { useState } from 'react';
import type { DocumentOutput } from '@/features/documents/types/document';
import { useDeleteDocument } from '@/features/documents/api/useDeleteDocument';
import { DocumentUpdateForm } from '@/features/documents/components/DocumentUpdateForm';
import { useGetDocumentComplete } from '@/features/documents/api/useGetDocumentComplete';

export const DocumentItem = ({ document }: { document: DocumentOutput }) => {
  // Fetches states
  const [showUpdateForm, setShowUpdateForm] = useState(false);
  const [showDocumentAnalysis, setShowDocumentAnalysis] = useState(false);
  const deleteDocument = useDeleteDocument();
  const getDocumentComplete = useGetDocumentComplete(
    document.id,
    showDocumentAnalysis,
  );

  return (
    <li>
      <>
        #{document.id} ({document.created_at}) {document.name} (
        {document.subject_type}) (type: {document.type})
      </>

      {/* Analysis button */}
      <button onClick={() => setShowDocumentAnalysis(!showDocumentAnalysis)}>
        Analysis
      </button>

      {/* Update button */}
      <button onClick={() => setShowUpdateForm(!showUpdateForm)}>
        Show update
      </button>

      {/* Delete button */}
      <button onClick={() => deleteDocument.mutate(document.id)}>Delete</button>

      {/* Delete status */}
      {deleteDocument.isError && <p>{deleteDocument.error.message}</p>}
      {deleteDocument.isPending && <p>Deleting interaction, please wait.</p>}

      {/* Document analysis */}
      {showDocumentAnalysis && (
        <div>
          {getDocumentComplete.isError && (
            <p>{getDocumentComplete.error.message}</p>
          )}
          {getDocumentComplete.isPending ? (
            <p>Fetching document, please wait.</p>
          ) : (
            getDocumentComplete.data?.[1]?.summary ||
            'This document has no content.'
          )}
        </div>
      )}

      {/* Update form */}
      {showUpdateForm && (
        <div>
          <DocumentUpdateForm
            document={document}
            onUpdate={() => setShowUpdateForm(false)}
          />
        </div>
      )}
    </li>
  );
};
