import StoryContainer from "@/components/story page/StoryContainer";
import { cookies } from "next/headers";

const baseUrl = process.env.NEXT_PUBLIC_API_URL || "https://localhost:25000";

async function fetchStory({ story_id }: { story_id: string }) {
  const cookieStore = await cookies();
  const cookieString = cookieStore.getAll().map(c => `${c.name}=${c.value}`).join('; ');

  const res = await fetch(`${baseUrl}/story/${story_id}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "Cookie": cookieString
    },
    credentials: "include",
  });

  if (!res.ok) {
    throw new Error("Failed to fetch story");
  }
  const data = await res.json();
  return data;
};

async function fetchNodes({ story_id }: { story_id: string }) {
  const cookieStore = await cookies();
  const cookieString = cookieStore.getAll().map(c => `${c.name}=${c.value}`).join('; ');

  const res = await fetch(`${baseUrl}/story/${story_id}/nodes`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "Cookie": cookieString
    },
    credentials: "include",
  });

  if (!res.ok) {
    throw new Error("Failed to fetch nodes");
  }
  const data = await res.json();
  return data;
}


export default async function StoryViewPage({ params }: { params: { story_id: string } }) {
  const { story_id } = await params;
  const storydata = await fetchStory({ story_id });
  if (storydata) {
    storydata.nodes = await fetchNodes({ story_id: storydata.public_id });
  }

  return (
    <div className="flex items-center justify-center min-h-screen px-6 py-24">
      {storydata ? (
        <StoryContainer
          StoryData={storydata}
        />
      ) : (
        <div className="text-center">Story not found.</div>
      )}
    </div>
  );
}
