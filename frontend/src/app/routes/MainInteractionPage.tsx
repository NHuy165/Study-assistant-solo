import { ChatForm } from '@/features/chat/components/ChatForm';
import { ChatsList } from '@/features/chat/components/ChatsList';
import { DocumentsList } from '@/features/documents/components/DocumentsList';
import { DocumentUploadForm } from '@/features/documents/components/DocumentUploadForm';
import { useGetInteractions } from '@/features/interactions/api/useGetInteractions';
import { FlashcardsActivityCreateForm } from '@/features/study-activities/components/FlashcardsActivityCreateForm';
import { StudyActivityCreateForm } from '@/features/study-activities/components/StudyActivityCreateForm';
import { StudyActivityDisplaysList } from '@/features/study-activities/components/StudyActivityDisplaysList';
import { Link, useParams } from 'react-router-dom';

export const MainInteractionPage = () => {
  const { interactionId } = useParams();
  const getInteractions = useGetInteractions();
  const interaction = getInteractions.data?.find(
    (interaction) => interaction.id === Number(interactionId as string),
  );

  return (
    <div className="max-w-3xl mx-auto py-6">
      {getInteractions.isPending && <p>Fetching data...</p>}
      {getInteractions.isError && <p>Failed to fetch data.</p>}
      {getInteractions.isPending || getInteractions.isError || interaction ? (
        <div className="space-y-8">
          {/* Title */}
          <div className="border-b pb-6">
            <h1 className="text-6xl font-bold text-center">
              {interaction?.name}
            </h1>
            <p className="px-6">
              <span className="block font-bold text-xl mb-3">
                Description:{' '}
              </span>
              <span className="block max-h-30 overflow-y-auto break-words whitespace-pre-wrap border p-3">
                {interaction?.description}
              </span>
            </p>
          </div>

          {/* Documents */}
          <div className="card shadow-xl border p-8">
            <h2 className="text-5xl font-bold text-center mb-10">Documents</h2>
            <DocumentUploadForm interactionId={Number(interactionId)} />
            <DocumentsList interactionId={Number(interactionId)} />
          </div>

          {/* LLM Chat */}
          <div className="card shadow-xl border p-8">
            <h2 className="text-5xl font-bold text-center mb-10">Chat</h2>

            <ChatsList interactionId={Number(interactionId)} />
            <ChatForm interactionId={Number(interactionId)} />
          </div>

          {/* Study activities */}
          <div className="card shadow-xl border p-8">
            <h2 className="text-5xl font-bold text-center mb-10">
              Study Activities
            </h2>
            <StudyActivityCreateForm interactionId={Number(interactionId)} />
            <FlashcardsActivityCreateForm
              interactionId={Number(interactionId)}
            />
            <StudyActivityDisplaysList interactionId={Number(interactionId)} />
          </div>
        </div>
      ) : (
        <Link to="/home" className="link link-primary link-hover">
          This interaction does not exist, go back to the Home Page?
        </Link>
      )}
    </div>
  );
};
