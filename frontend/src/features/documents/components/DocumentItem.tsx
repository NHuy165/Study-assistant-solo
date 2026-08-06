import { useState } from 'react';
import type { DocumentOutput } from '@/features/documents/types/document';
import { useDeleteDocument } from '@/features/documents/api/useDeleteDocument';
import { DocumentUpdateForm } from '@/features/documents/components/DocumentUpdateForm';
import { useGetDocumentComplete } from '@/features/documents/api/useGetDocumentComplete';
import { capitalizeString } from '@/utils/format-string';
import { Button } from '@/components/miscellaneous/Button';
import { ButtonCreateStudyActivity } from '@/features/documents/components/ButtonCreateStudyActivity';
import { ButtonCreateLLMResponse } from '@/features/documents/components/ButtonCreateLLMResponse';

export const DocumentItem = ({ document }: { document: DocumentOutput }) => {
  // Fetches states
  const [showUpdateForm, setShowUpdateForm] = useState(false);
  const [showDetails, setShowDetails] = useState(false);
  const deleteDocument = useDeleteDocument();
  const getDocumentComplete = useGetDocumentComplete(document.id, showDetails);

  return (
    <li>
      <div>
        {/* Main document */}
        <Button
          style="w-2/3"
          text={`#${document.id} ${document.name} (${
            document.subject_type
              ? capitalizeString(document.subject_type)
              : 'Other'
          })`}
          onClick={() => setShowDetails(!showDetails)}
        />
        <Button
          style="w-1/3"
          text="Delete"
          textDisabled="Deleting..."
          btnError={true}
          onClick={() => deleteDocument.mutate(document.id)}
        />

        {/* More details */}
        {showDetails && (
          <section className="card shadow-xl border border-primary mt-3 p-6">
            <h3 className="font-bold text-3xl mb-3">Details</h3>
            <div className="space-y-2">
              {/* Normal details */}
              <p>
                <span className="font-bold">Uploaded at:</span>{' '}
                {document.created_at}
              </p>
              <p>
                <span className="font-bold">Document type:</span>{' '}
                {document.type}
              </p>

              {/* Document analysis */}

              {/* Summary */}
              <p>
                <span className="font-bold">Document summary:</span>{' '}
                {getDocumentComplete.isError && 'Failed to fetch data.'}
                {getDocumentComplete.isPending && 'Fetching data...'}
                {getDocumentComplete.isError ||
                  getDocumentComplete.isPending || (
                    <div className="whitespace-pre-wrap max-h-60 overflow-y-auto">
                      {getDocumentComplete.data?.[1]?.summary ||
                        'This document has no content.'}
                    </div>
                  )}
              </p>

              {/* Recommendations */}
              <p>
                <span className="block font-bold">Recommendations:</span>{' '}
                {getDocumentComplete.isError && 'Failed to fetch data.'}
                {getDocumentComplete.isPending && 'Fetching data...'}
                {getDocumentComplete.isError ||
                  getDocumentComplete.isPending || (
                    <div className="space-y-8">
                      {/* Study activity recommendations */}
                      <section className="mt-4">
                        <span className="font-bold divider mb-8 divider-primary">
                          Create study activities
                        </span>
                        <ul className="space-y-6">
                          {(getDocumentComplete.data?.[1]
                            ?.material_recommendations?.length ?? 0) > 0 ? (
                            <>
                              {getDocumentComplete.data?.[1]?.material_recommendations?.map(
                                (recommendation) => (
                                  <ButtonCreateStudyActivity
                                    interactionId={document.interaction_id}
                                    studyActivityInput={{
                                      ...recommendation,
                                      document_id: document.id,
                                    }}
                                  />
                                ),
                              )}
                            </>
                          ) : (
                            <span>
                              Document has no study activity recommendation.
                            </span>
                          )}
                        </ul>
                      </section>

                      {/* LLM chat recommendations */}
                      <section>
                        <span className="font-bold divider mb-8 divider-primary">
                          Chat with LLM
                        </span>
                        <ul className="space-y-6">
                          {(getDocumentComplete.data?.[1]
                            ?.question_recommendations?.length ?? 0) > 0 ? (
                            <>
                              {getDocumentComplete.data?.[1]?.question_recommendations?.map(
                                (recommendation) => (
                                  <ButtonCreateLLMResponse
                                    interactionId={document.interaction_id}
                                    chatInput={{
                                      ...recommendation,
                                      document_id: document.id,
                                    }}
                                  />
                                ),
                              )}
                            </>
                          ) : (
                            <span>
                              Document has no LLM chat recommendation.
                            </span>
                          )}
                        </ul>
                      </section>
                    </div>
                  )}
              </p>
            </div>

            {/* Update button & Update form */}
            <Button
              style="w-full mt-6"
              text="Show update"
              onClick={() => setShowUpdateForm(!showUpdateForm)}
            />
            {showUpdateForm && (
              <div>
                <DocumentUpdateForm
                  document={document}
                  onUpdate={() => setShowUpdateForm(false)}
                />
              </div>
            )}
          </section>
        )}
      </div>
    </li>
  );
};
