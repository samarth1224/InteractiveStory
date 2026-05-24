'use client';

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth-context";
import StoryDiscoveryFeed from "@/components/home page/StoryDiscoveryFeed";
import { StoryData } from "@/interfaces/storydata.type";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";

const baseURL = process.env.NEXT_PUBLIC_API_URL || "https://localhost:25000";

export default function MyStoriesPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [stories, setStories] = useState<StoryData[]>([]);
  const [fetching, setFetching] = useState(true);

  useEffect(() => {
    if (authLoading) return;

    if (!user) {
      router.push("/auth/login");
      return;
    }

    const loadStories = async () => {
      try {
        const response = await fetch(`${baseURL}/story/stories/my`, {
          credentials: "include"
        });
        if (response.ok) {
          const data = await response.json();
          setStories(data);
        }
      } catch (error) {
        console.error("failed to fetch my stories:", error);
      } finally {
        setFetching(false);
      }
    };

    loadStories();
  }, [user, authLoading, router]);

  if (authLoading || (user && fetching)) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="flex flex-col items-center gap-4">
          <div className="w-10 h-10 border-4 border-[#8fa89b] border-t-transparent rounded-full animate-spin" />
          <p className="text-muted-foreground text-sm font-medium animate-pulse">Loading your library...</p>
        </div>
      </div>
    );
  }

  // If unauthorized and redirecting, return null to prevent screen flash
  if (!user) {
    return null;
  }

  return (
    <main className="min-h-screen pt-[100px] relative overflow-hidden bg-background">
      <div className="max-w-[1200px] mx-auto px-6 mb-8">
        <Link href="/" className="inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors">
          <ArrowLeft className="w-4 h-4" />
          Back to Home
        </Link>
      </div>

      <div className="relative z-10">
        {stories && stories.length > 0 ? (
          <StoryDiscoveryFeed Stories={stories} title="My Stories" subtitle="Your Creations" />
        ) : (
          <div className="max-w-[1200px] mx-auto px-6 py-20 text-center">
            <h2 className="text-2xl font-bold text-foreground mb-4">No stories yet</h2>
            <p className="text-muted-foreground mb-8">You haven't created any stories yet. Start a new adventure from the home page!</p>
            <Link href="/" className="px-6 py-3 rounded-full bg-foreground text-background font-semibold hover:opacity-90 transition-opacity">
              Create a Story
            </Link>
          </div>
        )}
      </div>
    </main>
  );
}
