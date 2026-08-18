# Research OS Blueprint v1
### A Research Operating System for Continuous UX Research

---

# Vision

Research OS is not an AI assistant.

It is an operating system that helps a UX researcher continuously build reliable knowledge over time.

The goal is not to summarize interviews.

The goal is to help researchers understand users better, preserve knowledge, support design decisions and continuously improve products.

AI is the engine.

The researcher remains the owner.

---

# Core Philosophy

## AI proposes.
Researchers decide.

Every important decision remains human.

AI may:

- organize
- synthesize
- cluster
- critique
- suggest

AI never decides what becomes truth.

---

## Evidence first

Every conclusion must be traceable.

Nothing exists without supporting evidence.

Evidence should preserve the richness of the research session before Research OS compresses it into patterns, insights or deliverables.

A 45-minute interview should not become only a few broad findings. It should first become a set of concrete, traceable observations: what the participant did, said, misunderstood, expected, compared, questioned or suggested.

Hierarchy:

Source

↓

Evidence

↓

Patterns

↓

Insights

↓

Recommendations

Deliverables may never skip these layers.

---

## Research is continuous

Research does not end after one study.

Knowledge grows across multiple research rounds.

Research OS continuously updates the current understanding while preserving historical context.

---

## Separate evidence from interpretation

Observations are facts.

Interpretations explain why those observations matter.

Recommendations are possible actions.

These are three different things.

This also means Research OS separates:

- many small Evidence observations
- fewer reviewable Findings or knowledge proposals
- even fewer Patterns and Insights

Researchers should review meaningful decisions, while still being able to inspect the richer evidence behind them.

---

## Researcher notes guide analysis

Researcher reflections are valuable.

However they are not evidence.

They provide:

- hypotheses
- context
- priorities
- intuition

AI may use them to understand direction.

AI may never use them as proof.

---

## Simplicity over features

Research OS should reduce administration.

It should never create additional work.

Whenever two solutions exist, choose the simpler one.

---

# Mental Model

Research is organised as:

Research Program

↓

Research Rounds

↓

Sources

↓

Knowledge

↓

Deliverables

A program represents an ongoing product area.

Examples:

- Fulfillment Operations
- Customer Messaging
- Internal Admin Tools

A research round represents one specific study.

Examples:

- Discovery
- Concept Test 1
- Concept Test 2
- Pilot
- Rollout Evaluation

---

# Folder Structure

Research/

Program/

0_Project/

Program.md

02-rounds/

Discovery/

Sources/

Knowledge/

Deliverables/

Concept Test 1/

Concept Test 2/

Overall Knowledge/

Templates/

AGENTS.md

---

# Sources

A research round may contain:

Interviews

Meetings

Workshops

Observations

Screenshots

Photos

Videos

Figma exports

Presentations

Documents

Researcher Notes

Researcher Notes include:

- voice reflections
- end-of-day summaries
- hypotheses
- whiteboard photos
- personal observations

---

# Processing Pipeline

Every new source automatically triggers processing.

Pipeline:

Source Added

↓

Metadata

↓

Evidence Extraction

↓

Method-specific Analysis

↓

Insight Synthesis

↓

Quality Critique

↓

Opportunity Extraction

↓

Program Comparison

↓

Knowledge Curation

↓

Current Understanding Update Proposal

The researcher reviews important changes.

Documentation is NOT generated yet.

---

# Closing a Research Round

Documentation is only created after the researcher explicitly closes the round.

Closing a round performs:

Freeze Current Understanding

↓

Generate Research Documentation

↓

Generate Presentation Preparation

↓

Generate Design & Product Recommendations (if applicable)

↓

Archive Round Knowledge

↓

Suggest Program Knowledge updates

Program knowledge is only updated after researcher approval.

---

# Knowledge Model

Research has three knowledge levels.

## 1. Current Understanding

Living.

Updated after every new source.

Contains:

- Insight Cards
- Open Questions
- Contradictions
- Opportunities
- Research Question Progress

This is the main workspace.

---

## 2. Round Knowledge

Frozen when the research round ends.

Represents what was learned during that study.

Never changes afterwards.

---

## 3. Program Knowledge

Long-term knowledge.

Builds across multiple rounds.

Tracks how insights evolve over time.

---

# Insight Cards

Insight Cards are the fundamental knowledge objects.

Everything builds on them.

Structure:

Insight

One sentence describing what was observed.

Why this matters

One sentence describing the meaning in the context of the research.

Supporting Evidence

Participant references

Quotes

Observations

Contradictions

Research Questions

Related Opportunities

Confidence

Last Updated

Research Round

Status

Needs Review / Approved / Rejected

---

# Main Insights

Main Insights are not separate objects.

They are collections of related Insight Cards.

AI proposes clusters.

The researcher decides which clusters become Main Insights.

---

# Program Insights

Program Insights connect insights across research rounds.

Example:

Discovery

↓

Concept Test 1

↓

Concept Test 2

↓

Pilot

↓

Rollout

The system shows:

- where the insight appeared
- how evidence evolved
- whether it improved
- whether it disappeared
- whether it became stronger

AI proposes matches.

The researcher confirms them.

---

# Current Understanding

This is the heart of Research OS.

It contains:

Current Main Insight Clusters

Insight Cards

Research Question Progress

Contradictions

Open Questions

Opportunities

Recent Changes

Confidence Overview

It is continuously updated.

---

# Deliverables

Research OS produces four outputs.

## 1. Current Understanding

Living knowledge.

For the researcher.

---

## 2. Research Documentation

Official documentation.

Contains:

Executive Summary

Key Insights

Key Opportunities

Detailed Findings

Evidence

Quotes

Contradictions

Reasoning

---

## 3. Presentation Preparation

Plain-text slide deck.

Each slide contains:

Slide Title

Insight

Subtitle

Impact

Evidence

Suggested Visual

Speaker Notes

This is intended as preparation for PowerPoint, Claude, Gamma or similar tools.

---

## 4. Design & Product Recommendations

Action-oriented document.

Contains:

Problem

Observed Behaviour

Evidence

Possible Recommendation(s)

Priority

Affected Flow

Related Insight Cards

Recommendations remain suggestions.

They are never presented as objective truth.

---

# Agent Architecture

## Research Planner

Reads:

Project

Method

Research Questions

Researcher Notes

Defines analysis focus.

---

## Source Intake

Processes incoming sources.

Extracts metadata.

Recognises source type.

---

## Evidence Extractor

Extracts:

Observations

Quotes

Behaviours

Context

Problems

Participant references

---

## Method Specialist

Uses different analysis strategies depending on:

Discovery

Usability

Concept Test

Workshop

Contextual Inquiry

etc.

---

## Insight Synthesizer

Creates and updates Insight Cards.

Suggests clusters.

Updates evidence.

Tracks confidence.

---

## Quality Critic

Challenges every insight.

Checks:

Evidence

Bias

Contradictions

Over-generalisation

Reasoning

Separates observations from interpretation.

---

## Opportunity Agent

Creates:

Opportunities

Design recommendations

Product recommendations

Research suggestions

---

## Program Linker

Compares current insights with previous research rounds.

Suggests links.

Never merges automatically.

---

## Knowledge Curator

The only agent allowed to update Current Understanding.

Combines outputs from all other agents.

Produces a proposed update.

---

## Deliverable Editor

Runs only after the round is closed.

Generates all deliverables.

---

# Agent Collaboration

Agents collaborate.

They may challenge each other.

If disagreements are small:

They resolve them automatically.

If disagreements remain:

They create a review item for the researcher.

Principle:

Agents resolve disagreements before involving the researcher.

---

# Research Review Philosophy

The researcher reviews changes.

Not documents.

AI proposes changes.

The researcher approves the evolution of knowledge.

---

# Future UI Vision

The future UI is centred around two concepts.

## Current Understanding

What do we currently know?

## Review Queue

What changed?

What needs researcher input?

The UI should expose process rather than implementation.

Agents remain invisible.

---

# Out of Scope (v1)

No collaboration

No permissions

No dashboards

No analytics

No databases

No chat interface

No manual coding

No complex workflow builder

Focus entirely on creating the strongest possible research backbone.

---

# Guiding Principle

Research OS should feel like working with a team of experienced researchers.

Not like operating an AI system.

The system should continuously answer one question:

**"Based on everything we know today, what is our current understanding?"**
