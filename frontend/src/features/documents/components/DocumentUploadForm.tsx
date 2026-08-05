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
import { useState } from 'react';
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
    setValue,
    reset,
    formState: { errors },
  } = useForm<DocumentInputForm, unknown, DocumentInput>({
    resolver: zodResolver(DocumentInputSchema),
    defaultValues: {
      name: null,
      page_starts_at: 1,
      subject_type: SubjectType.Other,
      subject_type_overwrite: 'false' as unknown as boolean,
      // These castings are used to satisfy HTML, which only accepts strings or numbers as values and the Zod schema, which requires something else.
      // String to boolean casting is done by Zod.
    },
  });
  const [showSubjectType, setShowSubjectType] = useState(true);

  const uploadDocument = useUploadDocument();

  const onSubmit: SubmitHandler<DocumentInput> = (data) => {
    uploadDocument.mutate(
      { interactionId, documentInput: data },
      { onSuccess: () => reset() },
    );
  };

  const handleSubjectOverwriteToggle = (
    e: React.ChangeEvent<HTMLSelectElement>,
  ) => {
    if (e.target.value === 'true') {
      setValue('subject_type', null);
      setShowSubjectType(false);
    } else {
      setShowSubjectType(true);
    }
  };

  return (
    <form
      className="card flex flex-col shadow-xl border border border-primary py-6 px-10 mx-10 mb-6"
      onSubmit={handleSubmit(onSubmit)}
    >
      <h3 className="font-bold text-2xl mb-3">Upload a document</h3>
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
      {showSubjectType && (
        <SelectField
          label="Subject type"
          name="subject_type"
          inputStyle="w-full"
          labelStyle="font-semibold block mb-2"
          options={Object.entries(SubjectType).map(([label, value]) => {
            return { label, value };
          })}
          register={register}
          error={errors.subject_type}
        />
      )}

      {/* Subject type overwrite */}
      <SelectField
        label="Allow automatic subject type overwrite"
        name="subject_type_overwrite"
        inputStyle="w-full"
        labelStyle="font-semibold block mb-2"
        onChange={handleSubjectOverwriteToggle}
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
  );
};
