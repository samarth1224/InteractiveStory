'use client';
import Link from 'next/link';
import { useState } from 'react';

export default function PromptContainer() {
  const [input, setInput] = useState('');

  return (
    <div className="h-screen flex flex-col gap-6 p-2 m-2 outline outline-grey-950 items-center">
      <textarea
        className="size-1/2 mt-24 outline outline-gray-950 p-2 resize-none"
        placeholder="Start typing..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />
      <Link href={`/${input}`} className=" outline outline-grey-950">Go to Story</Link>
    </div>
  );
}