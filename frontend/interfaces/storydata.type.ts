export interface StoryChoice {
    text: string;
    choice_id: number;
}

export interface StoryNode {
    node_id: string;
    content: string;
    image_url: string | null;
    choices: StoryChoice[];
}

export interface StoryData {
    public_id: string;
    title: string;
    nodes: StoryNode[];
}