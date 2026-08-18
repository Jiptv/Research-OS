# Knowledge Pipeline

> This document defines the knowledge pipeline of Research OS.
>
> It describes how raw research material enters the system, how it is transformed into traceable Evidence and interpreted knowledge, how Current Understanding changes over time, and how researchers remain in control of meaningful decisions.
>
> The pipeline connects the concepts defined in:
>
> - `01 Research Principles.md`
> - `02 Architecture.md`
> - `03 Domain Model.md`
> - `04 AI Agents.md`

---

# Part I — Foundations

## 1. Purpose

The Knowledge Pipeline describes **how knowledge flows through Research OS**.

The previous documents define:

- why the system exists
- the architectural concepts
- the domain model
- the responsibilities of each AI agent

This document explains **how those pieces work together over time**.

It describes how research moves through the system from the moment a researcher uploads a Source until new knowledge becomes part of Program Knowledge.

The pipeline transforms:

```text
Raw Research Material
        ↓
Source
        ↓
Source Representation
        ↓
Evidence
        ↓
Pattern
        ↓
Insight Card
        ↓
Recommendation
        ↓
Current Understanding
        ↓
Opportunity
        ↓
Recommendation
        ↓
Round Knowledge
        ↓
Program Knowledge
        ↓
Deliverables
```

Research OS has two intake scopes:

```text
Project-level input
        ↓
Project Source
        ↓
Source Representation
        ↓
Project Context Proposal
        ↓
Researcher Decision
        ↓
Project Context
        ↓
Future Research Context
```

```text
Round-level input
        ↓
Round Source
        ↓
Source Representation
        ↓
Evidence
        ↓
Pattern
        ↓
Insight Card
        ↓
Recommendation
        ↓
Current Understanding
```

Both scopes use the same traceability rules, but they produce different
knowledge objects by default.

Unlike many AI workflows, this is **not** a sequence of prompts.

It is a governed knowledge process.

Every stage has:

- a clear purpose
- defined inputs
- defined outputs
- quality rules
- ownership
- review requirements
- traceability requirements

The goal is not to automate research.

The goal is to make research knowledge:

- continuous
- explainable
- trustworthy
- reusable
- reviewable

---

## 2. Design Principles

The Knowledge Pipeline follows several principles.

### 2.1 Research is transformed in stages

Research should not move directly from transcript to conclusions.

Instead, understanding develops through explicit transformations.

```text
Source
    ↓
Evidence
    ↓
Patterns
    ↓
Insights
    ↓
Recommendations
    ↓
Understanding
```

Each stage exists because it represents a different level of abstraction.

Separating these stages makes reasoning inspectable.

---

### 2.2 Quality gates protect stage transitions

Each transition should have lightweight quality gates that make likely AI gaps
visible before knowledge moves downstream.

Quality gates should flag, but not decide:

- Evidence without source traceability, timestamp or useful snippet
- Evidence that combines too many observations
- Patterns with too little supporting Evidence
- Patterns or Insights without assessed contradictions
- Insights without assumptions or open questions
- Patterns, Insights or Recommendations that are too compressed to stand alone
- Recommendations without both `What we learned` and `What we should do`
- Review items without a clear `Helps us understand` field

Quality gates are not a replacement for researcher review. They make review
more focused by showing where Research OS may have skipped context, overreached
or failed to preserve evidence.

---

### 2.3 Knowledge grows incrementally

Research OS assumes that knowledge evolves.

Whenever a new Source is processed, the system should ask:

> What is the smallest meaningful change this Source introduces?

Possible answers include:

- no change
- additional supporting Evidence
- stronger confidence
- weaker confidence
- new contradiction
- refined applicability
- updated Insight
- new Insight
- updated Recommendation
- new Recommendation

The system should **not** regenerate every summary whenever a new interview is added.

---

### 2.4 Evidence always comes before interpretation

The pipeline first determines:

> What happened?

Only afterwards does it ask:

> What does that mean?

This prevents AI from presenting interpretations as observations.

---

### 2.4 Every conclusion remains traceable

Every important conclusion should be traceable backwards.

```text
Recommendation
    ↓
Opportunity
    ↓
Insight
    ↓
Evidence
    ↓
Source
```

Researchers should never need to guess why the system believes something.

---

### 2.5 Recommendations translate knowledge into action

Recommendations are a living synthesis layer before Outputs.

They answer:

```text
What did we learn?
        ↓
What should we do?
```

Recommendations may propose changes to the concept, prototype, product,
workflow, experiment strategy, communication, adoption approach or follow-up
research.

They may derive from accepted Insights, Patterns or Evidence. One strong,
traceable Evidence item may be enough when it reveals an important concept or
workflow issue.

Recommendations remain hypotheses. They should be concrete and actionable, but
they should not pretend to be final product decisions.

Every Recommendation must be understandable on its own. It should not only say
that something should be clearer or better; it should state what was unclear,
useful, risky or actionable.

---

### 2.6 Uncertainty is preserved

Uncertainty discovered early in the pipeline should remain visible.

For example:

```text
Low-quality transcript
        ↓
Uncertain Evidence
        ↓
Lower confidence Insight
        ↓
Visible limitation
```

Research OS should never convert uncertain information into confident knowledge simply because it has passed through several processing stages.

---

### 2.6 AI proposes

AI agents continuously propose changes.

Researchers decide which changes become official research knowledge.

---

### 2.7 Knowledge is never silently rewritten

Whenever understanding changes, Research OS records:

- what changed
- why it changed
- what caused the change
- who approved it
- what existed before

Knowledge evolves through explicit revisions.

---

## 3. Pipeline Overview

The complete conceptual pipeline is:

```text
Research Planning
        ↓
Source Intake
        ↓
Source Processing
        ↓
Evidence Extraction
        ↓
Method Interpretation
        ↓
Pattern Detection
        ↓
Insight Synthesis
        ↓
Quality Critique
        ↓
Knowledge Curation
        ↓
Meaningful Change Detection
        ↓
Review Queue
        ↓
Researcher Decision
        ↓
Current Understanding
        ↓
Round Closure
        ↓
Program Knowledge
        ↓
Deliverables
```

Not every Source passes through every stage in exactly the same way.

For example:

- importing an old report may skip transcription
- survey data may use different extraction logic than interviews
- workshop outputs require different method interpretation than usability tests

The overall architecture remains identical.

---

## 4. Pipeline Layers

Rather than thinking of the pipeline as one long chain, it is helpful to divide it into six conceptual layers.

### Layer 1 — Intake

Responsible for bringing research material into the system.

Produces:

- Sources
- Source metadata
- Source Representations

Project-level intake also produces Project Context proposals rather than
Evidence by default.

---

### Layer 2 — Evidence

Responsible for turning Sources into structured observations.

Produces:

- Evidence
- Quotes
- Method Assessments
- Patterns

---

### Layer 3 — Knowledge

Responsible for interpreting Evidence.

Produces:

- Insight Cards
- Confidence
- Contradictions
- Open Questions
- Current Understanding

---

### Layer 4 — Action

Responsible for translating understanding into future action.

Produces:

- Opportunities
- Recommendations

---

### Layer 5 — Governance

Responsible for ensuring trustworthy knowledge.

Produces:

- Review Items
- Decision Records
- Change Records

---

### Layer 6 — Publishing

Responsible for creating durable outputs.

Produces:

- Round Knowledge
- Program Knowledge
- Deliverables

---

## 5. Continuous Processing

Research OS assumes research never truly stops.

Instead of thinking in projects:

```text
Research
    ↓
Report
    ↓
Done
```

Research OS thinks in continuous learning.

```text
New Source
      ↓
Pipeline
      ↓
Current Understanding updated
      ↓
Research continues
```

Researcher review decisions are part of this loop. When a researcher chooses
`Needs changes`, `No`, or writes notes on `Yes`, Research OS should capture that
as feedback. Feedback can become reviewable Looped Learning suggestions. Once
accepted, those learnings become active instructions that future Codex/Cowork
runs must read before processing new sources, evidence, patterns, insights or
deliverables.

Whenever a Source arrives, the pipeline starts again.

Only the affected knowledge should be reconsidered.

For example:

```text
Interview 12 added

↓

Existing Insight gains one supporting Evidence object

↓

Confidence increases

↓

No researcher review required
```

Or:

```text
Interview 12 contradicts existing Insight

↓

Contradiction created

↓

Confidence decreases

↓

Review Item generated
```

This incremental model allows Research OS to support long-running research programs without constantly rebuilding knowledge from scratch.

---

## 6. Processing Modes

The pipeline supports three processing modes.

### 6.1 Immediate Processing

Runs automatically after a new Source is uploaded.

Typical tasks:

- transcription
- metadata extraction
- Evidence extraction
- Pattern updates

---

### 6.2 Incremental Knowledge Update

Runs whenever new Evidence is accepted.

Typical tasks:

- update Insights
- adjust confidence
- update Current Understanding
- detect meaningful changes

---

### 6.3 Full Knowledge Reassessment

Runs only when explicitly requested or when major structural changes occur.

Examples:

- merging Research Rounds
- importing historical research
- major changes to Research Questions
- large retrospective analysis

Full reassessment should be rare.

The default behaviour is incremental updating.

---

## 7. Pipeline States

Every processing task moves through a consistent lifecycle.

```text
Queued
    ↓
Running
    ↓
Completed
```

Alternative paths include:

```text
Queued
    ↓
Running
    ↓
Needs Review
```

or

```text
Queued
    ↓
Running
    ↓
Failed
```

or

```text
Queued
    ↓
Cancelled
```

Processing state is independent of research status.

For example:

A Research Round may be **Active**, while a transcript is still **Processing**.

---

## 8. Processing Boundaries

Each pipeline stage has clear boundaries.

A stage should complete only the work it is responsible for.

For example:

| Stage | May Do | Must Not Do |
|---------|---------|-------------|
| Source Intake | Classify Sources | Interpret research |
| Evidence Extraction | Create Evidence | Create Insights |
| Pattern Detection | Group Evidence | Explain behaviour |
| Insight Synthesis | Interpret Evidence | Approve knowledge |
| Knowledge Curation | Update Current Understanding | Change Sources |
| Deliverable Generation | Produce reports | Change underlying knowledge |

This separation is fundamental to the architecture.

It keeps every transformation explainable, reviewable and replaceable.

---

## 9. The Pipeline Philosophy

The Knowledge Pipeline is based on one central idea:

> **Knowledge is not generated in one step. It is cultivated through many small, transparent transformations.**

Each stage contributes something unique.

Each stage leaves an audit trail.

Each stage can be improved independently.

Together they create a research system in which:

- Sources remain trustworthy.
- Evidence remains reusable.
- Insights remain explainable.
- Knowledge evolves safely.
- Researchers remain in control.

---

# Part II — Source Intake Pipeline

## 10. Overview

The Source Intake Pipeline is responsible for transforming incoming research material into structured, processable Sources.

Its responsibility is **not** to understand the research.

Instead, it prepares research material so that later stages can process it consistently.

The output of this stage is a set of validated Source objects and their corresponding Source Representations.

```text
Uploaded Material
        ↓
Validation
        ↓
Classification
        ↓
Metadata Enrichment
        ↓
Privacy & Governance Checks
        ↓
Source Creation
        ↓
Processing Plan
        ↓
Source Processing
```

---

## 11. Trigger Events

The Source Intake Pipeline starts whenever new research material enters the system.

Typical trigger events include:

- researcher uploads an interview recording
- researcher uploads a transcript
- researcher uploads observation notes
- researcher uploads workshop results
- researcher imports historical research
- researcher imports survey data
- researcher imports screenshots
- researcher imports product documentation
- researcher imports usability recordings
- researcher creates Researcher Notes

The trigger itself does not determine how the Source will be processed.

That decision happens during classification.

---

## 12. Intake Responsibilities

The Source Intake Pipeline has six primary responsibilities.

### 12.1 Validate the upload

The system verifies that:

- the file can be read
- the format is supported
- the upload completed successfully
- corruption is detected where possible
- duplicate uploads are identified

If validation fails, the pipeline stops.

---

### 12.2 Create a Source

Every uploaded item becomes exactly one Source.

Examples:

```text
Interview Recording
↓

Source
```

```text
Transcript PDF
↓

Source
```

```text
Observation Notes

↓

Source
```

A Source should never be skipped.

Everything entering the system should first become a Source.

---

### 12.3 Classify the Source

The Source Intake Agent determines:

- Source Type
- Source Role
- likely research method
- language
- media type
- required processing

Example:

```text
Interview.mp3

↓

Source Type:
Audio

Source Role:
Primary Research

Method:
Interview

Language:
English

Required Processing:
- transcription
- speaker separation
- evidence extraction
```

---

### 12.4 Collect metadata

Where available, the pipeline records metadata such as:

- upload date
- collection date
- researcher
- participant IDs
- Research Round
- recording location
- device
- language
- interviewer
- moderator
- study
- consent information

The goal is to enrich the Source without modifying its content.

---

### 12.5 Determine processing strategy

Not every Source requires the same downstream workflow.

Examples:

| Source | Processing |
|---------|------------|
| Audio interview | Transcription → Evidence |
| Transcript | Evidence |
| Screenshot | Vision description → Evidence |
| Survey | Structured extraction |
| Observation notes | Evidence |
| Presentation | Document parsing |
| Historical report | Document extraction + contextual linking |

The processing strategy is attached to the Source.

---

### 12.6 Protect the Source

Before further processing begins, governance checks determine:

- access restrictions
- consent restrictions
- sensitive content
- export limitations
- retention policies

Later agents inherit these restrictions automatically.

---

## 13. Source Classification

Correct classification is important because it determines the rest of the pipeline.

Classification happens along several dimensions.

### 13.1 Source Type

Possible Source Types include:

- Audio
- Video
- Transcript
- Image
- Screenshot
- Observation Notes
- Survey
- Workshop Output
- Spreadsheet
- Presentation
- Document
- Researcher Note
- Imported Knowledge

Future Source Types can be added without changing the pipeline.

---

### 13.2 Source Role

The Source Role determines how the Source should be interpreted.

Typical roles include:

- Primary Research
- Supporting Context
- Product Documentation
- Operational Documentation
- Historical Research
- Research Guidance
- Project Context
- Stakeholder Context
- Prior Research Context

This distinction is important because not every Source produces Evidence in the same way.

For example:

A Product Specification may inform context.

It should not automatically become user Evidence.

A stakeholder interview, meeting recording, product framework or strategy deck
may inform Project Context.

It should not automatically become Round Evidence, even when it contains strong
opinions or claims. Those claims should be labelled as stakeholder context,
organizational context, assumptions or imported prior research until reviewed.

---

### 13.3 Method Detection

Where possible the pipeline identifies the research method.

Examples include:

- Interview
- Field Observation
- Usability Test
- Survey
- Diary Study
- Workshop
- Analytics Export
- Mixed Method

Method detection helps the Method Specialist later in the pipeline.

---

## 14. Source Validation

Every Source passes validation before processing.

Validation answers questions such as:

- Can the file be opened?
- Is the encoding readable?
- Does the upload appear complete?
- Is audio duration valid?
- Is the transcript empty?
- Are timestamps corrupt?
- Does the document contain readable text?

If validation fails:

```text
Source

↓

Validation Failed

↓

Processing stops

↓

Researcher notified
```

No downstream processing should continue.

---

## 15. Duplicate Detection

Researchers often upload multiple versions of the same material.

Research OS should detect:

### Exact duplicates

Example:

The same recording uploaded twice.

These may be merged safely at the metadata level while preserving upload history.

---

### Near duplicates

Example:

```text
Transcript v1

Transcript v2
```

These require researcher review.

The system should never silently replace one Source with another.

---

### Related Sources

Examples:

- interview recording
- transcript
- translated transcript
- observation notes

These should become separate Sources that are explicitly linked.

---

## 16. Metadata Enrichment

Metadata enrichment adds useful information without changing Source content.

Examples include:

### Language

```text
English
```

---

### Duration

```text
34 minutes
```

---

### Number of speakers

```text
2
```

---

### Recording quality

```text
High
```

---

### Upload origin

```text
Imported from Zoom
```

---

### Associated Research Round

```text
Fulfillment Operations

Round 5
```

---

Metadata enrichment should remain reversible.

Researchers should always be able to distinguish:

- original metadata
- inferred metadata
- manually edited metadata

---

## 17. Privacy Checks

Before processing continues, the Privacy & Governance Agent performs an initial assessment.

Possible checks include:

- participant names
- email addresses
- phone numbers
- faces
- addresses
- sensitive identifiers
- confidential business information

The goal is **not** to block research.

The goal is to ensure later agents know which restrictions apply.

For example:

```text
Source

↓

Contains personal information

↓

Evidence Extraction allowed

↓

Export restricted
```

---

## 18. Processing Plan

At the end of intake, every Source receives a processing plan.

Example:

```text
Source

↓

Process:

1. Transcribe
2. Separate speakers
3. Translate
4. Extract Evidence
5. Run Method Assessment
6. Detect Patterns
```

Another example:

```text
Survey Export

↓

Process:

1. Parse spreadsheet
2. Normalize answers
3. Extract quantitative Evidence
4. Compare segments
```

The plan determines the workflow.

It is not yet the workflow execution.

---

## 19. Output of the Intake Pipeline

When intake is complete, the pipeline has produced:

- validated Source
- metadata
- Source classification
- Source role
- research method
- processing plan
- governance restrictions
- processing status

No research understanding has been created yet.

At this point, Research OS knows:

- what the Source is
- where it belongs
- how it should be processed

It does **not** yet know what the Source means.

---

## 20. Invariants

The Source Intake Pipeline follows several invariants.

### Source invariant

Every uploaded research artifact becomes a Source.

---

### Immutability invariant

Original Source content is never modified.

---

### Classification invariant

Every Source has exactly one primary Source Type.

---

### Processing invariant

Every Source receives a processing strategy before downstream agents begin.

---

### Governance invariant

Access restrictions are established before any AI interpretation begins.

---

### Traceability invariant

Everything produced later in the pipeline must remain traceable back to the Source created during intake.

---

## 21. Summary

The Source Intake Pipeline prepares research material for analysis.

It answers the questions:

- What is this?
- Where does it belong?
- How should it be processed?
- Which restrictions apply?
- Is it safe to continue?

It intentionally does **not** answer:

- What happened?
- What does it mean?
- What should change?

Those questions belong to the next stages of the Knowledge Pipeline.

---

# Part III — Source Processing Pipeline

## 22. Overview

The Source Processing Pipeline transforms validated Sources into structured Source Representations.

Unlike the Source Intake Pipeline, which determines **what a Source is**, this stage determines **how the Source can be understood by both humans and AI**.

The output is not research knowledge.

It is a structured representation of the original material that preserves its meaning while making it easier to search, reference and process.

```text
Validated Source
        ↓
Source Processing
        ↓
Source Representation
        ↓
Evidence Extraction
```

The Source itself remains unchanged.

Everything produced during processing is linked back to the original Source.

---

## 23. Responsibilities

The Source Processing Pipeline has five primary responsibilities.

### 23.1 Preserve information

The first responsibility is preservation.

Processing should never lose important information that exists in the original Source.

Whenever uncertainty exists, the uncertainty should be recorded rather than removed.

For example:

```text
Unclear speech

↓

[inaudible]
```

is preferable to:

```text
Invented sentence
```

---

### 23.2 Increase accessibility

Many research artifacts are difficult to work with directly.

Examples include:

- audio recordings
- video
- photographs
- handwritten notes
- long documents

Processing converts these into representations that can be searched, referenced and analysed.

---

### 23.3 Standardize formats

Different Sources should eventually produce comparable representations.

For example:

```text
Interview transcript
```

and

```text
Observation notes
```

should both become structured text that later stages can analyse consistently.

---

### 23.4 Preserve structure

Processing should preserve meaningful structure whenever possible.

Examples include:

- timestamps
- speakers
- chapters
- slide boundaries
- table structure
- observation sequence
- page numbers

Structure often contains important research context.

---

### 23.5 Preserve provenance

Every element in a Source Representation should remain traceable to the original Source.

For example:

```text
Evidence

↓

Transcript

↓

Timestamp

↓

Audio Recording
```

This traceability allows researchers to inspect original context whenever necessary.

---

## 24. Source Representations

A Source Representation is a processed version of a Source that is easier to work with while remaining faithful to the original.

A single Source may produce multiple representations.

For example:

```text
Interview Recording

↓

Transcript

↓

Translated Transcript

↓

Speaker Timeline

↓

Topic Segments
```

Each representation serves a different purpose.

None replaces the original Source.

---

## 25. Processing by Source Type

Different Source Types require different processing strategies.

### Audio

Typical outputs:

- transcript
- timestamps
- speaker segmentation
- confidence scores
- language detection

---

### Video

Typical outputs:

- transcript
- speaker segmentation
- visual event descriptions
- timestamp alignment
- scene changes

---

### Documents

Typical outputs:

- extracted text
- heading hierarchy
- tables
- lists
- figures
- page references

---

### Presentations

Typical outputs:

- slide structure
- speaker notes (if available)
- extracted diagrams
- screenshots
- text content

---

### Images

Typical outputs:

- visual description
- detected interface elements
- detected products
- OCR text
- layout description

---

### Observation Notes

Typical outputs:

- normalized formatting
- chronological events
- observation segments
- referenced participants

---

### Surveys

Typical outputs:

- normalized responses
- structured questions
- participant metadata
- quantitative datasets

---

## 26. Transcription

Transcription converts spoken language into written language.

The goal is fidelity rather than readability.

Researchers can improve readability later if necessary.

The transcript should preserve:

- wording
- pauses where meaningful
- uncertainty
- speaker changes
- timestamps

The transcript should not silently:

- summarize
- interpret
- remove repetition
- improve grammar
- rewrite participant language

---

### Example

Original speech:

> "Yeah... I kind of looked there first... because... I don't know... it just felt easier."

Preferred transcript:

```text
Yeah... I kind of looked there first... because... I don't know... it just felt easier.
```

Not:

```text
The participant said the interface was easier.
```

The second version is already an interpretation.

---

## 27. Speaker Identification

Where possible, speakers should be separated.

Example:

```text
Interviewer

Participant
```

rather than:

```text
Speaker 1

Speaker 2
```

When identities are uncertain, confidence should be recorded.

For example:

```text
Speaker:
Unknown

Confidence:
Low
```

Incorrect certainty is worse than explicit uncertainty.

---

## 28. Translation

Translation creates an additional representation.

It never replaces the original language.

For example:

```text
Arabic transcript

↓

English translation
```

Both representations remain available.

Researchers should always be able to inspect the original wording.

This is particularly important for:

- emotions
- idioms
- culturally specific expressions
- ambiguity

---

## 29. OCR and Text Extraction

Many research artifacts contain embedded text.

Examples include:

- screenshots
- whiteboards
- workshop photos
- presentation slides
- sticky notes

The pipeline should extract this text while preserving where it appeared.

For example:

```text
Page 4

↓

Heading

↓

Paragraph

↓

Image Caption
```

rather than one large block of text.

---

## 30. Visual Description

Images often contain information that is not represented by text alone.

The pipeline may generate structured descriptions such as:

```text
A shopper is standing in front of a shelving aisle.

The highlighted product is located on the third shelf from the bottom.

The shopper is looking at the product image on the handheld device.
```

Descriptions should remain factual.

They should avoid interpretation.

Good:

```text
The participant looked at the screen.
```

Not:

```text
The participant was confused.
```

Confusion requires evidence beyond posture alone.

---

## 31. Segmentation

Long Sources should be divided into meaningful sections.

Segmentation improves:

- retrieval
- Evidence extraction
- traceability
- researcher navigation

Examples include:

### Interview

```text
Introduction

↓

Task 1

↓

Task 2

↓

Reflection
```

---

### Workshop

```text
Problem framing

↓

Idea generation

↓

Prioritization
```

---

### Presentation

```text
Slide 1

↓

Slide 2

↓

Slide 3
```

Each segment remains linked to the original Source.

---

## 32. Confidence Recording

Processing quality should be explicit.

Examples include:

| Element | Confidence |
|----------|------------|
| Speech recognition | High |
| Speaker separation | Medium |
| OCR | Low |
| Translation | High |

Later pipeline stages may use this information when assessing Evidence quality.

Confidence should never be hidden.

---

## 33. Failure Handling

Processing may fail partially.

Examples:

```text
Audio corrupted
```

```text
OCR unreadable
```

```text
Translation unavailable
```

Rather than failing the entire pipeline, the system should continue whenever possible.

Example:

```text
Transcript

✓ Complete

Visual extraction

✗ Failed
```

Downstream agents receive both results.

---

## 34. Source Representation Versioning

Representations may improve over time.

Examples:

```text
Transcript v1

↓

Transcript v2
```

or

```text
Translation updated
```

The pipeline should preserve:

- previous versions
- processing agent
- model version
- timestamp
- reason for replacement

Researchers should be able to reproduce earlier analyses if necessary.

---

## 35. Output of the Source Processing Pipeline

At the end of processing, the system has created one or more Source Representations.

Examples include:

- transcript
- translated transcript
- visual description
- extracted document text
- structured survey data
- OCR text
- segmented interview
- speaker timeline

No research conclusions have been produced.

The pipeline has only made the Source easier to understand and process.

---

## 36. Invariants

The Source Processing Pipeline follows several invariants.

### Preservation invariant

Processing never replaces the original Source.

---

### Fidelity invariant

Representations should remain as faithful as possible to the original material.

---

### Traceability invariant

Every representation must link back to the originating Source.

---

### Structure invariant

Important structural information should be preserved whenever possible.

---

### Transparency invariant

Uncertainty introduced during processing must remain visible.

---

### Interpretation invariant

Processing may describe.

Processing may not interpret.

Interpretation begins in the Evidence Pipeline.

---

## 37. Summary

The Source Processing Pipeline transforms raw research material into structured representations that are suitable for analysis.

Its responsibility is not to determine meaning.

Instead, it prepares high-quality representations that preserve:

- fidelity
- provenance
- structure
- uncertainty

These representations become the foundation for the next stage of the Knowledge Pipeline:

**Evidence Extraction**, where observations are identified for the first time.

---

# Part IV — Evidence Pipeline

## 38. Overview

The Evidence Pipeline is the first stage in which Research OS begins to understand research.

Until this point, the system has only prepared Sources.

Now it begins identifying observations that may contribute to research knowledge.

The purpose of this stage is deliberately narrow.

It answers:

> **What was observed, stated or measured?**

It does **not** answer:

> **Why did it happen?**

Nor does it answer:

> **What should we conclude?**

Those questions belong to later stages.

The output of this pipeline is a collection of structured Evidence objects that remain directly traceable to their originating Sources.

This collection should be richer than the final research story. Evidence Extraction is intentionally high-recall: it preserves many small observations so later stages can decide what repeats, what matters and what should be reviewed.

```text
Source Representation
        ↓
Evidence Extraction
        ↓
Method Assessment
        ↓
Evidence Validation
        ↓
Accepted Evidence
```

---

## 39. Why Evidence Exists

Many research repositories jump directly from transcripts to summaries.

This makes it difficult to answer questions such as:

- Which participant actually said this?
- How many observations support this conclusion?
- Is this based on behaviour or opinion?
- What changed after a new interview?

Research OS introduces Evidence as a separate layer because it acts as the bridge between raw research material and interpreted knowledge.

Evidence makes knowledge:

- traceable
- reusable
- measurable
- reviewable
- explainable

Rather than repeatedly reading transcripts, later stages reason over structured observations.

---

## 40. What is Evidence?

Evidence represents **one atomic research observation**.

Atomic means it should express one meaningful observation rather than multiple conclusions.

Evidence is not the same as a Finding.

A Finding is a later, reviewable statement that Research OS may use in synthesis. Evidence is the raw traceable observation that makes such a statement inspectable.

Good Evidence:

```text
The participant looked at the product image before reading the location code.
```

Not:

```text
The participant preferred the new design because the product image reduced cognitive load.
```

The second sentence already contains interpretation.

Evidence should remain descriptive.

---

## 41. Sources of Evidence

Evidence may originate from different kinds of research material.

Examples include:

### Observed behaviour

```text
Participant scanned the shelf before reading the location code.
```

---

### Participant statement

```text
"I always look at the picture first."
```

---

### Quantitative result

```text
Average completion time decreased from 48 to 39 seconds.
```

---

### Operational observation

```text
Three shoppers skipped the highlighted product.
```

---

### Environmental observation

```text
The aisle was partially blocked during the task.
```

---

### Researcher observation

```text
The participant repeatedly adjusted their grip before scanning.
```

Researcher observations should remain clearly identifiable as observations rather than interpretations.

---

## 42. Evidence Types

Different Evidence types should remain distinguishable.

Typical Evidence Types include:

- Observed Behaviour
- Participant Statement
- Quantitative Observation
- Environmental Observation
- System Event
- Researcher Observation
- Operational Metric

Different Evidence Types carry different strengths depending on the research question.

---

## 43. Evidence Extraction

The Evidence Extractor analyses Source Representations and proposes Evidence objects.

Its goal is high recall without sacrificing practical precision.

It should not compress a full interview into one Evidence item per screen, topic or Research Question. If a participant expresses three different reactions to the same screen, those should usually become three Evidence items.

The extractor asks questions such as:

- What happened?
- What was explicitly said?
- Which events occurred?
- Which measurable outcomes exist?
- Which observations appear relevant to the Research Questions?

The extractor should avoid asking:

- Why?
- What does this imply?
- Is this important?

Those belong to later agents.

For a rich 45-minute UX interview, a healthy extraction may produce dozens of Evidence items. Many will be small. That is acceptable because later stages can cluster, prioritize and decide what becomes reviewable knowledge.

---

## 44. Evidence Extraction Rules

The following rules apply to every proposed Evidence object.

### Rule 1 — One observation

Each Evidence object should describe one primary observation.

Good:

```text
The participant looked at the product image before reading the location code.
```

Instead of:

```text
The participant preferred the interface, trusted the product image and therefore completed the task faster.
```

---

### Rule 2 — Neutral language

Evidence should avoid explanatory language.

Good:

```text
The participant paused for seven seconds.
```

Not:

```text
The participant hesitated because they were confused.
```

---

### Rule 3 — Preserve context

Evidence should contain enough information to remain understandable outside the transcript.

Poor:

```text
The participant looked there.
```

Better:

```text
The participant looked at the highlighted product image before searching the shelf.
```

---

### Rule 4 — Preserve provenance

Every Evidence object should link to:

- Source
- Source Representation
- participant
- timestamp or location
- extraction method

---

### Rule 5 — Preserve uncertainty

If extraction confidence is low, the uncertainty should remain attached.

---

## 45. Quotes

Quotes are a specialized form of Evidence.

They preserve original participant wording.

Quotes should remain verbatim whenever possible.

Example:

```text
"I don't even need the location code anymore."
```

Quotes should never be rewritten into cleaner English.

If readability improvements are needed for a Deliverable, the original Quote should remain available.

---

## 46. Behaviour vs Statement

One of the most important distinctions in Research OS is the difference between:

- observed behaviour
- participant statements

These should not be merged.

Example:

Observed:

```text
Participant looked at the product image first.
```

Statement:

```text
"I always use the product image."
```

These may support one another.

They may also contradict one another.

Keeping them separate allows researchers to identify gaps between what people say and what they actually do.

---

## 47. Quantitative Evidence

Evidence is not limited to qualitative research.

Examples include:

```text
Completion time:
41 seconds
```

```text
Success rate:
92%
```

```text
Error frequency:
4%
```

Quantitative observations should become Evidence objects rather than remaining buried inside spreadsheets.

This allows qualitative and quantitative observations to participate in the same synthesis process.

---

## 48. Method Assessment

Evidence cannot be interpreted without understanding how it was collected.

The Method Specialist therefore evaluates every Evidence object in context.

Possible considerations include:

- prototype fidelity
- facilitator influence
- sample size
- observation quality
- artificial task effects
- self-report bias
- missing context

Method Assessments do not invalidate Evidence.

They describe how Evidence should later be interpreted.

---

## 49. Evidence Validation

Not every extracted observation should automatically become accepted Evidence.

Validation checks include:

### Completeness

Does the observation contain enough context?

---

### Traceability

Can it be linked back to the Source?

---

### Duplication

Has equivalent Evidence already been extracted?

---

### Interpretation leakage

Does the Evidence already contain conclusions?

---

### Method consistency

Does the Evidence match the research method?

---

### Confidence

Is extraction confidence sufficient?

---

If problems are detected, the Evidence may be revised before acceptance.

### Density check

Evidence Extraction should include a simple density sanity check.

If a long interview produces only a small number of Evidence items, the extractor or researcher should ask:

- Did we accidentally summarize by research question?
- Did we miss minor but useful moments of confusion, expectation or comparison?
- Did we preserve participant suggestions separately from participant problems?
- Did we capture changes in understanding across the session?

Low evidence volume is not automatically wrong, but it should be explainable.

---

## 50. Evidence Relationships

Evidence objects are not isolated.

They may relate to one another.

Examples include:

Supports

```text
Evidence A

↓

Evidence B
```

---

Contradicts

```text
Observed behaviour

↓

Participant statement
```

---

Same event

```text
Observation

↓

System log
```

---

Repeated occurrence

```text
Interview 2

↓

Interview 5
```

These relationships become valuable during Pattern Detection.

---

## 51. Accepted Evidence

Once validated, Evidence becomes part of the Research Round.

At this point it becomes available for:

- Pattern Detection
- Insight Synthesis
- researcher search
- Evidence browsing
- cross-source comparisons

Accepted Evidence should remain immutable.

Corrections create new versions rather than silently editing accepted observations.

---

## 52. Evidence Versioning

Evidence may evolve.

Examples:

```text
Evidence v1

↓

Clarified wording

↓

Evidence v2
```

or

```text
Speaker corrected

↓

Participant linked

↓

Evidence v2
```

Version history should preserve:

- previous wording
- reason for change
- approving researcher
- timestamp

---

## 53. Automatic vs Review

Routine extraction may happen automatically.

Examples:

- obvious participant statements
- clearly observed actions
- quantitative measurements
- timestamp linking

Researcher review becomes more valuable when:

- interpretation may have leaked into the observation
- Source quality is poor
- participant identity is uncertain
- Evidence materially affects existing knowledge
- extraction confidence is low

The Review Queue should focus on ambiguity rather than volume.

This means Evidence may be more numerous than review cards. The UI should help the researcher review meaningful Findings while keeping the underlying Evidence visible.

---

## 54. Output of the Evidence Pipeline

At the end of this stage, Research OS has created structured observations.

It now knows:

- what participants did
- what participants said
- what happened
- where it happened
- when it happened
- how reliable the observation appears

It still does **not** know:

- why it happened
- whether it matters
- whether it represents a broader pattern
- whether it changes existing understanding

Those questions belong to the next stage.

---

## 55. Invariants

The Evidence Pipeline follows several invariants.

### Observation invariant

Evidence describes observations.

It does not explain them.

---

### Atomicity invariant

Each Evidence object represents one primary observation.

---

### Traceability invariant

Every Evidence object remains traceable to its originating Source.

---

### Neutrality invariant

Evidence should use descriptive rather than explanatory language.

---

### Method invariant

Method limitations remain attached to the Evidence.

---

### Immutability invariant

Accepted Evidence is versioned rather than silently edited.

---

## 56. Summary

The Evidence Pipeline transforms processed research material into structured observations.

This stage answers:

- What happened?
- What was said?
- What was measured?

It deliberately avoids answering:

- Why?
- So what?
- What should we change?

Those questions begin in the next stage of the Knowledge Pipeline:

**Pattern Detection**, where individual observations start becoming collective understanding.

---

# Part V — Pattern Detection Pipeline

## 57. Overview

Once individual Evidence objects have been created, the next step is to determine whether they relate to one another.

Individual observations rarely become valuable knowledge on their own.

Research becomes meaningful when observations begin to repeat, reinforce, challenge or contextualize one another.

The purpose of the Pattern Detection Pipeline is therefore to answer:

> **Which Evidence belongs together?**

It deliberately does **not** answer:

> **What does this mean?**

Interpretation happens in the Insight Pipeline.

The output of this stage is a collection of structured Patterns that describe recurring observations without explaining them.

```text
Accepted Evidence
        ↓
Evidence Comparison
        ↓
Grouping
        ↓
Pattern Detection
        ↓
Pattern Validation
        ↓
Accepted Patterns
```

---

## 58. Why Patterns Exist

Without an intermediate Pattern layer, AI is forced to jump directly from hundreds of Evidence objects to high-level Insights.

This creates several problems.

It becomes difficult to understand:

- which observations support an Insight
- how widespread a behaviour is
- whether an observation is unique or recurring
- whether contradictory behaviour exists
- how participant groups differ

Patterns solve this by introducing an explicit descriptive layer between observation and interpretation.

Patterns answer:

> "These observations appear to describe the same phenomenon."

They do **not** answer:

> "This phenomenon happens because..."

---

## 59. What is a Pattern?

A Pattern is a collection of related Evidence that describes a recurring behaviour, statement, event or measurable outcome.

Unlike an Insight, a Pattern remains descriptive.

Example:

```text
Across six participants, the product image was consistently looked at before the location code.
```

This describes repetition.

It does not yet explain why.

---

## 60. Pattern Detection

The Pattern Detector compares newly accepted Evidence against existing Evidence within the same Research Round.

Depending on the scope, it may also compare Evidence across multiple Research Rounds.

Typical questions include:

- Does similar behaviour already exist?
- Does this support an existing Pattern?
- Does it contradict an existing Pattern?
- Does it represent a new Pattern?
- Is this simply another occurrence?

The detector focuses on similarity, not explanation.

---

## 61. Pattern Categories

Patterns may describe different kinds of repetition.

### Behaviour Patterns

Example:

```text
Participants consistently searched visually before reading location codes.
```

---

### Statement Patterns

Example:

```text
Participants repeatedly described the interface as calmer.
```

---

### Quantitative Patterns

Example:

```text
Average completion time improved across three studies.
```

---

### Error Patterns

Example:

```text
Most picking mistakes occurred on the lowest shelves.
```

---

### Workflow Patterns

Example:

```text
Experienced shoppers skipped onboarding instructions.
```

---

### Environmental Patterns

Example:

```text
Navigation errors increased in crowded aisles.
```

Different Pattern categories may later contribute to the same Insight.

---

## 62. Similarity

The Pattern Detector should not rely solely on semantic similarity.

Instead, similarity should consider multiple dimensions.

Examples include:

- observed behaviour
- participant goals
- research context
- environment
- workflow
- affected object
- timing
- outcome
- participant segment

Two observations may use similar wording while describing entirely different situations.

Conversely, different wording may describe the same behaviour.

---

## 63. Pattern Formation

When new Evidence arrives, the detector asks:

### Existing Pattern?

```text
Yes

↓

Attach Evidence
```

---

### New Pattern?

```text
Yes

↓

Create Pattern
```

---

### Contradiction?

```text
Yes

↓

Create competing Pattern
```

---

### Insufficient repetition?

```text
Yes

↓

Remain individual Evidence
```

Not every observation should become part of a Pattern.

---

## 64. Pattern Strength

Patterns become stronger as supporting Evidence grows.

Possible indicators include:

- number of supporting observations
- diversity of participants
- diversity of contexts
- consistency
- methodological diversity
- time span

Strength does **not** automatically equal truth.

A very strong Pattern may later be challenged by better Evidence.

---

## 65. Negative Patterns

Absence is sometimes as important as presence.

Examples include:

```text
No participant noticed the onboarding message.
```

or

```text
Nobody used the suggested shortcut.
```

These should become valid Patterns.

Negative findings often reveal opportunities that positive findings cannot.

---

## 66. Contradictory Patterns

Different participant groups may produce different Patterns.

Example:

Pattern A

```text
New shoppers relied on product imagery.
```

Pattern B

```text
Experienced shoppers relied on location codes.
```

These should remain separate.

The system should not average them into:

```text
Shoppers sometimes use product images and sometimes location codes.
```

That removes meaningful differences.

---

## 67. Context-Specific Patterns

Patterns should always preserve their context.

Example:

```text
Manual FC
```

is different from:

```text
Automated FC
```

Likewise:

```text
First-day shoppers
```

may differ significantly from:

```text
Experienced shoppers
```

Context is not metadata.

It is part of the Pattern itself.

---

## 68. Outliers

Not every observation belongs inside the dominant Pattern.

Sometimes a single participant behaves differently.

Example:

```text
Seven participants used visual guidance.

One participant ignored it completely.
```

The outlier should remain visible.

It may later become:

- an exception
- a new participant segment
- an important contradiction
- evidence of a design problem

Suppressing outliers reduces research quality.

---

## 69. Pattern Relationships

Patterns may relate to one another.

Examples include:

Supports

```text
Pattern A

↓

Pattern B
```

---

Contradicts

```text
Pattern A

↓

Pattern C
```

---

Refines

```text
General Pattern

↓

Specific Pattern
```

---

Specializes

```text
Visual navigation

↓

Visual navigation for new shoppers
```

These relationships become valuable during Insight synthesis.

---

## 70. Pattern Validation

Before a Pattern becomes accepted, Research OS validates:

### Membership

Does the Evidence actually belong together?

---

### Scope

Is the Pattern too broad?

---

### Duplication

Does an equivalent Pattern already exist?

---

### Context

Are different environments being mixed?

---

### Interpretation leakage

Has explanatory language appeared?

Example:

Poor Pattern:

```text
Participants preferred visual navigation because it reduced cognitive load.
```

Better:

```text
Participants consistently started with visual navigation.
```

---

## 71. Accepted Patterns

Once validated, Patterns become reusable research objects.

Later agents may:

- synthesize Insights
- compare participant groups
- compare Research Rounds
- identify Opportunities
- build Program Knowledge

Patterns remain descriptive.

They are not yet research conclusions.

---

## 72. Pattern Evolution

Patterns evolve as more Evidence arrives.

Examples:

```text
Pattern

↓

Additional supporting Evidence
```

or

```text
Pattern

↓

Split into two Patterns
```

or

```text
Pattern

↓

Contradicted by new participant segment
```

Rather than recreating Patterns from scratch, Research OS should update them incrementally.

---

## 73. Automatic vs Review

Many Pattern updates are routine.

Examples:

- attach supporting Evidence
- increase occurrence count
- expand participant coverage

Researcher review becomes valuable when:

- Patterns merge
- Patterns split
- context changes
- contradictory Patterns appear
- participant segmentation changes
- the Pattern affects stable knowledge

---

## 74. Output of the Pattern Pipeline

At the end of this stage, Research OS knows:

- which observations repeat
- which observations belong together
- where behaviour differs
- where contradictions exist
- which participant groups behave differently

It still does **not** know:

- why these behaviours occur
- whether they matter
- how they affect product decisions

Those questions belong to the Insight Pipeline.

---

## 75. Invariants

The Pattern Pipeline follows several invariants.

### Descriptive invariant

Patterns describe recurring observations.

They do not explain them.

---

### Context invariant

Patterns preserve participant and environmental context.

---

### Contradiction invariant

Competing Patterns may coexist.

---

### Outlier invariant

Outliers remain visible.

---

### Traceability invariant

Every Pattern remains linked to its supporting Evidence.

---

### Incremental invariant

Patterns evolve through updates rather than regeneration.

---

## 76. Summary

The Pattern Detection Pipeline transforms isolated observations into structured descriptions of recurring behaviour.

This stage answers:

- Which observations belong together?
- What repeats?
- What differs?
- Which participant groups behave differently?

It deliberately avoids answering:

- Why does this happen?
- Why is it important?
- What should we change?

Those questions begin in the next stage:

**Insight Synthesis**, where descriptive Patterns become interpreted research knowledge.

---

# Part VI — Insight Synthesis Pipeline

## 77. Overview

The Insight Synthesis Pipeline is where Research OS begins creating research knowledge.

Previous stages answered:

- What research material do we have?
- What happened?
- Which observations belong together?

This stage answers a different question:

> **What do these observations tell us?**

For the first time, the system moves beyond describing research toward interpreting it.

This is also the point where the greatest amount of researcher judgement becomes necessary.

The output of this stage is a collection of proposed Insight Cards that explain recurring user behaviour, needs, problems or mental models.

```text
Accepted Patterns
        ↓
Insight Synthesis
        ↓
Quality Critique
        ↓
Revision
        ↓
Proposed Insight Cards
```

Importantly, these Insights are still **proposals**.

They do not become part of Current Understanding until they have passed the governance stages later in the pipeline.

---

## 78. Why Insights Exist

Patterns describe **what repeatedly happens**.

Insights explain **why those observations matter**.

For example:

Pattern:

```text
Across eight participants, the product image was consistently viewed before the location code.
```

Insight:

```text
Visual product recognition provides shoppers with an immediate starting point, reducing the need to first understand the shelving system.
```

The Pattern describes behaviour.

The Insight explains the significance of that behaviour.

---

## 79. What is an Insight?

An Insight is an interpreted understanding that helps answer one or more Research Questions.

A good Insight should:

- explain observed behaviour
- remain grounded in Evidence
- describe something generally true within its stated context
- be useful for future decisions
- remain stable beyond a single participant

Insights should not merely summarize observations.

They should increase understanding.

---

## 80. Inputs

The Insight Synthesizer combines multiple sources of information.

Typical inputs include:

- accepted Patterns
- accepted Evidence
- Method Assessments
- Research Questions
- Research Context
- participant segmentation
- existing Insight Cards
- Current Understanding
- relevant Program Knowledge
- Researcher Notes where appropriate

The synthesizer should consider existing knowledge without allowing it to override new Evidence.

---

## 81. Questions Asked During Synthesis

Rather than asking:

> What happened?

the synthesizer asks questions such as:

- What explains these Patterns?
- Which Research Questions are being answered?
- Which behaviours appear meaningful?
- Which user needs emerge?
- Which assumptions are challenged?
- Which observations reinforce existing understanding?
- Which observations change existing understanding?
- Which findings appear context-specific?
- Which findings appear broadly applicable?

These are interpretive questions rather than observational ones.

---

## 82. Insight Construction

Every proposed Insight should contain several components.

### Insight Statement

A concise description of the understanding.

Example:

```text
Visual guidance gives new shoppers confidence to begin picking without first learning location codes.
```

---

### Why It Matters

Why this understanding is important.

Example:

```text
Reducing reliance on memorized codes lowers the learning barrier for new shoppers.
```

---

### Supporting Evidence

The Evidence and Patterns that support the Insight.

---

### Contradicting Evidence

Evidence that challenges or limits the Insight.

---

### Applicability

The situations in which the Insight appears valid.

Example:

```text
Applies to:

- Manual FCs
- First-time shoppers
```

---

### Confidence

An assessment of how strongly the available research supports the Insight.

---

## 83. Insight Rules

The Insight Synthesizer follows several important rules.

### Rule 1 — Explain, don't repeat

Poor Insight:

```text
Participants looked at the product image first.
```

This repeats the Pattern.

Better:

```text
Visual product recognition provides an intuitive entry point before shoppers begin location-based navigation.
```

The second statement explains the behaviour.

---

### Rule 2 — Stay within the Evidence

The synthesizer should never claim more than the research supports.

Poor:

```text
Visual guidance always improves efficiency.
```

Better:

```text
Visual guidance appears to reduce the effort required to begin navigation for new shoppers.
```

The second statement reflects the available context.

---

### Rule 3 — Preserve context

Good Insight:

```text
Experienced shoppers continue relying on memorized location codes when those codes remain available.
```

Poor Insight:

```text
Everyone prefers location codes.
```

The context is essential.

---

### Rule 4 — Separate understanding from recommendations

An Insight explains.

It does not prescribe.

Poor:

```text
We should remove location codes.
```

Better:

```text
Experienced shoppers continue relying on location codes when they are available.
```

Recommendations belong later in the pipeline.

---

## 84. Updating Existing Insights

Most new research should refine existing knowledge rather than creating completely new Insights.

When new Patterns appear, the synthesizer first asks:

```text
Does this strengthen an existing Insight?
```

Possible outcomes include:

- strengthen confidence
- reduce confidence
- expand applicability
- narrow applicability
- clarify wording
- identify contradiction
- create new Insight

New Insights should only be created when existing knowledge cannot adequately explain the new observations.

---

## 85. Contradictions

Conflicting research should remain visible.

Example:

Insight A

```text
Visual guidance reduces onboarding effort.
```

New Evidence:

```text
Experienced shoppers ignore visual guidance.
```

Possible synthesis:

```text
Visual guidance reduces onboarding effort for new shoppers, while experienced shoppers continue relying on established navigation strategies.
```

Rather than choosing one interpretation, the synthesizer incorporates both contexts.

---

## 86. Confidence

Confidence reflects the current state of understanding.

Confidence may depend on factors such as:

- Evidence quality
- Pattern consistency
- participant diversity
- methodological diversity
- contradiction
- environmental consistency
- research volume

Confidence is not certainty.

Even high-confidence Insights remain open to revision.

---

## 87. Open Questions

Sometimes synthesis reveals missing knowledge.

Example:

```text
Experienced shoppers ignored visual guidance.
```

The synthesizer may produce:

Open Question:

```text
Would experienced shoppers adopt visual guidance if location codes were gradually removed?
```

Open Questions become first-class research objects.

They help drive future Research Rounds.

---

## 88. Assumptions

The synthesizer may also expose assumptions.

Example:

```text
Current interface assumes shoppers navigate primarily through location codes.
```

An assumption is not necessarily wrong.

It simply represents something that should be tested or acknowledged.

---

## 89. Insight Relationships

Insights rarely exist independently.

Relationships may include:

Supports

```text
Insight A

↓

Insight B
```

---

Refines

```text
General navigation Insight

↓

Manual FC Insight
```

---

Challenges

```text
New Insight

↓

Existing Insight
```

---

Depends on

```text
Insight

↓

Operational assumption
```

These relationships help researchers understand how knowledge evolves over time.

---

## 90. Quality Critique

Every proposed Insight should be challenged before becoming accepted knowledge.

The Quality Critic evaluates questions such as:

- Is this supported by the Evidence?
- Is the wording too broad?
- Does it ignore contradictions?
- Has interpretation exceeded the available research?
- Has the Pattern been summarized instead of interpreted?
- Is applicability sufficiently clear?
- Does the confidence appear justified?

This critique reduces the likelihood that convincing AI writing becomes accepted without scrutiny.

---

## 91. Revision Loop

The synthesizer and critic may iterate several times.

Example:

```text
Insight Proposal

↓

Critique

↓

Revision

↓

Critique

↓

Accepted Proposal
```

If disagreement remains unresolved, the proposal enters the Review Queue for researcher judgement.

Artificial agreement should never be the goal.

---

## 92. Output of the Insight Pipeline

At the end of this stage, Research OS has produced proposed Insight Cards.

The system now understands:

- what recurring behaviour appears to mean
- which Research Questions are being answered
- which findings reinforce existing knowledge
- which findings challenge existing knowledge
- where uncertainty remains

However, these Insights have **not** yet become official knowledge.

They remain proposals until governance has been completed.

---

## 93. Invariants

The Insight Pipeline follows several invariants.

### Interpretation invariant

Insights explain observations.

They do not merely repeat them.

---

### Grounding invariant

Every Insight must remain grounded in supporting Evidence.

---

### Context invariant

Applicability remains explicit.

Insights never claim universal truth without evidence.

---

### Recommendation invariant

Insights explain understanding.

They do not prescribe solutions.

---

### Contradiction invariant

Conflicting Evidence remains visible.

---

### Revision invariant

Insights evolve through explicit revisions.

They are never silently rewritten.

---

## 94. Summary

The Insight Synthesis Pipeline transforms recurring observations into interpreted research knowledge.

It answers:

- What do these observations tell us?
- Why do they matter?
- Which Research Questions are now better understood?
- Which assumptions should change?

At the end of this stage, Research OS possesses structured candidate knowledge.

The next stage determines whether that knowledge is trustworthy enough to become part of the evolving understanding of the product.

That responsibility belongs to the **Knowledge Curation Pipeline**.

---

*End of Part VI*

# Part VII — Knowledge Curation Pipeline

## 95. Overview

The Knowledge Curation Pipeline is responsible for maintaining the evolving body of research knowledge.

Previous stages produced proposed Insight Cards.

Those proposals now need to be compared against what Research OS already knows.

The central question becomes:

> **How should our understanding change?**

This is fundamentally different from asking:

> **What did we learn?**

Research is continuous.

Most new research does not replace existing knowledge.

Instead, it refines it.

The Knowledge Curation Pipeline exists to ensure that understanding evolves carefully, incrementally and transparently.

```text
Proposed Insight
        ↓
Compare with Current Understanding
        ↓
Determine Meaningful Change
        ↓
Create Change Proposal
        ↓
Review (if required)
        ↓
Update Current Understanding
```

---

## 96. Why Knowledge Curation Exists

Traditional research repositories usually work like this:

```text
Study

↓

Report

↓

Archive
```

Every new study produces another report.

Researchers must manually compare reports to determine whether anything has changed.

Research OS instead maintains one continuously evolving understanding.

Every new Research Round asks:

```text
What should change?
```

rather than:

```text
What should we write?
```

Knowledge Curation is responsible for answering that question.

---

## 97. Current Understanding

Current Understanding represents the best available understanding at a given moment.

It is not:

- a report
- a summary
- a presentation
- an AI response

Instead, it is the living synthesis of everything accepted so far.

Every update should leave Current Understanding slightly more accurate than before.

---

## 98. Types of Knowledge Change

When a new Insight arrives, only a limited number of outcomes are possible.

### No change

Example:

```text
New interview confirms existing Insight.
```

Result:

```text
Attach supporting Evidence.

No researcher review.
```

---

### Confidence increases

Example:

```text
Three additional participants show identical behaviour.
```

Result:

```text
Confidence

Moderate

↓

High
```

---

### Confidence decreases

Example:

```text
Multiple contradictory observations appear.
```

Result:

```text
Insight remains.

Confidence reduced.
```

---

### Applicability changes

Example:

Previously:

```text
All shoppers
```

Updated:

```text
New shoppers only
```

The Insight has not changed.

Its scope has.

---

### Insight refined

Example:

Old:

```text
Visual guidance reduces cognitive effort.
```

New:

```text
Visual guidance reduces cognitive effort primarily during onboarding.
```

The Insight becomes more precise.

---

### Insight split

Sometimes one Insight actually describes two different phenomena.

Example:

Old:

```text
Shoppers rely on product images.
```

Updated:

```text
New shoppers rely on product images.

Experienced shoppers rely on location codes.
```

Splitting often improves clarity.

---

### Insight merged

Sometimes separate Insights describe the same underlying understanding.

Rather than keeping duplicate knowledge, they may become one richer Insight.

---

### New Insight

If existing knowledge cannot explain the new findings, a genuinely new Insight is created.

This should happen relatively infrequently.

---

### Insight superseded

Occasionally new research shows that previous understanding is no longer the best explanation.

The previous Insight should not disappear.

Instead:

```text
Superseded
```

becomes part of its history.

---

## 99. Meaningful Change Detection

One of the central responsibilities of Research OS is deciding whether a change is meaningful.

Not every modification deserves researcher attention.

For example:

```text
Added one supporting Quote.
```

is probably not meaningful.

However:

```text
Confidence changed from High to Low.
```

almost certainly is.

The Knowledge Curator therefore classifies every proposal.

---

## 100. Routine Changes

Routine changes may happen automatically.

Typical examples include:

- attaching supporting Evidence
- attaching Quotes
- metadata updates
- typo corrections
- relationship updates
- additional participant coverage
- stronger traceability

These changes improve the knowledge base without changing its meaning.

---

## 101. Meaningful Changes

Meaningful changes affect understanding.

Examples include:

- new Insight
- changed applicability
- changed confidence
- contradiction introduced
- contradiction resolved
- Insight merged
- Insight split
- Insight superseded
- new Open Question
- new Assumption
- updated Research Question answer

Meaningful changes usually enter the Review Queue.

---

## 102. Comparing Against Existing Knowledge

The Knowledge Curator compares every proposed Insight with Current Understanding.

Rather than asking:

```text
Is this correct?
```

it asks:

```text
What relationship exists?
```

Possible relationships include:

- identical
- strengthens
- weakens
- refines
- contradicts
- duplicates
- specializes
- generalizes
- replaces

This comparison allows Research OS to evolve knowledge incrementally.

---

## 103. Contradictions

Contradictions should rarely result in deleting knowledge.

Instead they become explicit parts of understanding.

Example:

Current Understanding:

```text
Experienced shoppers primarily navigate using location codes.
```

New Research:

```text
Experienced shoppers preferred visual guidance after one week.
```

Possible result:

```text
Contradiction created.

Further research required.
```

Current Understanding becomes richer rather than simpler.

---

## 104. Knowledge Stability

Some Insights become increasingly stable over time.

Others remain volatile.

Knowledge stability depends on factors such as:

- repeated confirmation
- participant diversity
- methodological diversity
- time
- contradiction frequency
- environmental consistency

Stable knowledge should not become impossible to change.

It should simply require stronger Evidence.

---

## 105. Change Records

Every meaningful update produces a Change Record.

A Change Record captures:

- previous state
- new state
- reason
- triggering Evidence
- triggering Research Round
- approving researcher
- timestamp

Researchers should always be able to reconstruct how understanding evolved.

---

## 106. Review Queue

Meaningful changes enter the Review Queue.

A Review Item should answer:

- What changed?
- Why?
- Which Evidence caused this?
- What agrees?
- What disagrees?
- Which decisions are available?

The goal is to minimize researcher effort while maximizing researcher control.

---

## 107. Updating Current Understanding

Once approved, the proposal becomes part of Current Understanding.

Importantly:

Current Understanding itself is versioned.

Researchers should be able to inspect:

```text
Current Understanding

↓

Yesterday
```

```text
Current Understanding

↓

Last month
```

```text
Current Understanding

↓

Today
```

Knowledge should evolve without losing history.

---

## 108. Output of the Knowledge Curation Pipeline

At the end of this stage, Research OS has determined:

- what changed
- how important the change is
- whether review is required
- how Current Understanding should evolve

This is the point where research stops being a collection of findings and becomes a continuously maintained body of knowledge.

---

## 109. Invariants

The Knowledge Curation Pipeline follows several invariants.

### Evolution invariant

Knowledge evolves.

It is never recreated from scratch.

---

### History invariant

Previous understanding is preserved.

---

### Meaning invariant

Routine updates never silently change meaning.

---

### Governance invariant

Meaningful changes require explicit handling.

---

### Traceability invariant

Every change remains linked to the Evidence that caused it.

---

### Transparency invariant

Researchers can always understand why Current Understanding changed.

---

## 110. Summary

The Knowledge Curation Pipeline is the heart of Research OS.

It transforms isolated research findings into continuously evolving organizational knowledge.

Rather than generating another report, it asks a more valuable question:

> **What has our understanding become?**

Every new Research Round contributes to that answer.

The next stage builds upon this evolving understanding to identify Opportunities and Recommendations.

---

*End of Part VII*

# Part VIII — Opportunity & Recommendation Pipeline

## 111. Overview

Once Current Understanding has been updated, Research OS can begin answering the question most product teams ultimately care about:

> **What should we do?**

This stage transforms research knowledge into actionable guidance.

Unlike previous stages, this pipeline is intentionally forward-looking.

It does not describe the current state of the world.

Instead, it explores how the world could be improved.

Importantly, this pipeline is split into two distinct steps:

```text
Current Understanding
        ↓
Opportunity Identification
        ↓
Opportunity Assessment
        ↓
Recommendation Generation
        ↓
Recommendation Review
```

Separating Opportunities from Recommendations ensures that problems remain independent from solutions.

---

## 112. Why Separate Opportunities and Recommendations?

Many research reports jump directly from Insights to solutions.

For example:

```text
Insight

↓

Redesign the onboarding
```

This skips an important step.

Understanding a problem does not automatically reveal the best solution.

Research OS therefore distinguishes between:

**Opportunity**

> Something that could be improved.

**Recommendation**

> A proposed way to improve it.

One Opportunity may lead to many possible Recommendations.

Likewise, the same Recommendation may address multiple Opportunities.

---

## 113. Opportunities

An Opportunity represents a gap between the current experience and a better future experience.

It is solution-independent.

Examples:

```text
New shoppers rely heavily on product imagery to begin navigation.
```

↓

Opportunity:

```text
Reduce the learning effort required to start picking.
```

Notice that the Opportunity does not prescribe *how* this should be achieved.

---

## 114. Characteristics of Good Opportunities

Good Opportunities are:

- grounded in research
- solution-independent
- understandable outside the research team
- connected to user needs
- connected to business context where appropriate
- durable across multiple design iterations

Poor Opportunity:

```text
Replace the location code with a shelf illustration.
```

Better Opportunity:

```text
Help shoppers orient themselves without requiring memorization.
```

---

## 115. Opportunity Identification

The Opportunity Agent analyses Current Understanding and asks questions such as:

- Which user needs remain unmet?
- Which recurring frustrations exist?
- Which unnecessary effort exists?
- Which workflows remain inefficient?
- Which assumptions could be challenged?
- Which constraints no longer appear necessary?
- Which behaviours indicate an unmet need?
- Which user goals are difficult to achieve?

These questions are intentionally open-ended.

The goal is exploration rather than solution generation.

---

## 116. Opportunity Relationships

Opportunities may relate to one another.

Examples include:

### Parent Opportunity

```text
Reduce cognitive effort during picking.
```

↓

Child Opportunities

```text
Reduce navigation effort.

Reduce product identification effort.

Reduce error recovery effort.
```

This hierarchy helps teams work at different levels of abstraction.

---

## 117. Opportunity Assessment

Not every Opportunity deserves immediate attention.

Research OS therefore assesses Opportunities along multiple dimensions.

Possible dimensions include:

- research confidence
- user impact
- operational impact
- business relevance
- frequency
- severity
- affected population
- strategic alignment

These dimensions are intended to support prioritization rather than determine it automatically.

---

## 118. Recommendations

Recommendations propose ways to address Opportunities.

Unlike Insights, Recommendations are intentionally prescriptive.

Example:

Opportunity:

```text
Reduce onboarding effort for new shoppers.
```

Possible Recommendations:

- increase emphasis on product imagery
- simplify location information
- provide progressive guidance
- delay advanced navigation concepts
- redesign onboarding flow

All of these may address the same Opportunity.

---

## 119. Recommendation Generation

Recommendations should be treated as hypotheses rather than answers.

A Recommendation expresses a belief that a particular intervention may improve the current experience.

For example:

```text
Increasing the size of the shelf visualization may help shoppers orient themselves more quickly.
```

Notice the wording:

- may
- appears likely
- based on current understanding

Recommendations should acknowledge uncertainty.

---

## 120. Recommendation Structure

Every Recommendation should contain:

### Proposal

What is being suggested?

---

### Opportunity

Which Opportunity does it address?

---

### Supporting Insights

Which Insights support the Recommendation?

---

### Supporting Evidence

Which Evidence ultimately grounds the Recommendation?

---

### Expected Outcome

What behaviour is expected to change?

---

### Risks

What could go wrong?

---

### Assumptions

Which assumptions should be validated?

---

### Confidence

How strongly does the current research support this Recommendation?

---

## 121. Multiple Recommendations

Research rarely produces one obvious solution.

Research OS should encourage multiple Recommendations.

Example:

Opportunity:

```text
Reduce navigation effort.
```

Possible Recommendations:

Option A

```text
Increase shelf visualization prominence.
```

Option B

```text
Simplify location codes.
```

Option C

```text
Introduce progressive navigation cues.
```

Rather than choosing the "best" solution, Research OS presents multiple research-informed possibilities.

---

## 122. Recommendations and Experiments

Recommendations often become the starting point for experimentation.

Example:

Recommendation

↓

Experiment

↓

Evidence

↓

New Insights

↓

Updated Current Understanding

This creates a continuous learning loop.

Recommendations are therefore not the end of the research process.

They are often the beginning of the next Research Round.

---

## 123. Recommendation Review

Recommendations should be challenged before adoption.

Review questions include:

- Is the Recommendation supported by the Insights?
- Does it actually address the Opportunity?
- Is it solution-independent enough?
- Have alternative approaches been considered?
- Are important assumptions explicit?
- Are potential risks acknowledged?

The review process encourages better decision-making rather than preventing change.

---

## 124. Recommendations vs Decisions

Research OS deliberately separates Recommendations from product decisions.

Research produces Recommendations.

Product teams make Decisions.

A Decision may:

- accept the Recommendation
- reject the Recommendation
- postpone the Recommendation
- partially adopt the Recommendation
- choose an alternative Recommendation

Keeping these separate preserves the distinction between research and product ownership.

---

## 125. Opportunity Evolution

Like Insights, Opportunities evolve over time.

Possible changes include:

- confidence increases
- confidence decreases
- merged with another Opportunity
- split into multiple Opportunities
- resolved
- deprioritized
- reactivated

An Opportunity should not disappear simply because a feature has been released.

Instead, its status changes.

This preserves organizational learning.

---

## 126. Recommendation Evolution

Recommendations also evolve.

Examples:

```text
Recommendation

↓

Experiment

↓

Validated
```

or

```text
Recommendation

↓

Experiment

↓

Rejected
```

or

```text
Recommendation

↓

Revised
```

Maintaining this history helps teams understand not only what was recommended, but what actually worked.

---

## 127. Output of the Opportunity & Recommendation Pipeline

At the end of this stage, Research OS has produced:

- structured Opportunities
- prioritized Opportunities
- proposed Recommendations
- supporting rationale
- assumptions
- expected behavioural outcomes

Importantly, none of these represent product commitments.

They remain research outputs intended to support better decisions.

---

## 128. Invariants

The Opportunity & Recommendation Pipeline follows several invariants.

### Opportunity invariant

Opportunities describe problems worth solving.

They do not prescribe solutions.

---

### Recommendation invariant

Recommendations propose interventions.

They do not represent decisions.

---

### Grounding invariant

Every Recommendation must remain traceable to supporting Insights and Evidence.

---

### Alternatives invariant

Multiple Recommendations may exist for the same Opportunity.

---

### Experiment invariant

Recommendations are hypotheses that should ideally be validated through future research or experimentation.

---

### Ownership invariant

Research informs decisions.

It does not make them.

---

## 129. Summary

The Opportunity & Recommendation Pipeline transforms organizational understanding into actionable guidance.

It answers:

- Where should we improve?
- Which user needs remain unmet?
- Which interventions appear promising?
- Which assumptions should be tested?

By separating Opportunities from Recommendations, Research OS ensures that product teams remain free to explore multiple solutions while staying grounded in research.

The next stage extends this beyond individual Research Rounds by maintaining knowledge at the program level and capturing how understanding evolves over time.

---

*End of Part VIII*

# Part IX — Round Closure & Program Knowledge Pipeline

## 130. Overview

Throughout a Research Round, knowledge evolves continuously.

Evidence is extracted.

Patterns emerge.

Insights are proposed.

Current Understanding is updated.

Eventually, however, a Research Round reaches a natural milestone.

At that point, Research OS captures what was learned during that Round while simultaneously updating the long-term understanding of the broader Research Program.

This stage answers two complementary questions:

> **What did this Research Round contribute?**

and

> **How has the overall Program Understanding changed?**

Rather than treating these as separate activities, Research OS performs them together.

```text
Current Understanding
        ↓
Round Closure
        ↓
Round Knowledge Snapshot
        ↓
Program Comparison
        ↓
Program Knowledge Update
```

Round Knowledge becomes a historical record.

Program Knowledge remains a living body of knowledge.

---

## 131. Why Separate Round Knowledge and Program Knowledge?

Research exists at multiple timescales.

A Research Round captures understanding within a specific period, context and research objective.

A Research Program captures understanding that evolves over many Research Rounds.

For example:

```text
Research Program

Fulfillment Operations
```

may contain Research Rounds such as:

- Baseline workflow
- Visual navigation concept
- Multi-pick improvements
- Rollout validation
- Experienced shopper adoption

Each Round answers different questions.

Together they build long-term understanding.

Without this distinction, organizations either lose historical context or continually rewrite history.

---

## 132. Round Closure

Closing a Research Round does not freeze its data.

Instead, it records the state of understanding at the moment the Round is considered complete.

Round Closure captures:

- accepted Evidence
- accepted Patterns
- accepted Insights
- Open Questions
- unresolved contradictions
- Recommendations
- researcher decisions
- knowledge changes introduced during the Round

This produces a durable historical snapshot.

---

## 133. Round Knowledge

Round Knowledge answers:

> **What did we know at the end of this specific Research Round?**

It should be possible to revisit a completed Round years later and understand:

- what was discovered
- which Evidence existed
- which assumptions were made
- which Recommendations were proposed
- which uncertainties remained

Round Knowledge should never change after closure.

If mistakes are later discovered, they become part of subsequent Research Rounds rather than rewriting history.

---

## 134. Program Knowledge

Program Knowledge represents the cumulative understanding across all Research Rounds within a Research Program.

Unlike Round Knowledge, Program Knowledge evolves continuously.

It answers:

> **What do we currently believe about this product, workflow or domain?**

Examples include:

- enduring user behaviours
- validated mental models
- recurring operational constraints
- long-term design principles
- validated Opportunities
- historical evolution of understanding

Program Knowledge should always represent the best currently available understanding.

---

## 135. Updating Program Knowledge

When a Round closes, Research OS compares the Round's contributions against existing Program Knowledge.

Possible outcomes include:

### Reinforcement

```text
Existing Insight

↓

Additional support
```

---

### Refinement

```text
Existing Insight

↓

More precise understanding
```

---

### Expansion

```text
Existing Insight

↓

Broader applicability
```

---

### Limitation

```text
Existing Insight

↓

Narrower applicability
```

---

### Contradiction

```text
Existing Insight

↓

Competing understanding
```

---

### New Program Insight

```text
Round introduces previously unknown knowledge.
```

The objective is evolution, not replacement.

---

## 136. Cross-Round Learning

One of the greatest strengths of Research OS is the ability to connect research over time.

For example:

```text
Round 2

↓

Participants rely on product images.
```

```text
Round 5

↓

Participants still rely on product images.
```

```text
Round 8

↓

Experienced shoppers adopt visual navigation after two weeks.
```

Viewed independently, each finding is useful.

Viewed together, they reveal a much richer understanding of learning behaviour.

Program Knowledge exists to capture these long-term developments.

---

## 137. Knowledge Evolution

Every update contributes to the historical evolution of understanding.

Researchers should be able to answer questions such as:

- When did this Insight first appear?
- How has confidence changed?
- Which Research Rounds strengthened it?
- Which studies challenged it?
- Which assumptions were eventually disproven?
- Which Opportunities have already been explored?

Knowledge should have a visible history rather than only a current state.

---

## 138. Open Questions Across Rounds

Not every Research Question is answered within a single Round.

Some remain open for months or years.

Research OS therefore maintains persistent Open Questions.

An Open Question may be:

- created during one Round
- partially answered during another
- fully answered later
- replaced by a better question
- closed after sufficient Evidence

This creates continuity between Research Rounds.

---

## 139. Assumption Tracking

Assumptions should evolve alongside knowledge.

Examples include:

```text
Assumption

↓

Validated
```

```text
Assumption

↓

Rejected
```

```text
Assumption

↓

Still uncertain
```

Tracking assumptions helps researchers distinguish between:

- what is known
- what is believed
- what still needs validation

---

## 140. Program Metrics

Research OS may maintain high-level indicators describing the maturity of Program Knowledge.

Examples include:

- number of active Insights
- number of stable Insights
- unresolved contradictions
- active Open Questions
- validated assumptions
- research coverage across user groups
- research coverage across workflows
- confidence distribution

These indicators describe the state of knowledge rather than product performance.

---

## 141. Round Archive

Closing a Round creates an immutable archive.

The archive should include:

- research scope
- Research Questions
- Sources
- accepted Evidence
- Patterns
- Insights
- Recommendations
- researcher decisions
- Change Records

Researchers should always be able to reconstruct how conclusions were reached during that Round.

---

## 142. Relationships Between Rounds

Research Rounds may relate to one another.

Examples include:

Follow-up

```text
Round 2

↓

Round 3
```

---

Replication

```text
Round 5

↓

Repeat study
```

---

Extension

```text
Round 4

↓

Additional participant group
```

---

Validation

```text
Prototype

↓

Production rollout
```

These relationships help explain how knowledge has developed over time.

---

## 143. Output of the Round Closure Pipeline

At the end of this stage, Research OS has produced:

- immutable Round Knowledge
- updated Program Knowledge
- historical Change Records
- updated Open Questions
- updated Assumptions
- cross-Round relationships
- knowledge evolution history

Research is no longer organized as disconnected projects.

Instead, every completed Round becomes another step in the continuous growth of organizational understanding.

---

## 144. Invariants

The Round Closure & Program Knowledge Pipeline follows several invariants.

### Snapshot invariant

Round Knowledge represents understanding at a specific moment in time.

It never changes after closure.

---

### Evolution invariant

Program Knowledge evolves continuously across Research Rounds.

---

### Historical invariant

Previous understanding is never lost.

---

### Traceability invariant

Every Program Insight remains traceable to the contributing Research Rounds.

---

### Continuity invariant

Open Questions and Assumptions may continue across multiple Research Rounds.

---

### Separation invariant

Round Knowledge captures history.

Program Knowledge captures the current understanding.

The two should never be confused.

---

## 145. Summary

The Round Closure & Program Knowledge Pipeline connects individual studies into a continuous research practice.

It answers:

- What did this Research Round contribute?
- How has our long-term understanding changed?
- Which questions remain unanswered?
- How has knowledge evolved over time?

By separating immutable Round Knowledge from continuously evolving Program Knowledge, Research OS preserves both historical accuracy and organizational learning.

The next stage focuses on making this knowledge useful by transforming it into reports, presentations and other consumable outputs without changing the underlying knowledge itself.

---

*End of Part IX*

# Part X — Deliverable Pipeline

## 146. Overview

Research OS is built around the idea that **knowledge is the product of research**.

Deliverables are not.

Reports, presentations and summaries remain valuable, but they are considered **views of knowledge**, not the knowledge itself.

The Deliverable Pipeline transforms existing knowledge into artifacts for specific audiences without changing the underlying knowledge.

It answers:

> **How should this knowledge be communicated?**

Rather than:

> **What do we know?**

```text
Current Understanding
        ↓
Audience Selection
        ↓
Content Selection
        ↓
Narrative Construction
        ↓
Deliverable Generation
        ↓
Human Review
        ↓
Published Deliverable
```

Knowledge flows into Deliverables.

Deliverables never flow back into knowledge.

---

## 147. Why Deliverables Are Separate

In many organizations, reports become the primary source of truth.

Over time this creates problems:

- knowledge becomes fragmented
- reports become outdated
- researchers repeat previous analyses
- contradictory reports coexist
- organizational learning slows down

Research OS separates:

```text
Knowledge
```

from

```text
Communication
```

The same Insight may appear in:

- a presentation
- a research report
- a dashboard
- an executive summary
- a design workshop
- a product brief

All of these reference the same underlying knowledge.

---

## 148. Deliverable Types

Different audiences require different representations of the same knowledge.

Typical Deliverable Types include:

- Research Report
- Executive Summary
- Slide Deck
- Workshop Materials
- Insight Collection
- Opportunity Overview
- Design Brief
- Experiment Proposal
- Product Review
- Research Timeline
- Evidence Appendix

Future Deliverable Types can be introduced without changing the knowledge model.

---

## 149. Audience-Aware Communication

Every Deliverable is created for a specific audience.

Examples include:

### Product Managers

Typically interested in:

- Opportunities
- Recommendations
- expected outcomes
- risks
- confidence

---

### Designers

Typically interested in:

- user behaviour
- mental models
- Evidence
- supporting Quotes
- Opportunities

---

### Leadership

Typically interested in:

- strategic themes
- major Insights
- confidence
- business impact
- research coverage

---

### Researchers

Typically interested in:

- Evidence
- methodology
- contradictions
- traceability
- Open Questions

The underlying knowledge remains identical.

Only the presentation changes.

---

## 150. Content Selection

Not every Insight belongs in every Deliverable.

The Deliverable Pipeline selects content based on factors such as:

- audience
- research objective
- Program
- Research Round
- confidence
- relevance
- publication scope

Selection should remain transparent.

Researchers should always be able to see why content was included or omitted.

---

## 151. Narrative Construction

Knowledge is rarely consumed as isolated Insight Cards.

Most audiences require a coherent narrative.

The Deliverable Generator organizes knowledge into a logical flow.

For example:

```text
Research Goal

↓

Method

↓

Key Insights

↓

Opportunities

↓

Recommendations

↓

Open Questions
```

The narrative should remain grounded in the underlying knowledge.

It should never introduce unsupported conclusions.

---

## 152. Evidence Inclusion

Deliverables should make supporting Evidence available when appropriate.

Examples include:

- participant Quotes
- screenshots
- workflow diagrams
- observation summaries
- quantitative metrics
- confidence indicators

Different audiences require different levels of detail.

For example:

An executive summary may show only the highest-level Insights.

A research report may include direct links to every supporting Evidence object.

---

## 153. Knowledge References

Every meaningful statement within a Deliverable should remain traceable.

For example:

```text
Recommendation

↓

Opportunity

↓

Insight

↓

Pattern

↓

Evidence

↓

Source
```

This allows researchers to answer questions such as:

- Where did this conclusion come from?
- Which interviews support this?
- Which participants disagreed?
- How confident are we?

Deliverables become explainable rather than authoritative.

---

## 154. Living Deliverables

Traditional reports become outdated as soon as new research arrives.

Research OS instead supports living Deliverables.

A Deliverable may optionally remain connected to Current Understanding.

Possible update modes include:

### Static

The Deliverable captures knowledge at one moment in time.

Future knowledge does not affect it.

---

### Living

The Deliverable reflects Current Understanding.

As knowledge evolves, the Deliverable can be refreshed.

---

### Review Required

Knowledge has changed.

A refreshed Deliverable is available but requires researcher approval before publication.

This allows organizations to choose the level of automation they prefer.

---

## 155. Versioning

Deliverables are versioned independently from knowledge.

Example:

```text
Insight v8
```

may appear in:

```text
Research Report v2
```

Later:

```text
Insight v9
```

does not automatically invalidate the report.

Instead, Research OS records:

- which Insight versions were used
- publication date
- Research Round
- author
- approval status

This preserves historical context.

---

## 156. Publication Review

Before publication, Deliverables may require review.

Typical review questions include:

- Is the narrative accurate?
- Are sensitive details removed?
- Are confidence levels represented correctly?
- Are recommendations appropriately framed?
- Are unsupported claims introduced?
- Is the intended audience served?

Review focuses on communication quality rather than research validity.

Research validity has already been addressed earlier in the pipeline.

---

## 157. Published Deliverables

Once approved, Deliverables become published artifacts.

Importantly:

Publishing does **not** freeze knowledge.

Instead:

```text
Knowledge

↓

Published Deliverable
```

Future research continues independently.

This separation allows organizations to maintain historical publications while continuously improving organizational understanding.

---

## 158. Deliverable Relationships

Deliverables may relate to one another.

Examples include:

Derived from

```text
Research Report

↓

Executive Summary
```

---

Expanded into

```text
Insight Collection

↓

Workshop
```

---

Updated by

```text
Version 1

↓

Version 2
```

These relationships help researchers understand how communication evolves over time.

---

## 159. Output of the Deliverable Pipeline

At the end of this stage, Research OS has produced one or more communication artifacts.

These artifacts may include:

- reports
- presentations
- dashboards
- summaries
- workshop materials
- design briefs

Importantly, none of these become part of the knowledge model.

They are representations of knowledge, not knowledge itself.

---

## 160. Invariants

The Deliverable Pipeline follows several invariants.

### Separation invariant

Deliverables are generated from knowledge.

Knowledge is never generated from Deliverables.

---

### Traceability invariant

Every important statement remains traceable to supporting research.

---

### Audience invariant

Communication adapts to the audience.

Underlying knowledge does not.

---

### Version invariant

Deliverables are versioned independently from Insights.

---

### Publishing invariant

Publishing never changes Current Understanding.

---

### Communication invariant

Deliverables communicate knowledge.

They do not replace it.

---

## 161. Summary

The Deliverable Pipeline transforms research knowledge into useful communication.

It answers:

- Who needs this knowledge?
- What should they see?
- How should it be presented?
- How can it remain traceable?

By treating Deliverables as views rather than sources of truth, Research OS ensures that organizational understanding continues to evolve while communication remains accurate, reusable and audience-specific.

The final part of the Knowledge Pipeline describes the cross-cutting concepts that apply across every stage of the system, followed by an end-to-end example of how knowledge flows from a single Source to continuously evolving Program Knowledge.

---

*End of Part X*

# Part XI — Cross-Cutting Concepts

## 162. Overview

The previous chapters described the Knowledge Pipeline as a sequence of transformations.

However, several concepts are not owned by any single pipeline stage.

Instead, they apply throughout the entire system.

These cross-cutting concepts ensure that Research OS remains:

- trustworthy
- explainable
- maintainable
- auditable
- scalable

They define **how** knowledge moves through the system, regardless of **where** it is in the pipeline.

---

## 163. Traceability

Traceability is one of the fundamental principles of Research OS.

Every meaningful research object should be traceable back to its origin.

A researcher should always be able to answer:

- Where did this come from?
- Which Evidence supports it?
- Which participants contributed?
- Which Research Round introduced it?
- Which Source contains the original context?

The complete traceability chain is:

```text
Deliverable
        ↓
Recommendation
        ↓
Opportunity
        ↓
Insight
        ↓
Pattern
        ↓
Evidence
        ↓
Source Representation
        ↓
Source
```

Every object should also be navigable in the opposite direction.

Researchers should be able to move seamlessly between high-level understanding and raw research material.

---

## 164. Versioning

Everything that represents knowledge should be versioned.

Versioning allows researchers to answer questions such as:

- What changed?
- When did it change?
- Why did it change?
- Who approved it?
- Which Evidence caused it?

Different objects evolve independently.

Examples include:

- Source Representations
- Evidence
- Patterns
- Insights
- Current Understanding
- Opportunities
- Recommendations
- Deliverables

Version history should preserve evolution rather than overwrite it.

---

## 165. Provenance

Every object should record where it originated.

Typical provenance information includes:

- originating Source
- originating Research Round
- processing agent
- researcher
- timestamps
- approval history
- contributing Evidence

Provenance is closely related to traceability but answers a different question.

Traceability asks:

> How do I navigate backwards?

Provenance asks:

> How did this object come into existence?

---

## 166. Confidence

Confidence exists throughout the pipeline.

Different stages express different forms of confidence.

Examples include:

### Processing confidence

```text
OCR confidence

Speaker detection confidence

Translation confidence
```

---

### Evidence confidence

```text
Extraction confidence

Observation quality
```

---

### Pattern confidence

```text
Consistency

Repetition

Coverage
```

---

### Insight confidence

```text
Research confidence
```

Confidence should never be collapsed into a single universal score.

Each stage should communicate uncertainty appropriate to that stage.

---

## 167. Human Review

Research OS is designed around selective human review.

Researchers should spend time reviewing meaningful changes rather than routine processing.

Typical review triggers include:

- contradictory findings
- new Insights
- Insight splits
- Insight merges
- confidence reductions
- applicability changes
- sensitive content
- publication approval

Routine processing should generally proceed without interruption.

This allows researchers to focus their expertise where it creates the most value.

---

## 168. Automation Principles

Automation should support researchers rather than replace them.

Research OS follows several principles.

### Automate repetitive work

Examples include:

- transcription
- extraction
- clustering
- traceability
- formatting

---

### Escalate ambiguity

Examples include:

- conflicting interpretations
- uncertain participant identity
- contradictory findings
- unclear scope

---

### Preserve researcher ownership

AI may propose.

Researchers approve.

Automation should reduce effort without reducing accountability.

---

## 169. Explainability

Every important output should be explainable.

For example:

An Insight should answer:

- Why does this Insight exist?
- Which Patterns support it?
- Which Evidence supports those Patterns?
- Which participants contributed?
- Which contradictions exist?

Researchers should never encounter unexplained AI conclusions.

Explainability is more important than sophistication.

---

## 170. Knowledge Freshness

Knowledge changes over time.

Research OS should distinguish between:

### Current

Knowledge supported by recent research.

---

### Stable

Knowledge repeatedly confirmed over long periods.

---

### Aging

Knowledge that has not recently been revisited.

---

### Outdated

Knowledge that has likely become unreliable due to changes in:

- product
- workflow
- users
- environment
- business context

Knowledge should not become outdated automatically.

Instead, freshness provides useful context during interpretation.

---

## 171. Governance

Governance ensures that organizational knowledge evolves responsibly.

Governance includes:

- approval workflows
- review history
- access control
- privacy
- version history
- audit logs
- publication control

Governance should support researchers rather than create unnecessary administrative work.

---

## 172. Access Control

Different users require different levels of access.

For example:

Researchers may access:

- Sources
- Evidence
- participant information

Product Managers may primarily access:

- Insights
- Opportunities
- Recommendations

Leadership may primarily access:

- Program Knowledge
- strategic summaries
- Deliverables

Access restrictions should propagate throughout the pipeline.

For example:

Restricted Sources should not accidentally become unrestricted Deliverables.

---

## 173. Privacy

Privacy requirements should persist throughout the knowledge lifecycle.

Examples include:

- participant consent
- anonymization
- retention policies
- export restrictions
- confidential business information

Privacy is established during Source Intake but remains attached to every downstream object.

Knowledge should never become detached from its privacy requirements.

---

## 174. Search and Retrieval

Every object within Research OS should be searchable.

Researchers should be able to search by:

- Research Program
- Research Round
- participant
- workflow
- product
- Opportunity
- Insight
- Pattern
- Evidence
- Source
- Quote
- Research Question
- Assumption
- Open Question

Search should navigate knowledge rather than simply matching text.

---

## 175. Scalability

Research OS is intended to support years of accumulated research.

Scalability therefore depends on:

- incremental updates
- reusable knowledge
- modular agents
- independent pipeline stages
- versioned objects
- durable identifiers

The architecture should scale primarily through organization rather than computational power.

---

## 176. Evolution

Research OS is designed to evolve.

Future improvements may include:

- new AI agents
- additional Source Types
- richer Pattern relationships
- improved confidence models
- additional Deliverable types
- new research methods

These extensions should integrate into the existing architecture without requiring fundamental redesign.

This is achieved by keeping pipeline stages loosely coupled and responsibilities clearly separated.

---

## 177. End-to-End Lifecycle

Taken together, the complete lifecycle looks as follows:

```text
Research Planning
        ↓
Source
        ↓
Source Representation
        ↓
Evidence
        ↓
Pattern
        ↓
Insight Proposal
        ↓
Knowledge Curation
        ↓
Current Understanding
        ↓
Opportunity
        ↓
Recommendation
        ↓
Round Knowledge
        ↓
Program Knowledge
        ↓
Deliverables
```

At every step:

- traceability is preserved
- uncertainty remains visible
- governance is applied
- researchers retain control

The pipeline therefore represents a continuous cycle of organizational learning rather than a sequence of disconnected research projects.

---

## 178. Invariants

The Cross-Cutting Concepts follow several system-wide invariants.

### Traceability invariant

Every knowledge object remains traceable to its origin.

---

### Explainability invariant

Every important conclusion can be explained through supporting research.

---

### Versioning invariant

Knowledge evolves through explicit versions rather than silent edits.

---

### Governance invariant

Meaningful changes remain reviewable.

---

### Privacy invariant

Privacy requirements propagate throughout the entire knowledge lifecycle.

---

### Ownership invariant

Researchers remain accountable for organizational knowledge.

AI supports that responsibility.

---

## 179. Summary

The Cross-Cutting Concepts provide the foundation that connects every stage of the Knowledge Pipeline.

Rather than belonging to one specific pipeline stage, they define the qualities that every stage must uphold.

Together they ensure that Research OS remains:

- explainable
- trustworthy
- auditable
- scalable
- continuously evolving

The final chapter demonstrates how all of these concepts work together by following a single piece of research from its original Source to continuously evolving Program Knowledge.

---

*End of Part XI*

# Part XII — End-to-End Example

## 180. Overview

The previous chapters described each stage of the Knowledge Pipeline independently.

This final chapter follows a single piece of research through the complete system.

Rather than introducing new concepts, it demonstrates how the existing concepts work together.

The example illustrates how Research OS transforms one interview into continuously evolving organizational knowledge while preserving traceability, uncertainty and researcher oversight.

---

## 181. Research Context

A product team is investigating how shoppers navigate a manual fulfillment center.

The Research Program is:

```text
Fulfillment Operations
```

The current Research Round focuses on a new navigation concept.

The primary Research Question is:

> **How do shoppers find the correct product?**

A researcher conducts an interview combined with a usability test.

The session is recorded and uploaded into Research OS.

---

## 182. Source Intake

The uploaded recording becomes a new Source.

During intake, the system determines:

- Source Type: Audio Recording
- Source Role: Primary Research
- Research Method: Moderated Usability Test
- Language: Dutch
- Associated Research Round: Visual Navigation Validation

Metadata such as the researcher, participant, recording date and consent information are attached.

A processing plan is generated.

```text
Audio Recording
        ↓
Transcription
        ↓
Speaker Identification
        ↓
Evidence Extraction
```

At this stage, the system still knows nothing about the participant's behaviour.

---

## 183. Source Processing

The recording is processed into several Source Representations.

These include:

- transcript
- timestamp alignment
- speaker separation
- segmented tasks

The original recording remains unchanged.

Every sentence in the transcript remains linked to the corresponding timestamp in the audio recording.

The research material has become accessible, but it has not yet been interpreted.

---

## 184. Evidence Extraction

The Evidence Extractor identifies several observations.

Examples include:

Observed Behaviour

```text
The participant looked at the product image before reading the location code.
```

Participant Statement

```text
"I immediately knew where to start."
```

Observed Behaviour

```text
The participant completed the task without asking for assistance.
```

Each observation becomes an individual Evidence object.

Every Evidence object remains linked to:

- transcript segment
- timestamp
- participant
- Source

---

## 185. Pattern Detection

The newly accepted Evidence is compared against existing Evidence within the Research Round.

Research OS discovers similar observations from previous participants.

Instead of creating isolated findings, the system strengthens an existing Pattern.

The Pattern now becomes:

```text
Across seven participants, product imagery was consistently used before location codes.
```

The Pattern records:

- supporting Evidence
- participant diversity
- contexts
- confidence
- contradictory observations

No conclusions have been drawn yet.

---

## 186. Insight Synthesis

The Insight Synthesizer interprets the Pattern.

A proposed Insight is created.

```text
Visual product recognition provides shoppers with an intuitive starting point before they begin location-based navigation.
```

Supporting information is attached.

Supporting Patterns.

Supporting Evidence.

Applicability:

```text
New shoppers

Manual fulfillment centers
```

Confidence:

```text
Moderate
```

The Insight is still a proposal.

It has not yet become part of organizational knowledge.

---

## 187. Knowledge Curation

The Knowledge Curator compares the proposed Insight with Current Understanding.

An existing Insight already states:

```text
Visual guidance reduces onboarding effort.
```

Rather than creating duplicate knowledge, the Curator proposes:

```text
Refine existing Insight.
```

Changes include:

- additional supporting Evidence
- more precise wording
- increased confidence

A Change Proposal is created.

Because only confidence increases, no researcher review is required.

Current Understanding is automatically updated.

---

## 188. Opportunity Identification

Once Current Understanding has been updated, the Opportunity Agent searches for unmet user needs.

It identifies an Opportunity.

```text
Reduce the effort required for first-time shoppers to orient themselves.
```

The Opportunity remains solution-independent.

It does not recommend changing the interface.

It simply identifies an area where improvement appears valuable.

---

## 189. Recommendation Generation

Several Recommendations are proposed.

Example A

```text
Increase the prominence of product imagery.
```

Example B

```text
Introduce progressive navigation cues during onboarding.
```

Example C

```text
Delay detailed location information until shoppers become familiar with the environment.
```

Each Recommendation references:

- the Opportunity
- supporting Insights
- supporting Evidence
- expected behavioural outcome
- assumptions
- confidence

The product team later decides which Recommendation, if any, should be explored.

---

## 190. Round Closure

The Research Round eventually concludes.

Research OS records an immutable Round Knowledge snapshot.

The snapshot contains:

- Research Questions
- Evidence
- Patterns
- Insights
- Opportunities
- Recommendations
- Open Questions
- researcher decisions

The Round now becomes part of the organization's research history.

Nothing is overwritten.

---

## 191. Program Knowledge

The completed Research Round contributes to the broader Research Program.

The Program Knowledge now contains an updated understanding of manual picking.

Researchers can now answer questions such as:

- Has confidence increased over time?
- Which participant groups behave differently?
- Which Insights have remained stable?
- Which assumptions have been disproven?
- Which Opportunities have already been explored?

The Research Round contributes to long-term organizational learning without replacing earlier knowledge.

---

## 192. Deliverables

Several Deliverables are generated from the same underlying knowledge.

For example:

A research report.

A presentation.

An executive summary.

A workshop deck.

Each Deliverable presents the knowledge differently.

None changes the underlying knowledge.

If the Research Program continues to evolve, updated Deliverables can later be generated from the newer understanding.

---

## 193. Traceability

Months later, a Product Manager asks:

> **Why do we believe product imagery is important?**

The researcher follows the traceability chain.

```text
Recommendation
        ↓
Opportunity
        ↓
Insight
        ↓
Pattern
        ↓
Evidence
        ↓
Transcript
        ↓
Audio Recording
```

Within seconds, the original participant quote and recording can be inspected.

Nothing relies on memory or trust.

Everything remains explainable.

---

## 194. Continuous Learning

Several months later, another Research Round investigates experienced shoppers.

New Evidence suggests:

```text
Experienced shoppers rarely use product imagery.
```

Research OS does not replace the previous Insight.

Instead, it evolves it.

Current Understanding becomes:

```text
Visual product recognition provides an intuitive starting point for new shoppers.

Experienced shoppers continue relying on memorized location codes until visual navigation becomes familiar.
```

Both findings coexist.

Knowledge becomes richer rather than simpler.

---

## 195. The Complete Knowledge Journey

The entire lifecycle can now be viewed as one continuous process.

```text
Research Planning
        ↓
Research Round
        ↓
Source
        ↓
Source Representation
        ↓
Evidence
        ↓
Pattern
        ↓
Insight Proposal
        ↓
Knowledge Curation
        ↓
Current Understanding
        ↓
Opportunity
        ↓
Recommendation
        ↓
Round Knowledge
        ↓
Program Knowledge
        ↓
Deliverables
        ↓
New Research Round
        ↓
Current Understanding evolves
```

The output of one Research Round becomes the input for future learning.

Research never truly ends.

---

## 196. Core Principles

The complete Knowledge Pipeline is built upon a small number of enduring principles.

### Research is continuous

Knowledge evolves over time rather than being recreated for every project.

---

### Evidence precedes interpretation

Understanding should always be grounded in observable research.

---

### Knowledge remains explainable

Every conclusion should be traceable to its supporting research.

---

### Researchers remain in control

AI assists with processing, synthesis and organization.

Researchers remain responsible for organizational knowledge.

---

### Knowledge is the product

Reports, presentations and summaries communicate knowledge.

They are not the knowledge itself.

---

## 197. Final Summary

Research OS reimagines research as a continuous knowledge system rather than a sequence of isolated projects.

Instead of producing reports that gradually become outdated, the system continuously maintains an evolving understanding of users, products and domains.

Every stage of the Knowledge Pipeline contributes a distinct transformation:

```text
Source
        ↓
Source Representation
        ↓
Evidence
        ↓
Pattern
        ↓
Insight
        ↓
Current Understanding
        ↓
Opportunity
        ↓
Recommendation
        ↓
Program Knowledge
        ↓
Deliverables
```

Each transformation is:

- explicit
- traceable
- versioned
- reviewable
- explainable

Together they create a research architecture in which knowledge grows incrementally, remains grounded in evidence and continues to become more valuable with every new Research Round.

This continuous evolution of understanding is the central purpose of Research OS.

---

*End of Knowledge Pipeline*
