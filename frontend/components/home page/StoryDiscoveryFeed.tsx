'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { BookOpen, Eye, ArrowRight, Zap } from 'lucide-react';
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
  CardDescription,
} from '@/components/ui/card';
import { StoryData } from '@/interfaces/storydata.type';


// /* ── Animation variants ─────────────────────────────────────── */
const containerVariants = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const cardVariants = {
  hidden: { opacity: 0, y: 28 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.45, ease: [0.22, 1, 0.36, 1] },
  },
};

const headerVariants = {
  hidden: { opacity: 0, y: -16 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5, ease: 'easeOut' } },
};

/* ── Main Section ───────────── ──────────────────────────────── */
export default function StoryDiscoveryFeed({
  Stories = [],
  title = "Explore Stories",
  subtitle = "Community Favorites"
}: {
  Stories?: StoryData[];
  title?: string;
  subtitle?: string;
}) {
  return (
    <section id="story-discovery" className="w-full max-w-[1200px] mx-auto px-6 pb-20">
      {/* Section Header */}
      <motion.div
        className="flex items-end justify-between flex-wrap gap-4 mb-10"
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: '-60px' }}
      >
        <div>
          <p className="text-muted-foreground text-xs font-semibold tracking-widest uppercase mb-1.5">
            {subtitle}
          </p>
          <h2 className="text-3xl font-bold text-foreground">{title}</h2>
        </div>
      </motion.div>

      {/* Story Grid */}
      <motion.div
        className="grid grid-cols-[repeat(auto-fill,minmax(320px,1fr))] gap-5"
        variants={containerVariants}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: '-40px' }}
      >
        {Stories.map((story) => (
          <StoryCard key={story.public_id} story={story} />
        ))}
      </motion.div>
    </section>
  );
}

/* ── Story Card ─────────────────────────────────────────────── */
function StoryCard({ story }: { story: StoryData }) {
  return (
    <motion.div

      whileHover={{ y: -6, transition: { duration: 0.2, ease: 'easeOut' } }}
      id={`story-card-${story.public_id}`}
      className="h-full"
    >
      <Card className="h-full flex flex-col border-border/60 hover:border-foreground/30 transition-colors duration-300 hover:shadow-[0_8px_32px_rgba(0,0,0,0.18)] dark:hover:shadow-[0_8px_32px_rgba(255,255,255,0.06)]">
        {/* Card Header */}
        <CardHeader className="pb-2">
          <div className="flex items-center gap-3 mb-3">
            <motion.div
              whileHover={{ scale: 1.1, rotate: -3 }}
              transition={{ duration: 0.2 }}
              className="w-10 h-10 rounded-lg flex items-center justify-center bg-foreground/8 border border-border/60 flex-shrink-0"
            >
            </motion.div>
          </div>

          <CardTitle className="text-base font-bold text-foreground leading-snug">
            {story.title}
          </CardTitle>
        </CardHeader>

        {/* Card Body */}
        <CardContent className="flex-1">
          <CardDescription className="text-sm leading-relaxed line-clamp-2">
            Lorem Ipsum doler set, Loren Ispsum Doler Set
          </CardDescription>
        </CardContent>

        {/* Card Footer */}
        <CardFooter className="justify-between">
          <Link
            href={`/Story/view/${encodeURIComponent(story.public_id)}`}
            id={`read-story-${story.public_id}`}
            className="group/link flex items-center gap-1.5 text-[0.82rem] font-semibold text-foreground no-underline hover:gap-2.5 transition-all duration-200"
          >
            Begin Story
            <motion.span
              className="inline-flex"
              initial={{ x: 0 }}
              whileHover={{ x: 3 }}
              transition={{ duration: 0.15 }}
            >
              <ArrowRight className="w-3.5 h-3.5" strokeWidth={2} />
            </motion.span>
          </Link>
        </CardFooter>
      </Card>
    </motion.div>
  );
}