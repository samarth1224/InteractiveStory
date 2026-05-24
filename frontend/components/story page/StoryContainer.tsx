'use client';

import { useState, useId } from 'react';
import Image from 'next/image';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ArrowRight } from 'lucide-react';
import { StoryData, StoryNode, StoryChoice, StateVariable } from '@/interfaces/storydata.type';


const baseUrl = process.env.NEXT_PUBLIC_API_URL || "https://localhost:25000";

const THEME_RULES = [
  { keywords: ['health', 'hp', 'life'], color: 'text-[#c29d9d]' }, // Soft dusty rose
  { keywords: ['sanity', 'mind', 'mental'], color: 'text-[#bcaec7]' }, // Soft lavender
  { keywords: ['reputation', 'trust', 'respect', 'relationship'], color: 'text-[#9db3c4]' }, // Soothing steel blue
  { keywords: ['gold', 'money', 'coins', 'cash', 'credits'], color: 'text-[#d4c5a9]' }, // Warm soft sand/gold
  { keywords: ['ammo', 'bullets', 'energy', 'power'], color: 'text-[#d6ab94]' }, // Soothing warm orange/peach
  { keywords: ['alert', 'threat', 'danger', 'suspicion', 'susp'], color: 'text-[#c9988f]' }, // Muted terracotta
  { keywords: ['karma', 'morality', 'honor'], color: 'text-[#8fa89b]' }, // Soothing sage green
];

const FALLBACK_PALETTES = [
  'text-[#8fa89b]', // Sage green
  'text-[#9db3c4]', // Steel blue
  'text-[#c29d9d]', // Dusty rose
  'text-[#d4c5a9]', // Soft sand
  'text-[#c9988f]', // Terracotta
  'text-[#bcaec7]', // Lavender
  'text-[#d6ab94]', // Peach
];

const getVariableColor = (name: string) => {
  const n = name.toLowerCase();

  // 1. Try keyword matching
  const rule = THEME_RULES.find(r => r.keywords.some(k => n.includes(k)));
  if (rule) return rule.color;

  // 2. Fallback: Hash the name to pick a stable, unique dynamic color
  let hash = 0;
  for (let i = 0; i < n.length; i++) {
    hash = n.charCodeAt(i) + ((hash << 5) - hash);
  }
  const index = Math.abs(hash) % FALLBACK_PALETTES.length;
  return FALLBACK_PALETTES[index];
};

function StoryDisplay({ content, image, pageNumber, statevariable }: { content: string; image: string | null; pageNumber: number, statevariable: StateVariable[] }) {
  return (
    <div className="space-y-6">
      {/* State Variable Plain HUD */}
      {statevariable && statevariable.length > 0 && (
        <div className="flex flex-wrap gap-x-4 gap-y-2 items-center justify-start py-2 border-b border-border/40">
          <StateVariables state={statevariable} />
        </div>
      )}

      {/* Image Block */}
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

      <div className="prose prose-sm prose-invert max-w-none relative pt-2">
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

function StateVariables({ state }: { state: StateVariable[] }) {
  const baseID = useId();
  return (
    <div className="flex flex-wrap gap-x-8 gap-y-3 py-1">
      {state.map((variable, index) => {
        const colorClass = getVariableColor(variable.variable_name);

        let displayValue = String(variable.value);
        if (typeof variable.value === 'boolean') {
          displayValue = variable.value ? 'Yes' : 'No';
        }

        return (
          <motion.div
            key={`${baseID}-${index}`}
            initial={{ opacity: 0, y: 4 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: index * 0.05 }}
            className="flex items-baseline gap-3"
          >
            <span className="text-[10px] sm:text-xs font-serif tracking-[0.2em] uppercase text-muted-foreground/60 font-medium">
              {variable.variable_name.replace(/_/g, ' ')}
            </span>
            <span className={`text-lg sm:text-xl font-serif font-semibold transition-all duration-300 ${colorClass}`}>
              {displayValue}
            </span>
          </motion.div>
        );
      })}
    </div>
  );
}

function ChoiceButtons({ choice, onSubmit }: {
  choice: StoryChoice[];
  onSubmit: (choice: StoryChoice) => void;
}) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full">
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
            className="w-full h-auto min-h-[5.5rem] flex flex-col items-start justify-between border-border hover:bg-foreground/5 hover:border-foreground/45 transition-all p-4 whitespace-normal gap-3 group relative overflow-hidden"
            onClick={() => onSubmit(c)}
          >
            <div className="flex justify-between items-start w-full gap-3">
              <span className="font-medium text-foreground/90 leading-snug">{c.text}</span>
              <ArrowRight className="w-4 h-4 text-muted-foreground flex-shrink-0 transition-transform duration-300 group-hover:translate-x-1 mt-0.5" strokeWidth={2} />
            </div>

            {c.story_state_variables && c.story_state_variables.length > 0 && (
              <div className="flex flex-wrap gap-x-5 gap-y-2 w-full pt-3 border-t border-border/30">
                {c.story_state_variables.map((variable, idx) => {
                  const colorClass = getVariableColor(variable.variable_name);
                  let displayVal = String(variable.value);
                  if (typeof variable.value === 'boolean') {
                    displayVal = variable.value ? 'Yes' : 'No';
                  }

                  return (
                    <span
                      key={idx}
                      className="flex items-baseline gap-1.5 uppercase"
                    >
                      <span className="text-[9px] font-serif tracking-[0.15em] text-muted-foreground/50 font-medium">
                        {variable.variable_name.replace(/_/g, ' ')}:
                      </span>
                      <span className={`text-xs sm:text-sm font-serif font-semibold ${colorClass}`}>
                        {displayVal}
                      </span>
                    </span>
                  );
                })}
              </div>
            )}
          </Button>
        </motion.div>
      ))}
    </div>
  );
}


export default function StoryContainer(
  { StoryData }: { StoryData: StoryData }
) {
  const [nodesCache, setNodesCache] = useState<Record<string, StoryNode>>(StoryData.nodes);
  const [currentNode, setCurrentNode] = useState(Object.values(StoryData.nodes)[0]);
  const [statevariables, setStateVariables] = useState<StateVariable[]>(StoryData.state_variable_definitions);
  console.log(statevariables)

  const handleSubmit = async (choice: StoryChoice) => {
    const next_node_id = choice.next_node_id
    setStateVariables(choice.story_state_variables);

    if (nodesCache[next_node_id]) {
      setCurrentNode(nodesCache[next_node_id]);
      return
    }

    try {
      const response = await fetch(`${baseUrl}/story/${StoryData.public_id}/create_node`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          previous_node_id: currentNode.node_id,
          choice_id: choice.choice_id,
        }),
        credentials: "include",
      })
      if (response.ok) {
        const data = await response.json();
        setCurrentNode(data);
        setNodesCache((prev) => ({ ...prev, [data.node_id]: data }));
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
          <StoryDisplay content={currentNode.content} image={currentNode.image_url} pageNumber={currentNode.level} statevariable={statevariables} />
          {currentNode.choices ? (
            <div>
              <p className="text-muted-foreground text-xs font-semibold uppercase tracking-widest mb-3">
                What happens next?
              </p>
              <ChoiceButtons choice={currentNode.choices} onSubmit={handleSubmit} />
            </div>) : (
            <p className="text-muted-foreground text-center text-xs font-semibold uppercase tracking-widest mb-3">
              The End
            </p>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
}