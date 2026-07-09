import { FormField } from '@/components/form-elements/FormField';
import { SelectField } from '@/components/form-elements/SelectField';
import { Button } from '@/components/miscellaneous/Button';
import { useUploadDocument } from '@/features/documents/api/useUploadDocument';
import {
  DocumentInputSchema,
  type DocumentInput,
  type DocumentInputForm,
} from '@/features/documents/types/document';
import { SubjectType } from '@/types/constants';
import { zodResolver } from '@hookform/resolvers/zod';
import { type FieldError, type SubmitHandler, useForm } from 'react-hook-form';

export const DocumentUploadForm = ({
  interactionId,
}: {
  interactionId: number;
}) => {
  // Fetches states
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<DocumentInputForm, unknown, DocumentInput>({
    resolver: zodResolver(DocumentInputSchema),
    defaultValues: {
      name: null,
      page_starts_at: 1,
      subject_type: '' as unknown as null, // This bypasses the check and gets the select field to default to the nu;l; option (whose initial value is actually '')
      subject_type_overwrite: 'false' as unknown as boolean,
    },
  });

  const uploadDocument = useUploadDocument();

  const onSubmit: SubmitHandler<DocumentInput> = (data) => {
    uploadDocument.mutate(
      { interactionId, documentInput: data },
      { onSuccess: () => reset() },
    );
  };

  return (
    <div className="card shadow-xl border py-6 px-10 mx-10 mb-6">
      <h3 className="font-bold text-2xl mb-3">Upload a document</h3>

      <form className="flex flex-col" onSubmit={handleSubmit(onSubmit)}>
        {/* File upload */}
        <FormField
          label="File:"
          name="file"
          type="file"
          inputStyle="file-input file-input-primary w-full p-0"
          labelStyle="font-semibold block mb-2"
          accept="image/*, text/*, .pdf"
          register={register}
          error={errors.name}
        />

        {/* Name */}
        <FormField
          label="Name"
          name="name"
          inputStyle="w-full"
          labelStyle="font-semibold block mb-2"
          placeholder="Blank for original name"
          register={register}
          error={errors.name}
        />

        {/* Page starts at */}
        <FormField
          label="Page starts at"
          name="page_starts_at"
          inputStyle="w-full"
          labelStyle="font-semibold block mb-2"
          register={register}
          error={errors.page_starts_at}
          type="number"
        />

        {/* Subject type */}
        <SelectField
          label="Subject type"
          name="subject_type"
          inputStyle="w-full"
          labelStyle="font-semibold block mb-2"
          options={Object.entries(SubjectType).map(([label, value]) => {
            return { label, value };
          })}
          includeNoneOption={true}
          register={register}
          error={errors.subject_type}
        />

        {/* Subject type overwrite */}
        <SelectField
          label="Allow automatic subject type overwrite"
          name="subject_type_overwrite"
          inputStyle="w-full"
          labelStyle="font-semibold block mb-2"
          options={[
            { label: 'Yes', value: 'true' },
            { label: 'No', value: 'false' },
          ]}
          register={register}
          error={errors.subject_type_overwrite as FieldError | undefined}
        />

        {/* Submit button */}
        <Button
          disabled={uploadDocument.isPending}
          style="mt-6"
          text="Upload"
          textDisabled="Uploading..."
          type="submit"
        />
      </form>
    </div>
  );
};
