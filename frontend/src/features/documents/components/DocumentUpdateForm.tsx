import { Button } from '@/components/miscellaneous/Button';
import { useUpdateDocument } from '@/features/documents/api/useUpdateDocument';
import {
  DocumentUpdateSchema,
  type DocumentOutput,
  type DocumentUpdate,
} from '@/features/documents/types/document';
import { SubjectType } from '@/types/constants';
import { zodResolver } from '@hookform/resolvers/zod';
import { type SubmitHandler, useForm } from 'react-hook-form';
import { FormField } from '@/components/form-elements/FormField';
import { SelectField } from '@/components/form-elements/SelectField';

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
    <form
      className="card shadow-xl border border border-primary mt-3 mb-6 p-6"
      onSubmit={handleSubmit(onSubmit)}
    >
      <h3 className="font-bold text-3xl mb-3">Update</h3>

      {/* Name */}
      <FormField
        label="New name"
        name="name"
        inputStyle="w-1/1"
        labelStyle="font-semibold block mb-2"
        register={register}
        error={errors.name}
      />

      {/* Subject type */}
      <SelectField
        label="New subject type"
        name="subject_type"
        inputStyle="w-1/1"
        labelStyle="font-semibold block mb-2"
        options={Object.entries(SubjectType).map(([label, value]) => {
          return { label, value };
        })}
        register={register}
        error={errors.subject_type}
      />

      {/* Submit button */}
      <Button
        disabled={updateDocument.isPending}
        style="mt-3"
        text="Update"
        textDisabled="Updating..."
        type="submit"
      />
    </form>
  );
};
