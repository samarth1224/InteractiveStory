# Interactive Story AI 

An immersive, AI-powered interactive storytelling platform. **Interactive Story** allows users to generate dynamic, branching narratives where their choices genuinely shape the world, characters, and plotline. 

This project consists of a Next.js frontend and a **FastAPI + Google Agent Development Kit (ADK) + MongoDB** backend.

---

##  Backend Architecture

The core of Interactive Story lies in its backend, which orchestrates Large Language Models (LLMs) to dynamically generate, track, and persist branching storylines in real-time.

### 1. Technology Stack
- **Framework**: FastAPI
- **Database**: MongoDB (via Beanie ODM)
- **Agent Orchestration**: Google Agent Development Kit (ADK)
- **Image Generation**: SiliconFlow (FLUX.1-schnell) with automated AWS S3 uploads.
- **Authentication**: JWT via HTTP-only cookies.

### 2. How the Story is Structured

The story generation is fundamentally modeled as a Graph of interconnected narrative nodes, guided by a master plan. 

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

---

##  API Flow summary

1. **`POST /story/create_story`**: 
   Takes a prompt. Initializes the ADK Runner. The `StoryPlanner` generates the Master Plotline and State Variables. The `NodeGenerator` yields the first node. A SiliconFlow image is generated, uploaded to S3, and the entire `Story` document is saved to MongoDB.
2. **`POST /story/{public_story_id}/create_node`**: 
   Takes the `previous_node_id` and the user's `choice_id`. Looks up the expected State Variables from the chosen path, feeds them back into the LLM, and generates the next scene. 
3. **`GET /story/stories`**: 
   Fetches all root stories associated with the authenticated User (or Guest).

---

##  Deployment
 Deployed via PM2 behind an Nginx reverse proxy managing port 8000 (Backend) and port 3000 (Frontend) on an AWS EC2 Ubuntu instance.

---

## Installation & Local Setup

### 1. Clone the repository.
```bash
git clone https://github.com/samarth1224/InteractiveStory.git
cd InteractiveStory
```

### 2. Backend Setup (FastAPI)
The backend requires Python 3.10+. Open a terminal and navigate to the project root.

```bash
cd Backend
python -m venv venv

# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Configure Environment:**
Copy the `.env.example` file to create your `.env` file, and fill in your Google GenAI, MongoDB, and SiliconFlow API keys.
```bash
cp .env.example .env
```
Key points to note:
1. Please make sure your MongoDB database is up and running.Make sure you copy connection string correctly.
2. If you do not intend to engage in hassle of acquiring API key for SiliconFlow, you can skip it, but the images will not be generated.
3. If you want to have images generated, get the SiliconFlow key than either,
 a) Leave the environment variables for AWS S3 section empty, this will directly take the link from the SiliconFlow servers(This is temporary link) 
 b) Set up AWS S3 bucket and fill in the environment variables for AWS S3 section, this will upload the images to your S3 bucket and the link will be taken from there(This is permanent link)  
4. Please Leave the **DATABASE_URL** as it points to an local instance of sqlite database which is required for ADK to store session data. You dont have to do anything for this.

**Run the Backend:**
```bash
uvicorn app.main:app --reload --port 8000
```


### 3. Frontend Setup (Next.js)
Open a *new* terminal window.
```bash
cd frontend
npm install
```

**Configure Environment:**
Copy the `.env.example` file to create your `.env.local` file.
```bash
cp .env.example .env.local
```

**Run the Frontend:**
```bash
npm run dev
```

The Interactive Story platform should now be accessible at `http://localhost:3000`!

### 4. API Contract Testing Using Specmatic (Optional)
If you want to run the Specmatic API contract tests against your live backend.

**Docker is required to run this test. Make sure your Docket engine is running**

```bash
# Make sure your backend is running, then run from the root directory:
docker run --rm -v "${PWD}:/usr/src/app" --network host specmatic/specmatic test
```

