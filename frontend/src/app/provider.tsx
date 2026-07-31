import { type ReactNode } from 'react';
import {
  MutationCache,
  QueryCache,
  QueryClient,
  QueryClientProvider,
} from '@tanstack/react-query';
import toast, { Toaster } from 'react-hot-toast';
import * as z from 'zod';

z.config(z.locales.en());

const queryClient = new QueryClient({
  queryCache: new QueryCache({
    onError: (error) => {
      console.log(`Request error: ${error.message}`);
      toast.error(error.message);
    },
  }),

  mutationCache: new MutationCache({
    onError: (error) => {
      console.log(`Request error: ${error.message}`);
      toast.error(error.message);
    },
  }),
});

export const AppProvider = ({ children }: { children: ReactNode }) => {
  return (
    <>
      <Toaster position="bottom-right" />
      <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
    </>
  );
};
