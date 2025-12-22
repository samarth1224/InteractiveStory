import Image from "next/image";
import Link from "next/link";





export default function Home() {
  return (
    <div className="h-screen flex flex-col gap-6 p-2 m-2 outline outline-grey-950 items-center">
      <textarea
        className="size-1/2 mt-24 outline outline-gray-950 p-2 resize-none"
        placeholder="Start typing..."
      />
      <Link href="/some-story-name" className=" outline outline-grey-950">Go to Story</Link>
    </div>
  );
}
