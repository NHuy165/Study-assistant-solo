import { useCreateInteraction } from '@/features/interactions/api/useCreateInteraction';
import { useInteractionStore } from '@/features/interactions/stores/useInteractionStore';

export const InteractionCreateForm = () => {
  const {
    createName: name,
    createDescription: description,
    setCreateName: setName,
    setCreateDescription: setDescription,
  } = useInteractionStore();

  const createInteraction = useCreateInteraction();

  const handleSubmit = (e: React.SubmitEvent<HTMLFormElement>) => {
    e.preventDefault();
    createInteraction.mutate({ name, description });
  };

  return (
    <div>
      {createInteraction.isError && <p>{createInteraction.error.message}</p>}
      {createInteraction.isPending && <p>Creating interaction, please wait.</p>}

      <form onSubmit={handleSubmit}>
        {/* Name */}
        <label>
          Name:
          <input value={name} onChange={(e) => setName(e.target.value)} />
        </label>

        <br />

        {/* Description */}
        <label>
          Description:
          <input
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </label>

        {/* Submit button */}
        <button type="submit">Register</button>
      </form>
    </div>
  );
};
