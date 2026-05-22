
export interface StateVariable {
    variable_name: string;
    value: any;
}

export interface StoryChoice {
    text: string;
    choice_id: number;
    next_node_id: string;
    story_state_variables: StateVariable[];
}

export interface StoryNode {
    node_id: string;
    level: number
    content: string;
    image_url: string | null;
    choices: StoryChoice[];
}

export interface StoryData {
    public_id: string;
    title: string;
    nodes: Record<string, StoryNode>;
}