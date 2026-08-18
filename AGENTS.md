# AGENTS.md

## Purpose

This file gives AI coding agents the project context they need before changing Research OS.

Research OS is an AI-assisted operating system for continuous UX research. It is not a report repository, transcript summarizer, generic AI chat interface, or document generator. Its purpose is to continuously transform research evidence into structured, traceable, reusable knowledge.

Before making architectural or implementation changes, read:

- `README.md`
- `docs/00 Vision.md`
- `docs/02 Architecture.md`
- `docs/03 Domain Model.md`
- `docs/05 Knowledge Pipeline.md`
- `docs/08 Contribution Principles.md`
- `docs/09 Project Handover.md`

## Core Context

The primary artifact of research in this project is knowledge, not documents.

Reports, presentations, summaries, opportunity maps, and stakeholder decks are generated outputs. They should be derived from approved knowledge rather than treated as the knowledge itself.

The system should help researchers answer:

> What do we currently know about this?

instead of:

> Where is the report?

## Non-Negotiable Principles

- Documentation is the source of truth.
- Evidence must remain traceable to its original source.
- AI proposes, explains, structures, critiques, and drafts.
- Researchers decide what becomes accepted knowledge.
- Do not collapse evidence, observations, findings, knowledge, and deliverables into one concept.
- Preserve rich, traceable evidence before compressing it into findings, patterns, insights, or deliverables.
- Do not turn Research OS back into document storage.
- Keep durable conceptual architecture separate from replaceable implementation details.
- Preserve history, uncertainty, contradictions, rejected interpretations, and open questions.
- Prefer simple, human-readable, version-controllable formats while the system is still being validated.

## Domain Flow

The intended knowledge flow is:

```text
Source
  -> Evidence / Observation
  -> Finding / Pattern
  -> Insight / Knowledge
  -> Opportunity / Recommendation
  -> Deliverable
```

Deliverables must not skip the underlying evidence and knowledge layers.

## AI Collaboration Model

Research OS uses specialized agents rather than one monolithic prompt. Agents may process sources, extract evidence, detect patterns, synthesize insights, critique quality, update knowledge proposals, and generate deliverables.

AI-generated changes to important knowledge should go through review. Researcher approval is the gate that turns proposed understanding into accepted knowledge.

## Current Development Posture

The project is still validating its first end-to-end workflow. Favor changes that help prove the pipeline in practice before adding complex orchestration, storage, automation, or UI infrastructure.

Open areas include:

- agent orchestration
- storage implementation
- exact knowledge schemas
- pipeline execution model
- deliverable generation triggers
- project and round templates

When uncertain, refine the documentation first, then align implementation with it.
