import { useCreateNotes } from '../api/useCreateNotes';
import { NoteInputSchema } from '../types';

export const NoteForm = () => {
  const createNote = useCreateNotes();

  const handleSubmit = async (e: React.SubmitEvent<HTMLFormElement>) => {
    e.preventDefault();

    const formData = new FormData(e.currentTarget);

    createNote.mutate(
      NoteInputSchema.parse({
        title: formData.get('title') as string,
        content: formData.get('content') as string,
      }),
    );

    e.currentTarget.reset();
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>
          Title:
          <input type="text" name="title" />
        </label>

        <label>
          Content:
          <input type="text" name="content" />
        </label>

        <button type="submit">Add note</button>
      </form>
    </div>
  );
};
