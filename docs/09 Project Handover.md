# 09 Project Handover

## Purpose

This document preserves project background from the original ChatGPT Classic exploration so future human and AI contributors understand the intent behind Research OS.

It is not a replacement for the Vision, Architecture, Domain Model, Knowledge Pipeline, or Contribution Principles. It is a compact handover that explains why the project exists, what must be preserved, and which areas are still open.

---

# 1. Project Overview

Research OS is an attempt to redesign how UX research is stored, organized, and reused.

The core idea is that knowledge, not documents, is the primary artifact of research.

Traditional research repositories revolve around projects, reports, presentations, and transcripts. Those documents eventually become static archives that require manual interpretation every time someone wants to reuse them.

Research OS instead models research as an evolving knowledge system where every study continuously updates an organization's understanding.

Reports, slide decks, presentations, summaries, and other deliverables are outputs generated from this knowledge. They are not the knowledge itself.

---

# 2. Original Vision

Research OS should become an AI-assisted operating system for research.

Instead of asking:

> Where is the report?

people should be able to ask:

> What do we currently know about this?

The system should:

- accumulate knowledge across projects and rounds
- preserve evidence
- make reasoning traceable
- generate research outputs on demand
- improve continuously as new evidence arrives

The long-term ambition is that research compounds instead of disappearing inside documents.

---

# 3. Problem It Solves

Current research workflows have several structural problems:

- every project starts from scratch
- findings become trapped inside reports
- evidence is difficult to trace
- insights are duplicated
- AI often summarizes documents instead of helping maintain knowledge
- researchers spend too much time producing deliverables instead of thinking

Research OS separates raw data, observations, evidence, knowledge, and deliverables so each layer can evolve independently.

---

# 4. Main Design Principles

## 4.1 Knowledge first

The knowledge system is the primary product.

Everything else is generated from it.

## 4.2 Evidence never disappears

Every conclusion should be traceable back to an interview, transcript, note, observation, screenshot, recording, or other source.

Nothing should become detached from evidence.

## 4.3 AI assists reasoning, not replaces it

AI can:

- cluster
- summarize
- detect themes
- propose hypotheses
- draft documents
- find contradictions
- link evidence

AI should not silently invent conclusions or decide what becomes accepted truth.

Human validation remains essential.

## 4.4 Documents are disposable

Reports are outputs.

Knowledge persists.

Reports can be regenerated from validated knowledge.

## 4.5 Keep durable concepts separate from implementation

Architecture documents intentionally avoid committing too early to models, frameworks, databases, UI, or APIs.

Those may change. The conceptual system should remain stable.

## 4.6 Understanding is incremental

Knowledge evolves over time.

Nothing is permanently finished.

New evidence can strengthen, weaken, refine, or invalidate previous understanding.

---

# 5. Core Concepts

The current conceptual flow is:

```text
Research Project
  -> Research Activities
  -> Evidence
  -> Observations
  -> Findings / Patterns
  -> Knowledge
  -> Deliverables
```

Research activities may include:

- interviews
- observations
- usability tests
- analytics
- surveys
- workshops

Observations are atomic statements describing what happened.

Findings and patterns combine multiple observations into recurring behavior or meaningful themes.

Knowledge is validated understanding that survives individual projects or rounds.

Deliverables are generated outputs such as:

- reports
- presentations
- summaries
- opportunity maps
- journey maps
- stakeholder decks

The important separation is:

```text
Evidence -> Observation -> Finding -> Knowledge
```

not:

```text
Transcript -> Report
```

---

# 6. Desired Workflow

The intended pipeline is:

1. A researcher creates a new project or research round.
2. Research materials are added, such as recordings, transcripts, notes, screenshots, photos, workshop exports, or documents.
3. Specialized AI agents process the raw material.
4. The researcher reviews AI output.
5. The researcher approves, edits, or rejects proposed knowledge changes.
6. Approved knowledge is added to the knowledge base.
7. Deliverables are generated from validated knowledge.

Possible agents include:

- transcript parser
- source processing agent
- observation extractor
- evidence extractor
- theme or pattern detector
- contradiction detector
- evidence linker
- insight generator
- knowledge updater
- quality critic
- deliverable generator

Agents should work independently on specialized tasks rather than relying on one monolithic prompt.

---

# 7. AI vs Researcher Responsibilities

## 7.1 AI responsibilities

AI should automate repetitive cognitive work.

AI may:

- organize files
- summarize interviews
- detect duplicate insights
- cluster observations
- link evidence
- identify contradictions
- draft findings
- generate reports
- maintain knowledge consistency

AI proposes.

AI explains.

AI traces evidence.

## 7.2 Researcher responsibilities

The researcher remains responsible for:

- framing research
- deciding significance
- validating findings
- interpreting nuance
- making trade-offs
- communicating decisions
- approving knowledge

AI should never become the final authority.

---

# 8. Important Design Decisions and Trade-Offs

## 8.1 Modular agent architecture

Decision:

Use many specialized agents instead of one giant prompt.

Reason:

- easier maintenance
- easier testing
- easier replacement
- more transparent reasoning

## 8.2 Documentation first

The current focus is research and architecture, not production implementation.

The goal is to define the conceptual system before building too much software around it.

## 8.3 Local-first development

The project currently lives locally.

Codex is used as a coding assistant.

GitHub infrastructure can come later.

## 8.4 Human approval gates

Knowledge should never automatically become truth.

Important transitions require researcher validation.

## 8.5 Stable concepts before technical commitments

Architecture documents describe enduring ideas.

Technical implementation should remain replaceable.

## 8.6 AI instructions as project documentation

AI-specific documentation is intentional. Coding agents should understand how decisions are made, not only what files to edit.

---

# 9. Things That Must Be Preserved

These are core constraints. Do not accidentally remove or collapse them.

- The knowledge model must not be reduced back into document storage.
- Evidence traceability must remain central.
- Human validation must remain required for accepted research conclusions.
- Evidence, observations, findings, knowledge, and deliverables must remain distinct concepts.
- Durable architecture must not be polluted by premature implementation details.
- Research should compound over time instead of overwriting history.
- Uncertainty, contradiction, confidence, assumptions, and open questions should remain visible.

---

# 10. Open Questions and Experimental Areas

Several important areas remain intentionally undecided.

## 10.1 Agent orchestration

Open questions include where agents live, how they communicate, how orchestration works, and how scheduling is handled.

## 10.2 Storage implementation

Storage is intentionally undecided.

Possible options include:

- markdown
- graph
- vector
- relational
- hybrid

The architecture should not depend on one storage technology yet.

## 10.3 Knowledge representation

Exact schemas are still evolving for:

- observations
- findings
- relationships
- confidence
- evidence strength
- contradictions
- assumptions
- limitations

## 10.4 Pipeline execution

Open questions include:

- manual triggers
- background execution
- incremental updates
- event-driven processing

## 10.5 Deliverable generation

Reports, presentations, and summaries are expected to be generated automatically, but the exact triggering mechanism remains open.

## 10.6 Project templates

The first end-to-end project template is still being validated.

This validation should guide future changes.

---

# 11. Current Project Status

The conceptual foundation is largely in place.

Completed documentation includes:

- Vision
- Architecture
- Research Principles
- Domain Model
- AI Agents
- Knowledge Pipeline
- Technical Specification
- Roadmap
- Contribution Principles

The current focus is not broad feature development. It is validating the workflow.

The next logical milestone is:

1. Create and validate the first real project structure.
2. Add representative research inputs.
3. Define the initial agent pipeline.
4. Run the pipeline manually.
5. Validate generated intermediate artifacts.
6. Refine the architecture based on real usage before expanding functionality.

The immediate objective is to prove that the conceptual pipeline works in practice.

Only after validating this first end-to-end flow should the system expand into richer orchestration, storage, automation, and productized interfaces.
