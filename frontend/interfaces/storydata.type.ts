export interface StoryChoice {
    text: string;
    choice_id: number;
}

export interface StoryNode {
    content: string;
    image_url: string | null;
    choices: StoryChoice[];
}

export interface StoryData {
    title: string;
    nodes: StoryNode[];
}