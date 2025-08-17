# RELIC: Conceptual Framework

## 1. The Core Problem: The Crisis of Lost Context

We are not suffering from a lack of information; we are suffering from a crisis of fragmentation and lost context. Our digital lives—our knowledge, work, and decisions—are scattered across dozens of disconnected applications. This creates three critical problems:

- **Digital Amnesia:** We have access to endless information but have lost access to our own experience. We spend hours searching for a file we know we saw or trying to remember a key decision from six months ago.
- **The Broken Causal Chain:** We see the artifacts of our work (the final document) but lose the most valuable part: the process. We forget the article that sparked the idea or the conversation that changed our minds.
- **The Generic AI Paradox:** We have access to superhumanly intelligent AI, but we interact with it as if it's a stranger with no memory. Its power is fundamentally limited by its lack of personal context.

## 2. The Product Vision: A Personal Intelligence Platform

RELIC is a Personal Intelligence Platform that solves this crisis by creating a secure, unified, and queryable digital twin of your knowledge and experience. It is the foundational memory layer that integrates your existing tools and empowers both you and your AI assistants with perfect context.

The product consists of three core pillars:

- **The Unified Chronicle:** A silent ingestion engine that synthesizes the trail of your digital life—notes, readings, conversations, code—into a single, structured timeline.
- **The Causal Knowledge Graph:** RELIC's core innovation is its ability to understand not just what you know, but how you know it. By analyzing the "path of your actions," it automatically constructs a knowledge graph based on causality and intent.
- **The Personal AI Context Layer:** Through a secure API, any language model can be granted access to the context within your RELIC, transforming it from a generic tool into a stateful, personalized co-pilot.

## 3. The Ontology of Knowledge

To structure the data, RELIC uses a three-layered ontology to model human experience.

- **The Static Core:** The relatively stable aspects of your identity (personality, values, skills).
- **The Dynamic State:** Your fluctuating internal world (cognitive, emotional, and physical states).
- **The Experiential Log:** The concrete external events and actions that make up your life.

## 4. The Capture Framework

### 4.1. The Hierarchy of Intent

Instead of relying on a single data source (like a calendar or ticket system), RELIC captures intent from a hierarchy of signals, making it adaptable to any workflow.

- **Level 1: Explicit Declarations (Ground Truth):** The user explicitly states their intention (e.g., via a "Quick Log" hotkey, a calendar event, or starting a task in a ticket system). This is the highest-signal data.
- **Level 2: High-Signal Behavior (Strong Inference):** Actions that strongly imply intent, such as creating a new document or highlighting and copying text. This is the "action-path" data.
- **Level 3: Passive Patterns (Weak Inference):** The AI-driven clustering of raw activity streams to infer event boundaries (e.g., identifying a "Deep Work - Coding" block). This is the safety net that provides temporal scaffolding.

### 4.2. The "Single Funnel" PoC Workflow

To simplify the initial engineering effort, the PoC will focus on a streamlined workflow where high-intent knowledge is channeled into a few easily accessible sources.

- **Active Generation (Notes/Ideas):** All long-form writing is done in a local folder of Markdown files (e.g., using Obsidian), which can be monitored by a simple File Watcher.
- **Active Referencing (Links/Articles):** All saved links and highlights are captured via a custom Browser Extension.
- **Mobile Capture:** Mobile capture is handled by leveraging existing tools that sync with the desktop. Notes are created in the Obsidian mobile app, and links are shared to a Telegram "Saved Messages" inbox for later processing on the desktop.

## 5. The Signal Processing Engine

### 5.1. The "Attention Object"

To differentiate high vs. low signal information, RELIC avoids flat logs. For every interaction (a webpage visit, a meeting), it creates a rich "Attention Object" that combines behavioral proxies (dwell time, scroll speed) and direct interactions (highlights, notes) to calculate an Attention Score. This allows the system to understand what you truly cared about.

### 5.2. Memory Reconsolidation

RELIC is designed to be an active reconsolidation engine. When a new, high-signal event is logged, the system actively searches for related past memories. It then prompts the user to link and reframe their understanding of the past event in light of the new information, turning the RELIC from a passive archive into a dynamic system for learning and personal growth.

---

# TODO LIST RECOMMENDED

When starting a new task, it is recommended to create a todo list.

1.  Include the `task_progress` parameter in your next tool call
2.  Create a comprehensive checklist of all steps needed
3.  Use markdown format: `- [ ]` for incomplete, `- [x]` for complete

**Benefits of creating a todo list now:**

- Clear roadmap for implementation
- Progress tracking throughout the task
- Nothing gets forgotten or missed
- Users can see, monitor, and edit the plan

**Example structure:**

```markdown
- [ ] Analyze requirements
- [ ] Set up necessary files
- [ ] Implement main functionality
- [ ] Handle edge cases
- [ ] Test the implementation
- [ ] Verify results
```

Keeping the todo list updated helps track progress and ensures nothing is missed.
