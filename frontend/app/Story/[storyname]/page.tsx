import StoryContainer from "@/components/story page/StoryContainer";
import { cookies } from "next/headers";

const baseUrl = process.env.NEXT_PUBLIC_API_URL || "https://localhost:25000";

async function fetchStory({ storyname }: { storyname: string }) {
  const cookieStore = await cookies();
  const cookieString = cookieStore.getAll().map(c => `${c.name}=${c.value}`).join('; ');


  try {
    const res = await fetch(`${baseUrl}/story/generate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Cookie": cookieString
      },
      body: JSON.stringify(storyname),
      credentials: "include",

    });

    if (!res.ok) {
      throw new Error("Failed to generate story");
    }
    const data = await res.json();
    return data;
  } catch (err) {
    console.error("Data fetching error caught silently:", err);
    return null;
  }
};

async function fetchNodes({ story_id }: { story_id: string }) {
  const cookieStore = await cookies();
  const cookieString = cookieStore.getAll().map(c => `${c.name}=${c.value}`).join('; ');

  try {
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
  } catch (err) {
    console.error("Data fetching error caught silently:", err);
    return null;
  }
}


export default async function StoryPage({ params }: { params: { storyname: string } }) {
  const { storyname } = await params;
  const storydata = await fetchStory({ storyname });
  storydata.nodes = await fetchNodes({ story_id: storydata.public_id });

  return (
    <div className="flex items-center justify-center min-h-screen px-6 py-24">
      <StoryContainer
        StoryData={storydata}
      />
    </div>
  );
}