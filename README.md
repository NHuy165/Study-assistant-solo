# ABOUT THE PROJECT

This is a personal project whose target is to build an **LLM-based study assistant**. Its core features include allowing users to upload documents as context, interact with an AI chatbot and have an LLM generate study materials.

The purpose of this project is, for the most part, an **exercise** of building a full-stack website with integrated external APIs. The core idea itself was heavily inspired by **NotebookLLM**. As such, it is **not** meant to introduce any novel ideas or concepts to the market.

The main focus of the project is on the **backend** and **external API integration**, as well as communicating with the **database**. Therefore, the frontend UI is kept minimalistic on purpose to prioritize developing the backend.

All the **external APIs** and **hosting services** used in the deployed version are free and do not guarantee quality.

The Live Demo can be checked out here: [study-assistant-project-psi.vercel.app](https://study-assistant-project-psi.vercel.app)

# TECH STACK

- **Database:**
  - **PostgreSQL**
  - **Extensions:** vector, pg_trgm
- **RAG:**
  - **API calling:** Google GenAI, httpx
  - **Chunking:** Langchain
- **Backend:**
  - **Framework:** FastAPI (Python)
  - **ORM:** SQLModel (async with asyncpg)
  - **Security:** PyJWT, pwdlib (Argon2)
  - **Testing:** Pytest
- **Frontend:**
  - **Framework:** React / Typescript
  - **Advanced state management:** Zustand, TanStack Query
  - **Validation:** React hook form, Zod
  - **Styling:** DaisyUI (Tailwind CSS)
  - **E2E Testing:** Playwright
- **Environment & CI**:
  - **Containerization:** Docker
  - **CI:** Github Actions

# FEATURES

## Core features (User experience)

- **Account registration & login:** Users can **register** and **log in** using an email and password, as well as include optional **personal information** to be used in LLM-based content generation for more personalization.
- **Interactions:** Users can create **Interactions** - basically a chat room / workspace. The main app features are accessed inside an Interaction.
- **Document upload:** Users can upload documents to be processed inside an Interaction.
  - Each processed document serves as **context** to be included in future conversations.
  - Each document also comes with an automatic document analysis, which includes a **document summary**, **recommended study activities** to be generated, as well as **recommended chat prompts** to ask the chatbot.
  - Current file types include PDFs, plain text files and images (jpeg/jpg, png, webp).
- **Chatbot:** Users can hold conversations with a chatbot inside an Interaction. The deployed app version chatbot uses the **Gemini 3.1 Flash Lite** model.
- **Study activities generation:** Users can generate study activities (study material) inside an Interaction.
  - Each study activity can either be an **Exercise** type, which is graded, or a **Review** type.
  - Currently available study activities include: Multiple choice questions (Exercise), Open ended questions (Exercise), Flashcards (Review).
- **Study assessment:** Daily study assessments are generated based on the users' actions the previous day, which includes held conversations with the chatbot, uploaded documents, generated or submitted study activities.
- **Study progress:** Generated study activities and grades are aggregated and can be viewed in the home page.

## Technical architecture highlights

- **Backend:**
  - **Authentication:** Authentication system utilizing JWT for token embedding and Argon2 for password hashing.
  - **Async API:** Asynchronous endpoint logic with FastAPI and asyncpg.
  - **Validation:** User request and LLM response validation with SQLModel and Pydantic.
  - **Exception handling:** An exception handling system complete with custom exception classes, types and documentations.
  - **RAG:**
    - **Chunking:** Recursive chunking with Langchain.
    - **Embedding:** Query rewrite for better context + Vector embedding.
    - **Search:** Vector search and keyword search, facilitated by the vector and pg_trgm database extensions.
    - **Image captioning:** Allows image type document via LLM-based image captioning.
  - **Testing:** Unit tests using Pytest

- **Frontend:**
  - **Type validation:** Compile time type safety with Typescript and runtime validation with React hook form and Zod.
  - **API calling:** Utilizes TanStack Query for backend requests and server state management.
  - **Token caching:** Utilizes Zustand for security token caching.
  - **Basic UI:** Simplistic and clarity-focused UI with DaisyUI.
  - **End-to-end testing:** End-to-end testing written with Playwright.

- **Environment & CI**:
  - **Containerization:** Containerizes development and production builds, as well as test running using Docker.
  - **CI Pipeline:** Utilizes Github Actions to automatically compose production builds, run Pytest and Playwright tests on every commit.

# GETTING STARTED

## Live Demo

The live demo can be accessed at: [study-assistant-project-psi.vercel.app](https://study-assistant-project-psi.vercel.app)

**NOTE:** This live demo was hosted using a free service, as such, users may experience lag, stutter or delayed responses due to sleeping services waking up.

## Manual Installation

In case users want to install and run the application locally, follow these steps:

1. **Clone this repository**

```sh
git clone https://github.com/NHuy165/Study-assistant-solo.git
```

2. **Configure the backend .env**
   - Inside `backend/`, create a `.env` file and copy all the contents from `backend/.env.example` over.
   - Fill in the missing environment variables:
     - PRIVATE_KEY: Can be obtained by running `openssl rand -hex 32`.
     - API_KEYS_GEMINI: Navigate to [Google AI Studio](https://aistudio.google.com/) and create an API key. This variable supports multiple keys by separating them with a comma.
     - CLOUDFLARE_ACCOUNT_ID: Log into [Cloudflare Dashboard](https://dash.cloudflare.com/), navigate to **Build > Compute > Workers & Pages** to find it.
     - CLOUDFLARE_API_TOKEN: Log into [Cloudflare Dashboard](https://dash.cloudflare.com/), navigate to **Profile > API Tokens > Create Token** and create a **Workers AI** token.
     - The other variables can be left as is or modified at your own risk.
3. **Configure the frontend .env**
   - Inside `frontend/`, create a `.env` file and copy all the contents from `frontend/.env.example` over.
4. **Start the app**
   - Make sure you have **Docker** installed on your machine. If not, navigate to [docker.com](https://www.docker.com) to download.
   - Start the app by simply running `docker compose up --build` from the root directory. Subsequent builds no longer need the `--build` flag.
   - The app (frontend) can be accessed at [http://localhost:5173/](http://localhost:5173/), while the backend endpoints can be accessed at [http://localhost:8000/docs](http://localhost:8000/docs) (SwaggerUI).

# SHORTCOMINGS & FUTURE ROADMAP

- **Authentication**
  - Implement real Email Verification to ensure account authenticity during registration (currently accepts any email as long as it is format-valid).
  - Implement OAuth2 authentication to allow for third-party verification.
- **RAG**
  - Add a local LLM fallback for when the API keys in use hit their limits.
  - Support more user uploaded document types, such as .docx files.
- **Testing**:
  - Write more edge case backend and end-to-end tests to ensure code integrity.
  - Write frontend tests using Vitest to test isolated components' functionality.
  - Set up load tests with Locust to test application performance.
- **Infrastructure maintenance**
  - Implement error tracking tools (like Sentry) to monitor and alert when errors occur.
  - Utilize tools to track application performance, health and third-party APIs availability.
