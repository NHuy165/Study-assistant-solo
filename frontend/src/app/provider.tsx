import { type ReactNode } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';

const queryClient = new QueryClient();

export const AppProvider = ({ children }: { children: ReactNode }) => {
  return (
    <>
      <Toaster position="bottom-right" />
      <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
    </>
  );
};
