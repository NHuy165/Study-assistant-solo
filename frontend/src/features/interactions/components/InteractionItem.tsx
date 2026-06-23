import type { InteractionOutput } from '@/features/interactions/types/interaction';
import { Link } from 'react-router-dom';
import { InteractionUpdateForm } from '@/features/interactions/components/InteractionUpdateForm';
import { useDeleteInteraction } from '@/features/interactions/api/useDeleteInteraction';
import { useState } from 'react';

export const InteractionItem = ({
  interaction,
}: {
  interaction: InteractionOutput;
}) => {
  // Fetches states
  const [showUpdateForm, setShowUpdateForm] = useState(false);
  const deleteInteraction = useDeleteInteraction();

  // Updates
  const handleClickUpdate = () => {
    setShowUpdateForm(!showUpdateForm);
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
      {showUpdateForm && (
        <>
          <br />

          <InteractionUpdateForm
            interaction={interaction}
            onUpdate={() => setShowUpdateForm(false)}
          />
        </>
      )}
    </li>
  );
};
