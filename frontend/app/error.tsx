'use client';

import { useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { AlertCircle } from 'lucide-react';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log the error to an error reporting service
    console.error(error);
  }, [error]);

  return (
    <div className="flex flex-col items-center justify-center min-h-[70vh] w-full px-4 text-center">
      <div className="bg-destructive/10 p-4 rounded-full mb-6">
        <AlertCircle className="h-12 w-12 text-destructive" strokeWidth={1.5} />
      </div>
      <h2 className="text-2xl font-bold tracking-tight mb-2">Something went wrong!</h2>
      <p className="text-muted-foreground max-w-md mb-8">
        We encountered an unexpected error while trying to load this page. Please try again.
      </p>
      <Button 
        onClick={() => reset()}
        variant="default"
        className="min-w-[120px]"
      >
        Try again
      </Button>
    </div>
  );
}
