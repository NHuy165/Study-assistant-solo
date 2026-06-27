import { FormField, SelectField } from '@/components/FormField';
import { SubmitButton } from '@/components/SubmitButton';
import { useUploadDocument } from '@/features/documents/api/useUploadDocument';
import {
  DocumentInputSchema,
  type DocumentInput,
} from '@/features/documents/types/document';
import { SubjectType } from '@/types/constants';
import { zodResolver } from '@hookform/resolvers/zod';
import { type SubmitHandler, useForm } from 'react-hook-form';

export const DocumentUploadForm = ({
  interactionId,
}: {
  interactionId: number;
}) => {
  // Fetches states
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<DocumentInput>({
    resolver: zodResolver(DocumentInputSchema),
    defaultValues: {
      name: null,
      page_starts_at: 1,
      subject_type: null,
      subject_type_overwrite: false,
    },
  });

  const uploadDocument = useUploadDocument();

  const onSubmit: SubmitHandler<DocumentInput> = (data) => {
    uploadDocument.mutate({ interactionId, documentInput: data });
  };

  return (
    <div>
      {uploadDocument.isError && <p>{uploadDocument.error.message}</p>}
      {uploadDocument.isPending && <p>Uploading document, please wait.</p>}

      <form onSubmit={handleSubmit(onSubmit)}>
        {/* File upload */}
        <FormField
          label="File"
          name="file"
          type="file"
          accept="image/*, text/*, .pdf"
          register={register}
          error={errors.name}
        />

        <br />

        {/* Name */}
        <FormField
          label="Name"
          name="name"
          placeholder="Blank for original name"
          register={register}
          error={errors.name}
        />

        <br />

        {/* Page starts at */}
        <FormField
          label="Page starts at"
          name="page_starts_at"
          register={register}
          error={errors.page_starts_at}
          type="number"
        />

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

        {/* Subject type overwrite */}
        <FormField
          label="Subject type overwrite"
          name="subject_type_overwrite"
          register={register}
          error={errors.subject_type}
          type="checkbox"
        />

        <br />

        {/* Submit button */}
        <SubmitButton
          disabled={uploadDocument.isPending}
          text="Upload"
          textDisabled="Uploading..."
        />
      </form>
    </div>
  );
};
