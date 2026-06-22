import { useUpdateInteraction } from '@/features/interactions/api/useUpdateInteraction';
import { useInteractionStore } from '@/features/interactions/stores/useInteractionStore';

export const InteractionUpdateForm = () => {
  // Fetches states
  const updateId = useInteractionStore((state) => state.updateId);
  const updateName = useInteractionStore((state) => state.updateName);
  const updateDescription = useInteractionStore(
    (state) => state.updateDescription,
  );

  const setUpdateName = useInteractionStore((state) => state.setUpdateName);
  const setUpdateDescription = useInteractionStore(
    (state) => state.setUpdateDescription,
  );

  const updateInteraction = useUpdateInteraction();

  // Update function
  const handleSubmit = (e: React.SubmitEvent<HTMLFormElement>) => {
    e.preventDefault();
    updateInteraction.mutate({
      id: updateId as number,
      interactionUpdate: { name: updateName, description: updateDescription },
    });
  };

  return (
    <div>
      {updateInteraction.isError && <p>{updateInteraction.error.message}</p>}
      {updateInteraction.isPending && (
        <p>Updating the interaction, please wait.</p>
      )}

      <form onSubmit={handleSubmit}>
        {/* Name */}
        <label>
          Name:
          <input
            value={updateName}
            onChange={(e) => setUpdateName(e.target.value)}
          />
        </label>

        <br />

        {/* Description */}
        <label>
          Description:
          <input
            value={updateDescription}
            onChange={(e) => setUpdateDescription(e.target.value)}
          />
        </label>

        {/* Submit button */}
        <button type="submit">Update</button>
      </form>
    </div>
  );
};
