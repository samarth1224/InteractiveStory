import StoryContainer from "@/components/story page/StoryContainer";
import { cookies } from "next/headers";

async function fetchStory({ storyname }: { storyname: string }) {
  const cookieStore = await cookies();
  const cookieString = cookieStore.getAll().map(c => `${c.name}=${c.value}`).join('; ');

  const baseUrl = process.env.NEXT_PUBLIC_API_URL || "https://localhost:25000";
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


export default async function StoryPage({ params }: { params: { storyname: string } }) {
  const { storyname } = await params;
  const storydata = await fetchStory({ storyname });

  return (
    <div className="flex items-center justify-center min-h-screen px-6 py-24">
      <StoryContainer
        StoryData={storydata}
      />
    </div>
  );
}