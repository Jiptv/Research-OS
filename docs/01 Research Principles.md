# Research Principles

> These principles define how Research OS thinks, reasons, and evolves.
> They are the foundation of every workflow, AI agent, and future feature.
>
> Whenever an implementation conflicts with these principles, the principles take precedence.

---

# Introduction

Research OS is built on a simple belief:

> Research is not about producing documents.
> Research is about building understanding.

Most research tools optimize for documentation. They help researchers create reports, presentations, or repositories of interview notes.

Research OS optimizes for something different: the continuous evolution of knowledge.

Every principle in this document exists to support that goal.

---

# 1. Knowledge over Documentation

Documentation is an output.

Knowledge is the product.

Reports, presentations and summaries are snapshots of understanding at a specific moment in time. They should never become the primary source of truth.

Research OS always prioritizes maintaining an accurate and evolving understanding over generating polished documents.

**Implications**

- Documentation is generated from knowledge.
- Documentation is never edited directly.
- Knowledge continuously evolves.

---

# 2. AI Proposes. Researchers Decide.

Artificial Intelligence should accelerate research, not replace researchers.

AI may:

- organize
- synthesize
- critique
- connect knowledge
- suggest opportunities

Researchers remain responsible for:

- interpretation
- prioritization
- decisions
- strategy

The researcher always owns the final understanding.

---

# 3. Evidence Before Interpretation

Everything starts with evidence.

No insight should exist without supporting observations.

Evidence extraction should favor research richness over premature compression. A session should first be represented as many concrete observations before Research OS turns those observations into fewer patterns, insights or recommendations.

Research OS maintains a clear hierarchy:

Source

↓

Evidence

↓

Patterns

↓

Insights

↓

Recommendations

Skipping layers weakens trust.

Every insight must be traceable back to the evidence that supports it.

---

# 4. Separate Facts from Meaning

Research contains different types of knowledge.

They should never be mixed.

## Observation

What happened.

Example:

> Five participants searched for the product image before reading the location code.

## Interpretation

Why it matters.

Example:

> Visual recognition appears to require less cognitive effort than location codes.

## Recommendation

What could improve.

Example:

> Increase the prominence of the product image.

Keeping these layers separate makes reasoning transparent.

It also protects review quality. Researchers should not be asked to approve vague summaries when the underlying research contained smaller, more concrete moments. The system should keep those moments available and ask for approval only when a finding or knowledge change is ready to be used.

---

# 5. Research is Continuous

Research is never finished.

Every study contributes to a growing understanding of a product.

New evidence may:

- strengthen an insight
- weaken it
- contradict it
- replace it
- reveal entirely new patterns

Research OS embraces this evolution rather than treating research as isolated projects.

---

# 6. Preserve Uncertainty

Not knowing something is valuable information.

Research OS should never create false certainty.

Instead it should explicitly represent:

- open questions
- conflicting evidence
- assumptions
- confidence levels
- areas requiring more research

Uncertainty guides future research.

---

# 7. Knowledge Evolves Incrementally

Understanding should grow.

It should not constantly be recreated.

Whenever possible, Research OS updates existing knowledge rather than generating completely new summaries.

This preserves continuity and allows researchers to understand how thinking changes over time.

---

# 8. Researcher Notes Are Not Evidence

Researchers often capture:

- ideas
- hypotheses
- concerns
- intuitions
- reflections

These are extremely valuable.

However:

They are guidance.

Not evidence.

Researcher Notes help AI understand what the researcher is exploring, but they should never be cited as proof.

---

# 9. Every Insight Should Be Explainable

Researchers should always be able to answer:

- Why does this insight exist?
- Which evidence supports it?
- Which participants contributed?
- How confident are we?
- What changed since last week?

Understanding should never become a black box.

---

# 10. AI Should Challenge AI

Research quality improves through critical thinking.

Different agents should review each other's work before asking the researcher for input.

Examples include:

- checking whether evidence actually supports an insight
- detecting contradictory findings
- identifying weak assumptions
- questioning over-generalizations

The goal is not agreement.

The goal is stronger understanding.

---

# 11. Current Understanding Is the Source of Truth

The primary artifact within Research OS is the Current Understanding.

Everything else is derived from it.

This means:

- reports
- presentations
- summaries
- recommendations

are generated from Current Understanding rather than maintained separately.

There should always be a single source of truth.

---

# 12. Preserve History

Knowledge changes.

History should not disappear.

Research OS should preserve:

- previous insights
- historical evidence
- outdated assumptions
- earlier recommendations

Understanding how thinking evolved is often as valuable as the current conclusion.

---

# 13. Minimize Administrative Work

Researchers should spend their time understanding users.

Not maintaining documentation.

Automation should remove repetitive work rather than introduce new workflows.

Whenever a choice exists between:

- more administration
- less administration

Research OS chooses less.

---

# 14. Surface Meaningful Change

Researchers should not review every update.

They should review meaningful changes.

Examples include:

- a new insight emerging
- confidence significantly changing
- contradictory evidence appearing
- recommendations becoming outdated

Everything else should happen automatically.

---

# 15. Recommendations Are Hypotheses

Research does not produce truth.

It produces evidence.

Recommendations should therefore be treated as hypotheses that require design, product and engineering judgement.

Research informs decisions.

It does not make them.

---

# 16. Build for the Long Term

Research knowledge becomes more valuable over time.

Every design decision within Research OS should optimize for preserving and improving knowledge over months and years rather than individual research projects.

The system should become smarter with every study.

Not simply larger.

---

# Closing Principle

The purpose of Research OS is not to automate research.

The purpose is to help researchers continuously build a trustworthy understanding of users, products and problems.

Everything else is secondary.
