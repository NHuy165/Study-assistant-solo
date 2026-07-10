import type { InteractionOutput } from '@/features/interactions/types/interaction';
import { useNavigate } from 'react-router-dom';
import { InteractionUpdateForm } from '@/features/interactions/components/InteractionUpdateForm';
import { useDeleteInteraction } from '@/features/interactions/api/useDeleteInteraction';
import { useState } from 'react';
import { Button } from '@/components/miscellaneous/Button';

export const InteractionItem = ({
  interaction,
}: {
  interaction: InteractionOutput;
}) => {
  // Fetches states
  const [showUpdateForm, setShowUpdateForm] = useState(false);
  const [showDetails, setShowDetails] = useState(false);
  const deleteInteraction = useDeleteInteraction();
  const navigate = useNavigate();

  return (
    <li>
      <div className="flex">
        {/* Main interaction */}
        <Button
          style="w-2/3"
          text={`#${interaction.id} ${interaction.name}`}
          onClick={() => navigate(`/interaction/${interaction.id}`)}
        />
        {/* More details */}
        <Button
          style="w-1/9"
          text="Details"
          onClick={() => setShowDetails(!showDetails)}
        />
        {/* Show update form */}
        <Button
          style="w-1/9"
          text="Update"
          onClick={() => setShowUpdateForm(!showUpdateForm)}
        />
        {/* Delete */}
        <Button
          style="w-1/9"
          text="Delete"
          textDisabled="Deleting..."
          btnError={true}
          onClick={() => deleteInteraction.mutate(interaction.id)}
        />
      </div>

      {/* Details */}
      {showDetails && (
        <div className="card shadow-xl border mt-3 p-6">
          <h3 className="font-bold text-3xl mb-3">Details</h3>
          <div className="max-h-30 overflow-y-auto break-words whitespace-pre-wrap">
            <p>
              <span className="font-bold">Created at:</span>{' '}
              {interaction.created_at}
            </p>
            <p>
              <span className="font-bold">Description:</span>{' '}
              {interaction.description}
            </p>
          </div>
        </div>
      )}

      {/* Update form */}
      {showUpdateForm && (
        <div>
          <InteractionUpdateForm
            interaction={interaction}
            onUpdate={() => setShowUpdateForm(false)}
          />
        </div>
      )}
    </li>
  );
};
