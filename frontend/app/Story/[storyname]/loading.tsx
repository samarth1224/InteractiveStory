import { Sparkles, Loader2 } from "lucide-react";

export default function StoryLoading() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen px-6 py-24">
      <div className="flex flex-col items-center gap-6 p-10 rounded-2xl bg-card border border-border/50 shadow-2xl max-w-md w-full text-center">
        <div className="relative">
          <Loader2 className="h-12 w-12 animate-spin text-primary opacity-50" />
          <Sparkles className="h-5 w-5 text-primary absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2" />
        </div>
        <div className="space-y-2">
          <h3 className="text-xl font-bold text-foreground tracking-tight">Crafting Your Story</h3>
          <p className="text-sm text-muted-foreground font-medium animate-pulse">
            Our AI agents are weaving the plotlines... This may take a few moments.
          </p>
        </div>
      </div>
    </div>
  );
}
