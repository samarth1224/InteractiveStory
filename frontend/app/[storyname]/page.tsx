import StoryContainer from "@/components/story page/StoryContainer";

export default async function Story(
    { params }:
        {
            params: Promise<{ storyname: string }>
        }) {
    const { storyname } = await params;
    const response = await fetch('http://localhost:8007/story/generate_story', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ story_description: storyname }),
    });
    const data = await response.json()

    return <div className='flex items-center justify-center h-screen'>
        <StoryContainer storyname={storyname} image={data.image} choice={data.choice} content={data.content} />
    </div>
}