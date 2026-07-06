import { useGetInteractions } from '@/features/interactions/api/useGetInteractions';
import { InteractionItem } from '@/features/interactions/components/InteractionItem';

export const InteractionsList = () => {
  const getInteractions = useGetInteractions();

  return (
    <div>
      <h2 className="font-bold text-4xl mb-3">Interactions list:</h2>

      {getInteractions.isError && <p>Failed to fetch data.</p>}
      {getInteractions.isPending && <p>Fetching data...</p>}

      {getInteractions.isPending ||
        getInteractions.isError ||
        (getInteractions.data.length > 0 ? (
          <ul>
            {getInteractions.data?.map((interaction) => (
              <InteractionItem key={interaction.id} interaction={interaction} />
            ))}
          </ul>
        ) : (
          <span>User currently has no Interactions.</span>
        ))}
    </div>
  );
};
