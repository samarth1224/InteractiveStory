import StoryCreationContainer from "@/components/home page/StoryCreationContainer";
import StoryDiscoveryFeed from "@/components/home page/StoryDiscoveryFeed";

export default function Home() {
  return (
    <main className="min-h-screen pt-[72px] relative overflow-hidden">

      {/* ── Immersive Gradient Orbs ────────────────────── */}
      <div className="absolute -top-24 -left-36 w-[600px] h-[600px] rounded-full pointer-events-none blur-[120px] animate-[orbFloat_15s_ease-in-out_infinite] bg-[radial-gradient(circle,rgba(56,189,248,0.08)_0%,transparent_70%)]" />
      <div className="absolute top-48 -right-24 w-[500px] h-[500px] rounded-full pointer-events-none blur-[120px] animate-[orbFloat_18s_ease-in-out_-6s_infinite] bg-[radial-gradient(circle,rgba(99,102,241,0.06)_0%,transparent_70%)]" />
      <div className="absolute bottom-48 left-[30%] w-[400px] h-[400px] rounded-full pointer-events-none blur-[100px] animate-[orbFloat_20s_ease-in-out_-10s_infinite] bg-[radial-gradient(circle,rgba(14,165,233,0.05)_0%,transparent_70%)]" />

      {/* ── Hero Section ─────────────────────────────────────────────── */}
      <section className="relative z-10 text-center px-6 pt-20 pb-16">
        {/* Headline */}
        <h1 className="font-bold leading-tight max-w-[800px] mx-auto mb-5 animate-[fadeInUp_0.7s_ease_0.1s_both] text-[clamp(2.2rem,5vw,4rem)] text-foreground">
          {process.env.NEXT_PUBLIC_API_URL}
          <br />
          <span className="text-muted-foreground">
            Become Worlds
          </span>
        </h1>

        {/* Sub-headline */}
        <p className="text-muted-foreground max-w-[560px] mx-auto mb-12 leading-relaxed font-light animate-[fadeInUp_0.7s_ease_0.2s_both] text-[clamp(1rem,2vw,1.2rem)]">
          Craft immersive tales with AI. Every choice matters. Every story is
          uniquely yours.
        </p>

        {/* Creation card */}
        <div>
          <StoryCreationContainer />
        </div>
      </section>

      {/* ── Divider ─────────────────────────────────────────────────── */}
      <div className="w-full h-px bg-border my-10" />

      {/* ── Discovery feed ──────────────────────────────────────────── */}
      <div className="relative z-10">
        <StoryDiscoveryFeed />
      </div>

      {/* ── Footer ──────────────────────────────────────────────────── */}
      <footer className="flex flex-col items-center justify-center px-6 py-10 border-t border-border text-muted-foreground text-sm">
        <p className="text-foreground text-base mb-2 font-semibold tracking-widest">StoryForge</p>
        <div className="flex items-center gap-1.5">
          <span>Crafted with imagination & AI</span>
          <span className="ml-2">{new Date().getFullYear()}</span>
        </div>
      </footer>
    </main>
  );
}
