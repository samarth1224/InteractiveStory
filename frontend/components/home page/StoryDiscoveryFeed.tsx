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

const mockStories = [
  {
    id: '1',
    name: 'The Obsidian Throne',
    content:
      'A fallen knight must reclaim a kingdom consumed by shadow magic. Every choice reshapes the fate of millions.',
    reads: '12.4k',
  },
  {
    id: '2',
    name: 'Echoes of Andromeda',
    content:
      "Stranded on a dying colony ship, you discover the AI navigator is hiding a terrible secret about humanity's origin.",
    reads: '8.7k',
  },
  {
    id: '3',
    name: 'The Crimson Séance',
    content:
      'A detective who speaks to the dead takes a case that blurs the line between the living and the spectral realm.',
    reads: '6.1k',
  },
  {
    id: '4',
    name: 'Song of the Wandering Sea',
    content:
      'Pirates, sirens, and ancient treasure — a young cartographer maps the unmappable edge of the world.',
    reads: '9.3k',
  },
  {
    id: '5',
    name: 'Neon Purgatory',
    content:
      'In a city that never sleeps, ghosts of the digital age haunt a hacker who can see between the signal and the soul.',
    reads: '11.0k',
  },
  {
    id: '6',
    name: 'The Glass Grimoire',
    content:
      "A bookbinder discovers every book she repairs changes reality. She must fix the one book that shouldn't exist.",
    reads: '7.8k',
  },
];

/* ── Animation variants ─────────────────────────────────────── */
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

/* ── Main Section ───────────────────────────────────────────── */
export default function StoryDiscoveryFeed() {
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
            Community Favorites
          </p>
          <h2 className="text-3xl font-bold text-foreground">Explore Stories</h2>
        </div>

        <motion.button
          whileHover={{ scale: 1.04 }}
          whileTap={{ scale: 0.97 }}
          className="px-4 py-1.5 rounded-full text-xs font-semibold border border-border bg-transparent text-muted-foreground hover:bg-foreground hover:text-background transition-colors duration-200 cursor-pointer"
        >
          Browse Stories
        </motion.button>
      </motion.div>

      {/* Story Grid */}
      <motion.div
        className="grid grid-cols-[repeat(auto-fill,minmax(320px,1fr))] gap-5"
        variants={containerVariants}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: '-40px' }}
      >
        {mockStories.map((story) => (
          <StoryCard key={story.id} story={story} />
        ))}
      </motion.div>
    </section>
  );
}

/* ── Story Card ─────────────────────────────────────────────── */
function StoryCard({ story }: { story: (typeof mockStories)[0] }) {
  return (
    <motion.div

      whileHover={{ y: -6, transition: { duration: 0.2, ease: 'easeOut' } }}
      id={`story-card-${story.id}`}
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
              <BookOpen className="w-4 h-4 text-foreground/70" strokeWidth={1.75} />
            </motion.div>

            <div className="flex items-center gap-1 text-muted-foreground text-xs ml-auto">
              <Eye className="w-3.5 h-3.5" strokeWidth={1.75} />
              <span>{story.reads} reads</span>
            </div>
          </div>

          <CardTitle className="text-base font-bold text-foreground leading-snug">
            {story.name}
          </CardTitle>
        </CardHeader>

        {/* Card Body */}
        <CardContent className="flex-1">
          <CardDescription className="text-sm leading-relaxed line-clamp-2">
            {story.content}
          </CardDescription>
        </CardContent>

        {/* Card Footer */}
        <CardFooter className="justify-between">
          <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
            <span>Interactive</span>
            <Zap className="w-3 h-3" />
            <span>AI-Powered</span>
          </div>

          <Link
            href={`/${encodeURIComponent(story.name)}`}
            id={`read-story-${story.id}`}
            className="group/link flex items-center gap-1.5 text-[0.82rem] font-semibold text-foreground no-underline hover:gap-2.5 transition-all duration-200"
          >
            Read Story
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