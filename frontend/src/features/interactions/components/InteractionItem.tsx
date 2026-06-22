import type { InteractionOutput } from '@/features/interactions/types/interaction';
import { Link } from 'react-router-dom';
import { useInteractionStore } from '@/features/interactions/stores/useInteractionStore';
import { InteractionUpdateForm } from '@/features/interactions/components/InteractionUpdateForm';
import { useDeleteInteraction } from '@/features/interactions/api/useDeleteInteraction';

export const InteractionItem = ({
  interaction,
}: {
  interaction: InteractionOutput;
}) => {
  // Fetches states
  const updateId = useInteractionStore((state) => state.updateId);

  const setUpdateId = useInteractionStore((state) => state.setUpdateId);
  const setUpdateName = useInteractionStore((state) => state.setUpdateName);
  const setUpdateDescription = useInteractionStore(
    (state) => state.setUpdateDescription,
  );
  const resetUpdate = useInteractionStore((state) => state.resetUpdate);

  const deleteInteraction = useDeleteInteraction();

  // Updates
  const handleClickUpdate = () => {
    if (updateId === interaction.id) {
      resetUpdate();
    } else {
      setUpdateId(interaction.id);
      setUpdateName(interaction.name);
      setUpdateDescription(interaction.description);
    }
  };

  // Deletes
  const handleClickDelete = () => {
    deleteInteraction.mutate(interaction.id);
  };

  return (
    <li>
      #{interaction.id} ({interaction.created_at}) {interaction.name} (
      {interaction.description}):
      <Link to={`/interaction/${interaction.id}`}>Enter</Link>
      {/* Update button */}
      <button onClick={handleClickUpdate}>Show update</button>
      {/* Delete button */}
      <button onClick={handleClickDelete}>Delete</button>
      {/* Delete status */}
      {deleteInteraction.isError && <p>{deleteInteraction.error.message}</p>}
      {deleteInteraction.isPending && <p>Deleting interaction, please wait.</p>}
      {/* Update form */}
      {updateId === interaction.id && (
        <>
          <br />

          <InteractionUpdateForm />
        </>
      )}
    </li>
  );
};
