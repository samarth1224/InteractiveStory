# Interactive Story AI 📖✨

An immersive, AI-powered interactive storytelling platform. **Interactive Story** allows users to generate dynamic, branching narratives where their choices genuinely shape the world, characters, and plotline. 

This project consists of a Next.js frontend and a highly sophisticated **FastAPI + Google Agent Development Kit (ADK)** backend.

---

## 🏗️ Backend Architecture

The core of Interactive Story lies in its backend, which orchestrates Large Language Models (LLMs) to dynamically generate, track, and persist branching storylines in real-time.

### 1. Technology Stack
- **Framework**: FastAPI
- **Database**: MongoDB (via Beanie ODM)
- **Agent Orchestration**: Google Agent Development Kit (ADK)
- **Image Generation**: SiliconFlow (FLUX.1-schnell) with automated AWS S3 uploads.
- **Authentication**: JWT via HTTP-only cookies.

### 2. How the Story is Structured

The story generation is fundamentally modeled as a **Directed Acyclic Graph (DAG)** of interconnected narrative nodes, guided by a master plan. 

When a user initiates a new story, the backend triggers the **`StoryPlanner` Agent**:
1. **The Bottleneck Map**: The AI acts as a Dungeon Master, outlining the overall narrative arc. It defines a "bottleneck map" which dictates the total number of levels/decisions it will take to reach a conclusion.
2. **The Branching Logic**: The AI establishes the logical constraints of the world. It sets up the initial conditions and boundaries.

Once the master plan is generated, the backend triggers the **`NodeGenerator` Agent** to construct the very first scene (`StoryNode`).

#### The `StoryNode` Object
Each step of the story is encapsulated in a `StoryNode`, which contains:
- **`content`**: The descriptive narrative text.
- **`image_url`**: A dynamically generated image illustrating the scene (stored in S3).
- **`choices`**: A list of `Choice` objects that the user can select from.

---

## 🔀 The Choice & State Variable System

What makes this engine unique is that choices do not simply jump to a static piece of text—they actively mutate the world's **State Variables**.

### Understanding State Variables
During the initial planning phase, the `StoryPlanner` generates a list of dynamic `StateVariable` definitions (e.g., `Hero_Health: 100`, `Has_Ancient_Key: False`, `Kingdom_Tension: 50`).

### How Choices Affect State
When the `NodeGenerator` generates a `StoryNode`, it explicitly calculates the consequence of every single choice it offers. 

Inside a `Choice` object:
- **`text`**: What the user sees (e.g., "Attack the dragon!").
- **`next_node_id`**: A unique ID linking to the future outcome.
- **`story_state_variables`**: An updated snapshot of the world's state variables *if* this choice is selected.

**Example Flow**:
1. User is at **Node A**. The `Kingdom_Tension` is currently `50`.
2. The user selects **Choice 2**: "Insult the King."
3. The backend receives the request. It looks at the `Choice 2` object, which specifically dictates that `Kingdom_Tension` must change to `80`.
4. The backend packages this new updated state (`Kingdom_Tension: 80`) alongside the user's action and feeds it back into the **`NodeGenerator` Agent**.
5. The LLM processes the new constraint and generates **Node B**. Because the tension is now `80`, the AI alters its tone, generates a hostile scenario, and creates new choices reflecting the consequences of the user's past actions.

This recursive loop ensures infinite, logically consistent replayability.

---

## 🚀 API Flow summary

1. **`POST /story/create_story`**: 
   Takes a prompt. Initializes the ADK Runner. The `StoryPlanner` generates the Master Plotline and State Variables. The `NodeGenerator` yields the first node. A SiliconFlow image is generated, uploaded to S3, and the entire `Story` document is saved to MongoDB.
2. **`POST /story/{public_story_id}/create_node`**: 
   Takes the `previous_node_id` and the user's `choice_id`. Looks up the expected State Variables from the chosen path, feeds them back into the LLM, and generates the next scene. 
3. **`GET /story/stories`**: 
   Fetches all root stories associated with the authenticated User (or Guest).

---

## 🔒 Security & Deployment

- **Environment**: All secrets (JWT, AWS, MongoDB URIs) are strictly loaded via `.env`.
- **CORS**: Dynamically parsed to allow cross-origin requests from the specified frontend.
- **Production**: Deployed via `ecosystem.config.js` (PM2) behind an Nginx reverse proxy managing port 8000 (Backend) and port 3000 (Frontend) on an AWS EC2 Ubuntu instance.
