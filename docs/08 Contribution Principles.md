# 08 Contribution Principles

## Purpose

This document describes the principles that guide all contributions to Research OS.

These principles apply equally to humans and AI assistants.

Their purpose is to ensure that Research OS evolves consistently while remaining understandable, maintainable, trustworthy and aligned with its vision.

These principles should be followed whenever changing documentation, designing new concepts, building workflows, implementing features or extending the system.

---

# 1. Documentation is the source of truth

The documentation defines how Research OS works.

Implementation should always follow the documented concepts and architecture.

If implementation and documentation diverge, update the documentation before changing the implementation.

Research OS should never evolve through code alone.

---

# 2. Preserve the conceptual model

Research OS is built around a small number of core concepts.

Whenever possible:

- extend existing concepts
- refine existing models
- improve existing workflows

Avoid introducing new concepts if an existing one already solves the problem.

A coherent system is more valuable than a collection of independent solutions.

---

# 3. Simplicity over cleverness

Prefer the simplest solution that satisfies the problem.

Avoid unnecessary abstraction.

Avoid premature optimisation.

Avoid solving problems that do not yet exist.

Simple systems are easier to understand, maintain and extend.

---

# 4. Build for understanding

Research OS exists to improve understanding.

Every contribution should make the system easier to understand.

Prioritise:

- clarity
- consistency
- explicit behaviour
- predictable workflows

Avoid hidden logic, implicit behaviour or unnecessary complexity.

---

# 5. Research integrity comes first

Research evidence is the foundation of the system.

Evidence should never be modified.

Knowledge may evolve over time, but every knowledge claim should remain traceable back to the evidence from which it originated.

Understanding can change.

Evidence should not.

---

# 6. AI is a collaborator, not the decision maker

AI exists to support researchers.

AI may:

- organise information
- extract evidence
- generate summaries
- identify patterns
- suggest improvements
- generate deliverables

AI should not silently:

- modify approved knowledge
- invent evidence
- make irreversible decisions
- replace human judgement

Human review remains an essential part of the research process.

---

# 7. Human-readable first

Research OS should remain understandable without specialised tools.

Prefer formats that are:

- human-readable
- version controllable
- easy to inspect
- durable

Whenever possible, choose transparent solutions over hidden implementations.

---

# 8. Design for evolution

Research is continuous.

Research OS should continuously improve as new evidence becomes available.

Design systems that can evolve without requiring complete redesigns or migrations.

Small incremental improvements are preferred over large rewrites.

---

# 9. Think in systems, not features

Individual features should strengthen the overall system.

Avoid solving isolated problems in ways that weaken consistency across Research OS.

Before introducing something new, ask:

- Does this fit the existing architecture?
- Does it improve the overall system?
- Will it still make sense in several years?

If not, reconsider the approach.

---

# 10. Favour long-term knowledge over short-term output

The purpose of Research OS is not to produce reports.

The purpose of Research OS is to continuously build reusable organisational knowledge.

Reports, presentations, summaries and other deliverables are valuable outputs, but they should always be generated from the underlying knowledge rather than becoming the knowledge themselves.

Every contribution should strengthen the knowledge base rather than only improving individual deliverables.

---

# 11. Keep responsibilities clear

Every component within Research OS should have a single, well-defined responsibility.

Projects organise research.

Rounds organise research activities.

Evidence captures observations.

Knowledge captures understanding.

Deliverables communicate knowledge.

Agents perform specific tasks.

Avoid overlapping responsibilities or concepts that blur these boundaries.

---

# 12. Build for reproducibility

The same inputs should produce the same outputs whenever possible.

Processes should be transparent and repeatable.

Users should always be able to understand:

- where information came from
- how it was transformed
- why a conclusion was reached

Reproducibility builds trust.

---

# Guiding Question

When making any contribution, ask:

> **Does this make Research OS a better system for continuously transforming research evidence into reusable knowledge?**

If the answer is yes, it is likely a good contribution.

If not, reconsider the approach.