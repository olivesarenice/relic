# RELIC PoC: Work Plan & Repository Structure

## 1. High-Level Goal

To build a functional Proof of Concept (PoC) for RELIC within 12 weeks. The PoC will focus on capturing, processing, and retrieving high-signal textual and contextual knowledge from a core set of user-defined sources. The primary outcome is to demonstrate the core value proposition: turning fragmented personal information into a queryable, intelligent knowledge graph that can be leveraged by an LLM.

## 2. Overall Repository Structure

We will use a monorepo structure to manage the various services and applications. This simplifies dependency management and ensures consistency across the platform.

```
/relic
├── .github/              # CI/CD workflows
├── apps/
│   └── web-ui/           # The user-facing web application (e.g., SvelteKit, Next.js)
├── collectors/
│   ├── browser-extension/  # The web clipper and passive logger
│   ├── file-watcher/     # Watches the local Markdown folder
│   └── service-connectors/ # Cloud functions for Calendar, Teams, etc.
├── infra/
│   ├── docker/           # Dockerfiles for services
│   └── terraform/        # Infrastructure as Code (optional for PoC)
├── packages/
│   ├── engram-model/     # Shared data model for the 'Engram' object
│   ├── db-schemas/       # SQL schemas, vector index definitions
│   └── eslint-config/    # Shared linting configurations
├── services/
│   ├── hub/              # The central ingestion API endpoint (e.g., FastAPI)
│   ├── processors/       # The data cleaning and enrichment workers
│   └── data-api/         # The internal API for querying the RELIC stores
└── README.md
```

## 3. Phased Work Plan (12 Weeks)

### Phase 1: The Backbone - Minimum Viable Capture & Storage (Weeks 1-4)

**Goal:** Establish the foundational data pipeline. At the end of this phase, we should be able to capture data from our highest-priority sources and see it structured in our database.

**Week 1: Infrastructure & Data Modeling**

- [ ] **Task:** Set up the monorepo with basic tooling (TypeScript, ESLint, Prettier).
- [ ] **Task:** Define the initial version of the Engram standard object in `/packages/engram-model`.
- [ ] **Task:** Provision the Engram Metadata DB (PostgreSQL, e.g., Supabase) and define the initial schema in `/packages/db-schemas`.
- [ ] **Task:** Deploy a basic version of the Hub service to receive and log raw data.

**Week 2: Collector 1 - The File Watcher**

- [ ] **Task:** Build the File Watcher collector for local Markdown files (e.g., in Python or Node.js).
- [ ] **Task:** It must detect new files, modified files, and deleted files.
- [ ] **Task:** It must send the file content to the Hub.

**Week 3: Collector 2 - The Browser Extension (Core)**

- [ ] **Task:** Build the skeleton of the browser extension.
- [ ] **Task:** Implement the "Active Referencing" feature: a button to clip a URL, title, and selected text, and send it to the Hub.
- [ ] **Task:** Implement the passive web activity logger (URL and active dwell time only).

**Week 4: The Processing Pipeline**

- [ ] **Task:** Set up a message queue (e.g., RabbitMQ, AWS SQS) to decouple the Hub from the Processors.
- [ ] **Task:** Build the initial Router and Cleaner services for the file and web data.
- [ ] **Task:** Ensure cleaned, standardized Engrams are being correctly saved to the PostgreSQL database.

### Phase 2: The Brain - Knowledge Enrichment & Semantic Search (Weeks 5-8)

**Goal:** Add the intelligence layer. At the end of this phase, all textual data should be searchable by meaning, not just keywords.

**Week 5: Vector Storage & Embeddings**

- [ ] **Task:** Provision the Vector Storage (e.g., Chroma, Supabase pgvector).
- [ ] **Task:** Add an "Embedding" step to the processing pipeline. Every textual Engram must be converted to a vector embedding upon creation.
- [ ] **Task:** Backfill embeddings for all data captured in Phase 1.

**Week 6: Collector 3 - The Service Connector (Teams)**

- [ ] **Task:** Build a serverless function to connect to the Microsoft Teams API.
- [ ] **Task:** Initially, it will only pull messages from a "self-chat" or designated channels.
- [ ] **Task:** Integrate this new source into the processing pipeline.

**Week 7: Enrichment Service 1 - Context Fusion**

- [ ] **Task:** Build the first enrichment service.
- [ ] **Task:** Its initial job is to perform Named Entity Recognition (NER) on all incoming text to automatically tag Engrams with people, projects, etc.
- [ ] **Task:** These tags should be saved as metadata in the PostgreSQL DB.

**Week 8: The Data API**

- [ ] **Task:** Build the internal Data API.
- [ ] **Task:** Create the first critical endpoint: a "fused search" that takes a text query, performs a vector search, and then retrieves the corresponding metadata from PostgreSQL.

### Phase 3: The Interface - Retrieval & User Interaction (Weeks 9-12)

**Goal:** Close the loop and allow a user to interact with their RELIC.

**Week 9-10: The RAG Layer & Web UI**

- [ ] **Task:** Build the RAG Layer service. It will take a user query, call the Data API to get context, and then construct a prompt for an LLM.
- [ ] **Task:** Build a minimal, functional Web UI in `/apps/web-ui`.
- [ ] **Task:** The UI will have a single input box to send a query to the RAG Layer and a display area for the streamed response.

**Week 11: The Knowledge Graph & Action Path**

- [ ] **Task:** Provision the Knowledge Graph store (e.g., Neo4j).
- [ ] **Task:** Implement the ActionPath enrichment service. Its first job is to detect simple causal links (e.g., a web highlight followed by a new note creation) and save this relationship to the graph.
- [ ] **Task:** Update the Data API to allow basic queries against the graph.

**Week 12: PoC Review & Demo Prep**

- [ ] **Task:** End-to-end testing of the entire data flow.
- [ ] **Task:** Refine the Web UI based on initial usage.
- [ ] **Task:** Prepare a compelling demo showcasing the core use cases: semantic search, question-answering, and surfacing "forgotten" knowledge.
