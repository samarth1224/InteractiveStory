'use client';

import { useState } from 'react';
import Image from 'next/image';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ArrowRight, Zap } from 'lucide-react';
import { StoryData } from '@/interfaces/storydata.type';
import { StoryChoice } from '@/interfaces/storydata.type';

const baseUrl = process.env.NEXT_PUBLIC_API_URL || "https://localhost:25000";

function StoryDisplay({ content, image, pageNumber }: { content: string; image: string | null; pageNumber: number }) {
  return (
    <div className="space-y-6">
      {image && image !== 'sample' && (
        <div className="relative aspect-video w-full overflow-hidden rounded-xl border border-border/40 shadow-2xl">
          <Image
            src={image}
            alt="Story illustration"
            fill
            className="object-cover transition-transform duration-700 hover:scale-105"
            priority
          />
        </div>
      )}
      <div className="prose prose-sm prose-invert max-w-none relative">
        <p className="text-foreground/90 leading-relaxed text-lg font-serif">{content}</p>
        <div className="flex justify-end mt-4">
          <span className="text-[10px] uppercase tracking-widest text-muted-foreground font-bold bg-muted/30 px-2 py-1 rounded">
            Page {pageNumber}
          </span>
        </div>
      </div>
    </div>
  );
}

function ChoiceButtons({ choice, onSubmit }: {
  choice: StoryChoice[];
  onSubmit: (choice_id: number) => void;
}) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full">
      {choice.map((c, i) => (
        <motion.div
          key={c.choice_id}
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: i * 0.08, duration: 0.3, ease: 'easeOut' }}
          whileHover={{ y: -2 }}
        >
          <Button
            variant="outline"
            className="w-full h-auto min-h-[4.5rem] items-start justify-between text-left font-medium border-border hover:bg-foreground/5 hover:border-foreground/40 transition-all p-4 whitespace-normal"
            onClick={() => onSubmit(c.choice_id)}
          >
            <span>{c.text}</span>
            <ArrowRight className="w-4 h-4 text-muted-foreground flex-shrink-0" strokeWidth={1.75} />
          </Button>
        </motion.div>
      ))}
    </div>
  );
}

export default function StoryContainer(
  { StoryData }: { StoryData: StoryData }
) {
  const [currentNode, setCurrentNode] = useState(StoryData.nodes[0]);

  const handleSubmit = async (choice_id: number) => {
    try {
      const response = await fetch(`${baseUrl}/story/${StoryData.public_id}/next_node`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          previous_node_id: currentNode.node_id,
          choice_id: choice_id,
        }),
        credentials: "include",
      })
      if (response.ok) {
        const data = await response.json();
        setCurrentNode(data);
      }
    } catch (error) {
      console.error("An Error occurred", error);
    }
  }

  if (StoryData == null) {
    return (
      null
    )

  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 32 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
      className="w-full max-w-2xl"
    >
      <Card className="shadow-2xl border-border/60">
        <CardHeader className="border-b border-border/40 pb-4">
          <CardTitle className="text-xl font-bold text-foreground capitalize">
            {StoryData.title}
          </CardTitle>
        </CardHeader>

        <CardContent className="space-y-8 pt-6">
          <StoryDisplay content={currentNode.content} image={currentNode.image_url} pageNumber={currentNode.level} />

          <div>
            <p className="text-muted-foreground text-xs font-semibold uppercase tracking-widest mb-3">
              What happens next?
            </p>
            <ChoiceButtons choice={currentNode.choices} onSubmit={handleSubmit} />
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}