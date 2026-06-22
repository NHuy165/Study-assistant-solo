import { useGetInteractions } from '@/features/interactions/api/useGetInteractions';
import { InteractionItem } from '@/features/interactions/components/InteractionItem';

export const InteractionsList = () => {
  const getInteractions = useGetInteractions();

  return (
    <div>
      {getInteractions.isError && <p>{getInteractions.error.message}</p>}
      {getInteractions.isPending && <p>Fetching interactions, please wait.</p>}

      <ul>
        {getInteractions.data?.map((interaction) => (
          <InteractionItem key={interaction.id} interaction={interaction} />
        ))}
      </ul>
    </div>
  );
};
