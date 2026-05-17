'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Textarea } from '../ui/textarea';
import { motion } from 'framer-motion';
import { Send } from 'lucide-react';
import { useAuth } from '@/lib/auth-context';

export default function StoryCreationContainer() {
  const [input, setInput] = useState('');
  const { user } = useAuth();
  const router = useRouter();

  const charCount = input.length;
  const maxChars = 300;

  const handleSubmit = () => {
    if (charCount === 0) return;

    // If not authenticated, redirect to login
    if (!user) {
      router.push('/auth/login');
      return;
    }

    router.push(`/Story/${encodeURIComponent(input)}`);
  };

  return (
    <section id="story-creation" className="w-full max-w-4xl mx-auto px-6 mt-24">
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ type: 'spring', stiffness: 90, damping: 18 }}
        className="w-full max-w-2xl mx-auto"
      >
        <Card className="bg-transparent border-none shadow-none">
          <CardHeader className="pb-8">
            <CardTitle className="text-4xl md:text-5xl font-extrabold tracking-tight text-foreground flex items-center justify-center">
              Begin Your Story
            </CardTitle>
          </CardHeader>

          <CardContent className="px-0">
            <div className="relative border border-border/80 rounded-2xl bg-background/50 focus-within:ring-1 focus-within:ring-foreground/30 focus-within:border-foreground/30 transition-all shadow-sm">
              <Textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                maxLength={maxChars}
                placeholder="Describe your world, character, or opening scene..."
                className="resize-none h-40 text-[0.95rem] leading-relaxed border-0 focus-visible:ring-0 focus-visible:ring-offset-0 bg-transparent p-5 pb-14 w-full shadow-none"
              />

              <div className="absolute bottom-3 right-3 flex items-center gap-4">
                <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                  <Button
                    onClick={handleSubmit}
                    className="h-8 w-8 rounded-md p-0 bg-foreground text-background hover:bg-foreground/90 flex items-center justify-center"
                    disabled={charCount === 0}
                    title="Generate Story"
                  >
                    <Send className="w-3.5 h-3.5 ml-px" strokeWidth={2.5} />
                  </Button>
                </motion.div>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </section>
  );
}