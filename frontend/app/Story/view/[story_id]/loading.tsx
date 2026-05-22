import { Loader2 } from "lucide-react";

export default function StoryViewLoading() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen px-6 py-24">
      <div className="flex flex-col items-center gap-4 p-8 rounded-2xl bg-card border border-border/50 shadow-xl max-w-sm w-full text-center">
        <Loader2 className="h-10 w-10 animate-spin text-primary" />
        <div className="space-y-1">
          <h3 className="text-lg font-semibold text-foreground">Loading Story...</h3>
          <p className="text-xs text-muted-foreground font-medium">
            Retrieving your adventure from the archives.
          </p>
        </div>
      </div>
    </div>
  );
}
