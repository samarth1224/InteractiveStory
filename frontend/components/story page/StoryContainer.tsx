'use client'
import Image from "next/image";
import { useState } from 'react';

function StoryDisplay({ content, image }: { content: string; image: string }) {
    return (
        <div className='flex gap-2 outline-purple-600'>
            <Image src={image}
                alt='sample image'
                width={300}
                height={500}
                className='rounded-lg shadow-md flex-1 outline outline-blue-600' />
            <p className="outline flex-1">{content}
            </p>
        </div>
    )
}


function ChoiceButtons({ choice }: { choice: { text: string; id: number }[] }) {
    return (
        <div className='flex gap-2 justify-center'>
            {choice.map((choice) => (
                <button key={choice.id} className='outline outline-blue-600 hover:bg-blue-600'>{choice.text}</button>
            ))}
        </div>
    )
}




export default function StoryContainer({ content, storyname, image, choice }:
    {
        content: string,
        storyname: string,
        image: string,
        choice: { text: string; id: number }[]
    }) {
    const [storySegmentArray, setStorySegmentArray] = useState();

    return (
        <div className='size-3/4 flex flex-col gap-2 p-2 outline outline-red-600 '>
            <h1 className="text-2xl text-center
             outline outline-Emerald-500">{storyname}</h1>
            <StoryDisplay image={image} content={content} />
            <ChoiceButtons choice={choice} />
        </div>
    )
}