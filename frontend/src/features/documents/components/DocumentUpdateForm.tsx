import { FormField, SelectField } from '@/components/form-elements';
import { SubmitButton } from '@/components/SubmitButton';
import { useUpdateDocument } from '@/features/documents/api/useUpdateDocument';
import {
  DocumentUpdateSchema,
  type DocumentOutput,
  type DocumentUpdate,
} from '@/features/documents/types/document';
import { DocumentType, SubjectType } from '@/types/constants';
import { zodResolver } from '@hookform/resolvers/zod';
import { type SubmitHandler, useForm } from 'react-hook-form';

export const DocumentUpdateForm = ({
  document,
  onUpdate,
}: {
  document: DocumentOutput;
  onUpdate: () => void;
}) => {
  // Fetches states
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<DocumentUpdate>({
    resolver: zodResolver(DocumentUpdateSchema),
    values: {
      name: document.name,
      page_starts_at: document.page_starts_at,
      subject_type: document.subject_type,
    },
  });

  const updateDocument = useUpdateDocument();

  // Updates function
  const onSubmit: SubmitHandler<DocumentUpdate> = (data) => {
    updateDocument.mutate(
      {
        documentId: document.id,
        documentUpdate: data,
      },
      { onSuccess: () => onUpdate() },
    );
  };

  return (
    <div>
      {updateDocument.isError && <p>{updateDocument.error.message}</p>}
      {updateDocument.isPending && <p>Updating the document, please wait.</p>}

      <form onSubmit={handleSubmit(onSubmit)}>
        {/* Name */}
        <FormField
          label="Name"
          name="name"
          register={register}
          error={errors.name}
        />

        <br />

        {/* Page starts at, only available if document is a PDF */}
        {document.type == DocumentType.Pdf && (
          <FormField
            label="Page starts at"
            name="page_starts_at"
            register={register}
            error={errors.page_starts_at}
          />
        )}

        <br />

        {/* Subject type */}
        <SelectField
          label="Subject type"
          name="subject_type"
          options={Object.entries(SubjectType).map(([label, value]) => {
            return { label, value };
          })}
          register={register}
          error={errors.subject_type}
        />

        <br />

        {/* Submit button */}
        <SubmitButton
          disabled={updateDocument.isPending}
          text="Update"
          textDisabled="Updating..."
        />
      </form>
    </div>
  );
};
