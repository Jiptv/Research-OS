# Architecture

This document defines the conceptual architecture of Research OS.

It describes how research is organized, how evidence becomes knowledge, how that knowledge evolves over time, and how AI and researchers collaborate.

The document intentionally focuses on durable system concepts rather than specific technologies, models, interfaces or implementation choices.

---

1. Purpose

Research OS is built around a fundamental belief:

Research is the continuous process of building understanding.

Most research tools are organized around projects, files and deliverables. A study starts, researchers collect data, a report is created, and the project is closed.

The resulting knowledge often becomes trapped inside:

* slide decks
* reports
* transcripts
* research repositories
* workshop boards
* meeting notes
* the memories of individual researchers

Future teams must search for these materials, interpret them again, or repeat research that has already been conducted.

Research OS uses a different architecture.

The primary product of research is not a document. It is an evolving and traceable understanding of users, products, environments and problems.

Reports and presentations are still valuable, but they are outputs of that understanding. They are not the understanding itself.

The architecture must therefore support four things particularly well:

1. Continuously ingesting new research material.
2. Turning raw material into structured and traceable knowledge.
3. Updating existing understanding without losing history or uncertainty.
4. Keeping researchers in control of interpretation and decisions.

Everything else follows from these requirements.

---

2. Architectural Position

Research OS is not primarily:

* a transcription tool
* a research repository
* a report generator
* a presentation generator
* an AI chat interface
* a project management tool

It may include capabilities associated with these products, but they are not its organizing model.

Research OS is a knowledge operating system for research.

It coordinates the complete lifecycle from research context and raw sources to evidence, insights, opportunities, decisions and deliverables.

Its first and primary use case is UX Research. The architecture should support that use case deeply before it is generalized to other disciplines.

The system is designed around three connected architectures:

### 2.1 Knowledge Architecture

How research knowledge is structured, connected, versioned and preserved.

### 2.2 Processing Architecture

How raw sources become evidence, insights and current understanding.

### 2.3 Collaboration Architecture

How specialized AI agents and human researchers divide responsibilities, review work and resolve uncertainty.

These three architectures are independent of any specific AI model or technical stack.

Models, databases and interfaces may change over time. The conceptual architecture should remain stable.

---

3. Architectural Principles

The following decisions guide the architecture.

### 3.1 Knowledge is the primary asset

The central purpose of Research OS is to create and maintain trustworthy research knowledge.

Documents, presentations and summaries are derived artifacts.

### 3.2 Current Understanding is the operational source of truth

Research OS maintains a living representation of what is currently understood within a Research Round.

Researchers should not need to reconstruct the state of the research from multiple documents.

### 3.3 Evidence remains separate from interpretation

Observations, interpretations, opportunities and recommendations are distinct objects.

The system never hides where evidence ends and interpretation begins.

### 3.4 Everything important is traceable

Every insight should be traceable to supporting evidence, and every piece of evidence should remain traceable to its source.

### 3.5 Knowledge evolves without erasing history

Research OS updates understanding incrementally while preserving previous states, rejected interpretations and contradictory evidence.

### 3.6 AI proposes; researchers decide

AI may extract, structure, synthesize, connect, critique and recommend.

Researchers remain accountable for research interpretation, prioritization and final decisions.

### 3.7 AI work is reviewed by AI before it reaches a researcher

Specialized agents challenge each other’s outputs. Researchers should primarily see meaningful changes and unresolved questions, not every intermediate processing step.

### 3.8 Uncertainty is represented, not removed

Confidence, assumptions, contradictions, limitations and open questions are part of the knowledge model.

### 3.9 Administrative work should be minimized

The system should not require researchers to manually maintain duplicate documents, update multiple repositories or repeatedly restructure the same material.

### 3.10 Research Rounds create boundaries without fragmenting knowledge

A Research Round provides a coherent scope and a stable historical snapshot.

Program Knowledge connects learning across rounds so that future research does not start from zero.

---

4. Architecture at a Glance

Research OS can be understood through the following high-level structure:

Research Program
```
```
```
```
│
├── Project Context
│
├── Research Round
│   │
│   ├── Research Context
│   ├── Research Questions
│   ├── Sources
│   ├── Evidence
│   ├── Insight Cards
│   ├── Current Understanding
│   ├── Review Queue
│   └── Deliverables
│
├── Research Round
│   └── ...
│
└── Program Knowledge
    ├── Confirmed cross-round insights
    ├── Historical development
    ├── Contradictions
    ├── Open questions
    └── Linked round knowledge
```

```
Within an active Research Round, knowledge flows through the following pipeline:

Sources
```
```
   ↓
Source Intake
   ↓
Evidence Extraction
   ↓
Evidence
   ↓
Pattern Detection
   ↓
Insight Synthesis
   ↓
Quality Critique
   ↓
Current Understanding
   ↓
Meaningful Change Detection
   ↓
Review Queue
   ↓
Researcher Decision
```
```
```

```
When the researcher closes the round:

Current Understanding
```
```
```
```
   ↓
Round Snapshot
   ↓
Research Documentation
```
```
Presentation Preparation
Design & Product Recommendations
```
```
   ↓
Program Knowledge Linking
```
```
```

```
This creates a distinction between two modes:

Active research

Sources are continuously added and Current Understanding continues to change.

Closed research

The round becomes a stable historical snapshot, deliverables are created, and its knowledge can be connected to the broader program.

---

## Part I — Knowledge Architecture

5. Research Program

A Research Program represents an ongoing product, domain, service or problem space in which knowledge accumulates over time.

Examples include:

* Fulfillment Operations
* Workflow Tools
* Customer Messaging
* Field Operations
* Workforce Experience

A program may exist for months or years. It does not end when an individual study ends.

The program provides continuity across multiple research efforts.

A Research Program contains:

* Project Context
* Research Rounds
* Program Knowledge
* shared terminology
* enduring research questions
* long-term assumptions
* relevant product and operational context

The program is the stable container around changing research activity.

### 5.1 Project Context

Project Context contains information that is useful across research rounds.

Examples include:

* product purpose
* primary users
* environments of use
* important workflows
* product terminology
* business and operational constraints
* known stakeholders
* historical product decisions
* existing product principles
* enduring areas of uncertainty
* stakeholder priorities and constraints
* product, strategy and research frameworks
* historical research documents and presentations
* recurring meeting context that affects how research should be framed

Project Context helps AI interpret incoming sources correctly.

It is context, not evidence.

Statements in Project Context may be based on known facts, existing documentation or researcher input, but they should not automatically be used as proof for research insights.

Project Context may be created and updated from project-level Sources.

Project-level Sources are raw inputs that belong to the Research Program rather
than to a single Research Round. They may include slide decks, stakeholder
interviews, meeting recordings, product documentation, research documents,
frameworks, strategy material, roadmaps, previous reports and operational
manuals.

The system processes these Sources through the same intake and representation
discipline as round Sources: the original material remains immutable, derived
representations remain traceable, and proposed context changes require review.

Project-level Sources may inform:

* Project Context
* shared terminology
* durable assumptions
* stakeholder and organizational constraints
* future Research Context proposals
* interpretation of round Sources

They should not directly create Round Evidence, Patterns or Insights.

If a project-level Source contains prior research evidence, Research OS should
preserve that provenance explicitly. The material can inform Project Context or
Program Knowledge only through a reviewed proposal that records whether the
claim is imported context, prior accepted knowledge, an assumption or evidence
that remains traceable to its original study.

### 5.2 Why Programs exist

Without a Program layer, every study becomes isolated.

The same user group may be described differently in multiple projects. Insights may be duplicated. Contradictions may remain undiscovered. Researchers may repeat the same foundational work.

The Program creates a persistent knowledge boundary across studies while still allowing each Research Round to retain its own purpose, evidence and conclusions.

---

6. Research Round

A Research Round is a bounded period of research within a Research Program.

Examples include:

* initial discovery
* workflow observation
* concept validation
* usability testing
* pilot evaluation
* rollout evaluation
* follow-up research

A Research Round is organized around a specific objective or set of research questions.

It contains:

* Research Context
* Research Questions
* Sources
* Evidence
* Insight Cards
* Current Understanding
* Review Queue
* Deliverables
* a closure state

### 6.1 Why Research Rounds exist

Continuous knowledge requires boundaries.

Without boundaries, the system would struggle to answer:

* Which evidence belonged to a particular study?
* What did the team understand at a specific point in time?
* Which conclusions informed a decision?
* When was a deliverable created?
* Which later findings changed earlier knowledge?

A Research Round creates a coherent historical unit.

It separates exploration from communication.

While a round is active, knowledge is expected to change frequently. Sources may still be incomplete, interpretations may conflict and confidence may shift.

When a researcher closes the round, Research OS creates a stable snapshot of its final Current Understanding.

That snapshot does not prevent future knowledge from evolving. It records what was understood at the close of that specific round.

### 6.2 Research Round states

A Research Round may have the following conceptual states:

Planned
```
```
```
```
   ↓
Active
   ↓
Ready for Closure
   ↓
Closed
```
```
```

```
Planned

The research objective, questions and intended methods are being prepared.

Active

Sources are being added and Current Understanding is continuously evolving.

Ready for Closure

The system believes the research questions are sufficiently addressed or that no meaningful new knowledge is currently emerging.

This is a suggestion, not an automatic decision.

Closed

The researcher has explicitly closed the round. Its final knowledge state becomes an immutable historical snapshot.

A closed round may receive annotations or corrections, but its original state should never be silently rewritten.

### 6.3 Round Knowledge

The final knowledge state of a closed Research Round is referred to as Round Knowledge.

Round Knowledge contains:

* final Insight Cards
* confidence at closure
* open questions
* unresolved contradictions
* opportunities
* research limitations
* links to evidence
* links to generated deliverables

Round Knowledge is immutable as a historical record.

New evidence should normally enter a new Research Round rather than changing a completed one.

---

7. Research Context and Research Questions

Research processing should not begin without context.

AI can extract language and behavior from sources, but it cannot determine relevance without understanding what the research is trying to learn.

Every Research Round therefore includes Research Context.

Research Context may contain:

* background
* problem statement
* research objective
* known constraints
* target users
* product or concept being studied
* intended research method
* stakeholder needs
* prior knowledge
* assumptions
* explicit exclusions

Research Questions define what the round aims to answer.

Examples:

* How do experienced shoppers interpret the shelf visualization?
* Which elements help new shoppers locate products?
* When do users fall back on the location code?
* What creates uncertainty during multi-picks?

Research Questions serve several functions:

* they guide source processing
* they help prioritize evidence
* they structure Current Understanding
* they expose unanswered areas
* they provide closure criteria
* they prevent synthesis from becoming an unbounded summary

AI may propose improvements, missing questions or subquestions.

The researcher owns the final research questions.

Research Context may be prefilled or improved from Project Context, but the
round keeps its own framing. Changes to Project Context do not automatically
rewrite active or closed Research Context.

---

8. Sources

Sources are the raw inputs of Research OS.

Supported source types may include:

* audio recordings
* video recordings
* interview transcripts
* meeting transcripts
* observation notes
* usability test notes
* survey responses
* workshop outputs
* screenshots
* photographs
* presentations
* research documents
* product documentation
* field notes
* researcher notes

### 8.1 Source immutability

A source represents what entered the system.

The original source should remain immutable.

Research OS may create derived representations such as:

* transcripts
* timestamps
* image descriptions
* speaker segmentation
* extracted text
* metadata
* translated text

These derived representations remain linked to the original.

Corrections may be stored as revisions, but the original material should remain available.

This protects traceability.

### 8.2 Source metadata

Each source should contain sufficient metadata to support interpretation and retrieval.

Depending on the source, this may include:

* title
* source type
* date
* Source scope
* Research Program
* Research Round
* participant or contributor
* researcher
* language
* location
* session type
* method
* duration
* consent or access classification
* processing status

### 8.3 Source roles

Not every source has the same evidentiary role.

Research OS should distinguish at least between:

Primary research sources

Direct records of user behavior or statements.

Examples:

* interviews
* observations
* usability tests
* survey responses

Supporting sources

Material that provides context but is not direct user evidence.

Examples:

* product documentation
* business requirements
* existing slide decks
* operational manuals

Researcher Notes

Ideas, interpretations, questions, reflections and guidance added by the researcher.

Researcher Notes are valuable, but they are not evidence.

Project Context sources

Material that informs the broader Research Program rather than a single round.

Examples:

* stakeholder interviews
* meeting recordings
* strategy decks
* product frameworks
* historical research reports
* product or operational documentation

Project Context sources may produce Project Context proposals. They do not
produce Round Evidence unless the researcher explicitly imports traceable prior
evidence into a round or Program Knowledge workflow.

They may guide:

* what the AI should examine
* which contradictions matter
* which assumptions to challenge
* what the researcher believes may be emerging
* what to investigate next

They may not be cited as proof that an insight is true.

---

9. Evidence

Evidence consists of discrete observations extracted from sources.

Evidence is the smallest traceable research unit in the system.

Examples:

Participant 04 first looked at the product image before scanning the shelf.

Three experienced shoppers returned to the full location code when it became available.

The participant stated that the product image helped when items were misplaced.

Evidence should describe what happened without prematurely explaining why it happened.

### 9.1 Evidence structure

An Evidence object may contain:

* evidence statement
* source reference
* precise source location
* participant or contributor
* research question relevance
* evidence type
* context
* extraction confidence
* method-specific metadata
* tags
* researcher corrections

### 9.2 Evidence types

Evidence may represent:

* observed behavior
* participant statement
* task outcome
* error
* workaround
* preference
* emotional response
* environmental condition
* interaction pattern
* quantitative result
* contradiction
* researcher-observed event

Evidence types help method specialists interpret data appropriately.

A participant preference is not equivalent to observed behavior. A quote is not automatically proof of actual behavior. A task failure should not be interpreted in isolation from prototype limitations.

### 9.3 Atomic evidence

Evidence should be sufficiently atomic to be reused.

A single evidence object should normally express one observation.

This allows the same evidence to support multiple insights without duplicating or rewriting it.

### 9.4 Evidence quality

Research OS should evaluate evidence quality without hiding weaker evidence.

Relevant factors may include:

* directness
* clarity
* source completeness
* method fit
* participant relevance
* prototype fidelity
* environmental validity
* repetition
* independence
* possible researcher influence

Quality signals inform confidence but do not automatically remove evidence.

---

10. Patterns

Patterns are recurring relationships across multiple pieces of evidence.

Examples:

* new shoppers repeatedly rely on visual cues
* experienced shoppers repeatedly translate visuals back into location codes
* the product image is used for validation when shelves are imperfect
* quantity information is overlooked during multi-picks

Patterns are descriptive groupings.

They indicate that related evidence exists, but they do not yet explain significance or causality.

Patterns may be:

* proposed automatically
* created by researchers
* merged
* split
* challenged
* retired

Patterns are useful intermediate structures between evidence and insights.

They reduce the risk that AI jumps from individual observations directly to broad conclusions.

---

11. Insight Cards

An Insight Card is the fundamental unit of interpreted knowledge in Research OS.

Insight Cards connect evidence to meaning.

A card should be understandable independently while remaining fully traceable to its supporting material.

### 11.1 Insight Card structure

Each Insight Card contains:

Insight

A concise statement of what has been learned.

Why this matters

The consequence for users, the product, the operation or the research objective.

Supporting evidence

Evidence that strengthens the insight.

Contradictory evidence

Evidence that weakens, limits or complicates the insight.

Representative quotes

Selected quotes that communicate the participant perspective without replacing broader evidence.

Research questions

Questions the insight helps answer.

Open questions

What remains unknown.

Opportunities

Potential areas for product, design, process or further research.

Confidence

The current strength of the insight.

Status

The current lifecycle state of the card.

History

How the insight has changed over time.

### 11.2 Observation versus insight

An Insight Card should not merely restate an observation.

Observation:

Six participants looked at the product image before the shelf code.

Insight:

Product recognition is often the first orientation strategy, suggesting that the product image reduces the effort required to begin a pick.

The first statement describes evidence.

The second interprets its meaning.

Research OS should preserve both and keep their relationship explicit.

### 11.3 Insight Card lifecycle

An Insight Card may move through states such as:

Proposed
```
```
```
```
   ↓
Under Review
   ↓
Active
   ↓
Strengthened / Weakened
   ↓
Superseded or Archived
```
```
```

```
Not every state transition requires manual approval.

Researchers should review transitions that meaningfully change the understanding of the research.

### 11.4 Main Insights

Main Insights are not separate knowledge objects.

They are clusters of related Insight Cards used to create a higher-level narrative.

For example:

Main Insight:
Visual guidance reduces the cognitive effort required to pick.
Related Insight Cards:
- New shoppers begin with the product image.
- Shelf visualization enables picking without precise code knowledge.
- Visual guidance supports recovery when shelves are imperfect.
- Experienced shoppers revert to learned code-based behavior.

AI may propose clusters based on semantic relationships, shared evidence and common consequences.

The researcher confirms or changes the grouping.

This prevents the system from maintaining duplicate insight hierarchies.

---

12. Current Understanding

Current Understanding is the primary living artifact within an active Research Round.

It represents the best available interpretation of the research at the current moment.

It is not a static report.

It is a structured view over the current knowledge state.

### 12.1 Contents

Current Understanding may include:

* Research Questions
* Main Insight clusters
* Insight Cards
* opportunities
* contradictions
* open questions
* assumptions
* limitations
* confidence
* unresolved agent disagreements
* recent meaningful changes

### 12.2 Organization around research questions

Current Understanding should be organized primarily around what the study is trying to answer.

For each Research Question, the system can show:

* current answer
* contributing Insight Cards
* supporting evidence
* confidence
* unresolved contradictions
* remaining gaps

This prevents the system from becoming a generic collection of themes.

### 12.3 Continuous updating

Whenever a new source is processed, Research OS evaluates whether Current Understanding should change.

Possible outcomes include:

* no meaningful change
* add evidence to an existing insight
* strengthen confidence
* weaken confidence
* create a new insight
* merge related insights
* split an over-broad insight
* identify a contradiction
* create an open question
* identify a new opportunity
* supersede an existing interpretation

Current Understanding is updated incrementally.

The system should not regenerate the entire synthesis from scratch after every source unless a full reassessment is explicitly required.

Incremental updating preserves continuity and makes change explainable.

### 12.4 Change explanation

Every meaningful update should answer:

* What changed?
* What new evidence caused the change?
* Which previous understanding was affected?
* Why did the system make this proposal?
* How did confidence change?
* Does the researcher need to review it?

---

13. Confidence and Uncertainty

Confidence should be explicit but not falsely precise.

A confidence model should consider factors such as:

* quantity of supporting evidence
* quality of supporting evidence
* independence of observations
* participant diversity
* consistency across methods
* contradictory evidence
* relevance to the research question
* limitations of the study
* researcher confirmation

Confidence may be represented using understandable categories such as:

* Low
* Emerging
* Moderate
* Strong

The system should explain the reasoning behind a confidence level.

It should not present a mathematically precise score unless the underlying method genuinely supports that precision.

### 13.1 Contradictions

Contradictory evidence is not noise to be removed.

It may reveal:

* different user groups
* environmental differences
* changes over time
* method limitations
* incorrect assumptions
* multiple valid behaviors

Research OS should preserve contradictions and attempt to explain them.

Unresolved contradictions should remain visible in Current Understanding and may become future Research Questions.

### 13.2 Open questions

An open question represents a meaningful gap in understanding.

Open questions may originate from:

* incomplete evidence
* contradictory behavior
* agent critique
* researcher input
* an insight with limited applicability
* missing participant groups
* emerging product decisions

Open questions connect current knowledge to future research planning.

### 13.3 Assumptions

Assumptions should be explicitly labeled.

They may inform research or synthesis but should never be presented as evidence.

A future research round may strengthen, reject or replace an assumption.

---

14. Opportunities and Recommendations

Research OS separates Opportunities from Recommendations.

### 14.1 Opportunities

An Opportunity identifies an area in which the product, service, workflow or research could improve.

It is derived from one or more Insight Cards.

Example:

Help experienced shoppers transition from code-based navigation to visual guidance without removing access to familiar information.

An opportunity describes a problem space.

It does not prescribe a specific solution.

### 14.2 Design and Product Recommendations

A Recommendation proposes a possible response to an Opportunity.

Example:

Keep the location code available as secondary information while visually prioritizing the product image and shelf position.

Recommendations are hypotheses.

In the active Research Round pipeline, Recommendations are a living synthesis
layer before Deliverables. They use a lightweight two-step structure:

* What we learned
* What we should do

Recommendations may be grounded in accepted Insights, Patterns or Evidence. A
single strong Evidence item may support a Recommendation when it is important,
traceable and clearly labeled with appropriate confidence.

They should include:

* linked Opportunity when one exists
* linked Insight Cards, Patterns or Evidence
* supporting evidence or knowledge references
* risks
* assumptions
* unresolved questions
* confidence
* suggested validation

Recommendations do not become independent knowledge.

They remain traceable to the research knowledge or evidence that created them.

Recommendations must stay concrete enough to stand alone. They should not only
say that something should be clearer or better; they should state what was
unclear, useful, risky or actionable.

### 14.3 Why the distinction matters

An insight explains what has been learned.

An opportunity identifies where value may be created.

A recommendation proposes what the team might do.

Keeping these layers separate allows product teams to explore multiple solutions for the same underlying opportunity.

---

15. Program Knowledge

Program Knowledge represents confirmed knowledge that spans multiple Research Rounds.

It is not a continuously rewritten summary of every study.

It is a structured layer that connects stable or evolving insights across time.

### 15.1 Inputs

Each closed Research Round contributes its immutable Round Knowledge.

Research OS compares new Round Knowledge with existing Program Knowledge.

It may identify:

* supporting relationships
* repeated insights
* changed behavior
* contradictions
* shifts in confidence
* insights that apply to different contexts
* previous questions that are now answered
* previously stable knowledge that may be outdated

### 15.2 Linking rather than automatically merging

AI may propose that insights from different rounds represent the same underlying knowledge.

For example:

Round 1:
New shoppers rely on visual recognition.
Round 2:
First-day shoppers ignore precise location codes when product imagery is available.

The system may propose a connection.

The researcher decides whether to:

* link the insights
* merge them into Program Knowledge
* keep them separate
* define one as context-specific
* mark them as contradictory

Cross-round merging should not happen invisibly.

### 15.3 Program Insight history

A Program Insight should preserve its development across rounds.

Researchers should be able to see:

* when it first emerged
* which rounds supported it
* when its wording changed
* when confidence increased or decreased
* which contexts it applies to
* which evidence contradicts it
* whether it has been superseded

### 15.4 Program Knowledge is curated

Program Knowledge should remain valuable rather than merely comprehensive.

Not every minor Round Insight needs to become Program Knowledge.

The Knowledge Curator may propose additions, connections and clean-up.

The researcher confirms significant changes.

---

## Part II — Processing Architecture

16. End-to-End Knowledge Pipeline

Research OS processes each source through a defined pipeline:

Source
```
```
```
```
   ↓
Source Intake
   ↓
Extraction
   ↓
Evidence
   ↓
Method Interpretation
   ↓
Pattern Detection
   ↓
Insight Synthesis
   ↓
Quality Critique
   ↓
Agent Resolution
   ↓
Current Understanding Update
   ↓
Meaningful Change Detection
   ↓
Review Queue
```
```
```

```
Each stage has a distinct responsibility.

Separating stages prevents a single AI operation from silently transforming raw material into broad conclusions.

---

17. Source Intake

Source Intake prepares a source for processing.

Responsibilities include:

* identifying source type
* validating metadata
* linking the source to a Research Program and Research Round
* determining language
* identifying participants or speakers where possible
* detecting missing context
* creating derived representations
* classifying the source role
* flagging privacy or access concerns
* checking whether the source is complete enough to process

Source Intake should not create insights.

Its responsibility is to ensure later agents understand what they are working with.

---

18. Extraction

Extraction converts a source into processable material.

Depending on the source, this may include:

* transcription
* speaker separation
* timestamp alignment
* text extraction
* image or screenshot description
* document sectioning
* quote identification
* event identification
* participant action extraction
* environmental context extraction

The extraction stage should preserve location references so that all later knowledge remains traceable to the relevant passage, timestamp, page or image region.

---

19. Evidence Extraction

The Evidence Extractor proposes atomic evidence objects.

It should:

* distinguish behavior from statements
* distinguish facts from researcher interpretation
* preserve participant context
* link every observation to its source location
* avoid combining unrelated events
* identify evidence relevant to Research Questions
* retain potentially contradictory observations
* assign extraction confidence
* avoid drawing conclusions

The output is proposed evidence, not final interpretation.

Routine evidence proposals may be accepted automatically when confidence and source quality are sufficient.

Researchers should be able to correct or reject extracted evidence.

Corrections should improve future processing without changing the original source.

---

20. Method Interpretation

Different research methods produce different kinds of evidence.

A Method Specialist interprets evidence within the limitations of the method.

Examples:

Interview

A participant statement reflects what the participant reports or believes. It may not reflect actual behavior.

Usability test

Task behavior may be influenced by prototype fidelity, facilitation, artificial scenarios or limited exposure.

Field observation

Observed behavior may have high environmental validity but limited insight into participant reasoning.

Survey

Quantitative patterns may indicate prevalence but not necessarily explain motivation.

Workshop

Outputs may reflect stakeholder alignment, hypotheses or decisions rather than user evidence.

The Method Specialist helps prevent inappropriate generalization.

It may add:

* limitations
* method-specific confidence
* cautions
* alternative interpretations
* missing contextual information

---

21. Pattern Detection

Pattern Detection groups related evidence without yet creating final insights.

It may identify:

* repeated behaviors
* recurring workarounds
* differences between participant groups
* common errors
* sequence patterns
* environmental triggers
* repeated language
* outliers
* contradictions

Pattern proposals should remain inspectable.

Researchers should be able to see which evidence has been grouped and why.

---

22. Insight Synthesis

The Insight Synthesizer transforms evidence and patterns into proposed Insight Cards.

It should:

* answer the Research Questions
* explain why patterns matter
* avoid claims broader than the evidence supports
* distinguish observed behavior from inferred motivation
* incorporate contradictory evidence
* identify applicability and limits
* propose confidence
* create or update opportunities
* connect new findings to existing Insight Cards
* avoid duplicating knowledge

The Synthesizer should prefer updating existing knowledge over generating a new card whenever the evidence concerns the same underlying phenomenon.

---

23. Quality Critique

The Quality Critic independently reviews proposed changes.

It should challenge:

* unsupported claims
* over-generalization
* missing evidence
* causal language not supported by the method
* ignored contradictions
* duplicate insights
* unclear distinction between observation and interpretation
* inflated confidence
* recommendations presented as conclusions
* researcher notes being treated as evidence
* missing applicability conditions
* missing limitations

The Critic does not merely score quality.

It proposes concrete revisions or objections.

---

24. Agent Resolution

The Synthesizer and Critic should resolve routine disagreements before involving a researcher.

A possible loop is:

Synthesizer proposes
```
```
```
```
        ↓
Critic reviews
        ↓
Revision requested
        ↓
Synthesizer revises
        ↓
Critic re-evaluates
```
```
```

```
The loop should stop when:

* the Critic accepts the revision
* the agents agree that uncertainty must remain
* the disagreement requires human judgement
* a safe iteration limit is reached

The system should not optimize for artificial consensus.

A valid outcome may be:

Evidence supports two plausible interpretations. Researcher judgement is required.

Only unresolved or meaningful disagreements enter the Review Queue.

---

25. Current Understanding Update

After synthesis and critique, the Knowledge Curator proposes changes to Current Understanding.

The Curator decides where the new knowledge belongs.

Possible actions include:

* attach evidence to an existing card
* revise an Insight Card
* create a new card
* merge cards
* split a card
* change confidence
* add a contradiction
* create an open question
* create an Opportunity
* mark a card as superseded
* reorganize Main Insight clusters

The Curator should preserve history and explain each change.

---

26. Meaningful Change Detection

Not every processing event should interrupt a researcher.

Research OS therefore evaluates whether a proposed update is meaningful.

Meaningful changes may include:

* a new Insight Card
* a material change in confidence
* strong contradictory evidence
* a change to the answer of a Research Question
* a previously stable insight becoming uncertain
* a proposed merge or split
* an emerging participant segment
* a Recommendation becoming unsupported
* an important new Opportunity
* an unresolved agent disagreement
* evidence suggesting the round is ready for closure

Routine changes may include:

* another supporting quote
* minor wording improvements
* additional evidence that does not change confidence
* metadata corrections
* low-impact pattern refinements

Routine updates may happen automatically and remain visible in the change history.

Meaningful changes enter the Review Queue.

---

## Part III — Collaboration Architecture

27. Human–AI Responsibility Model

Research OS is designed around complementary responsibilities.

AI is responsible for

* ingesting sources
* structuring material
* extracting proposed evidence
* identifying patterns
* proposing insights
* checking traceability
* surfacing contradictions
* challenging reasoning
* tracking changes
* connecting knowledge
* drafting deliverables
* reducing administrative work

Researchers are responsible for

* defining research intent
* choosing methods
* ensuring ethical and appropriate research practice
* interpreting ambiguity
* evaluating applicability
* resolving meaningful disagreements
* confirming major insight changes
* prioritizing opportunities
* making recommendations accountable
* closing Research Rounds
* deciding what should influence product decisions

The system must never create the impression that AI owns the final research conclusion.

---

28. Specialized Agents

Research OS uses specialized agents with bounded responsibilities.

The conceptual agent set includes:

### 28.1 Research Planner

Helps define:

* research objective
* Research Questions
* methods
* participant groups
* source plan
* known assumptions
* success and closure criteria

### 28.2 Source Intake Agent

Classifies and prepares incoming sources.

### 28.3 Evidence Extractor

Creates traceable proposed evidence.

### 28.4 Method Specialist

Evaluates evidence in the context of the research method.

### 28.5 Insight Synthesizer

Creates and updates Insight Cards.

### 28.6 Quality Critic

Challenges the quality and validity of synthesis.

### 28.7 Opportunity Agent

Identifies Opportunities derived from accepted insights.

### 28.8 Program Linker

Identifies relationships between Round Knowledge and Program Knowledge.

### 28.9 Knowledge Curator

Maintains Current Understanding, clusters, links, history and knowledge quality.

### 28.10 Deliverable Editor

Transforms approved knowledge into coherent documentation and presentation preparation.

These agents are conceptual roles.

A technical implementation may combine several roles into one model invocation or separate one role into multiple services.

The architectural boundaries remain the same.

---

29. Review Queue

The Review Queue is the primary interface between researchers and AI-generated knowledge changes.

Researchers should not need to inspect every source processing step.

The Review Queue contains only items requiring judgement.

Examples include:

* proposed new insight
* significant insight revision
* merge or split proposal
* unresolved contradiction
* disputed confidence level
* opportunity proposal
* cross-round knowledge merge
* recommendation proposal
* readiness-to-close suggestion

Each review item should include:

* proposed change
* previous state
* supporting evidence
* contradicting evidence
* agent reasoning
* confidence
* reason human review is required
* available actions

Possible researcher actions include:

* approve
* revise
* reject
* defer
* request deeper analysis
* mark as unresolved
* create a Researcher Note

The Review Queue should communicate decisions, not expose internal AI complexity unnecessarily.

---

30. Approval Model

Not every object requires explicit approval.

Research OS should use a risk-based approval model.

Automatic

Low-risk, traceable and reversible actions.

Examples:

* metadata extraction
* quote linking
* duplicate detection
* additional supporting evidence
* minor wording normalization

Review required

Actions that materially affect understanding.

Examples:

* new Insight Card
* confidence change
* merge or split
* contradiction resolution
* Program Knowledge update
* Recommendation creation
* closure proposal

Researcher-only

Actions that define the official state of the research.

Examples:

* final interpretation of unresolved ambiguity
* confirmation of major Program Knowledge merges
* closure of a Research Round
* acceptance of final Recommendations
* deletion or correction of sensitive material

This approach preserves researcher control without turning the system into a constant approval workflow.

---

31. Researcher Guidance

Researchers may guide the system using Researcher Notes.

Examples:

* “Pay particular attention to how experienced shoppers use the code.”
* “The prototype failed to show error feedback in this session.”
* “Do not interpret stakeholder workshop output as user evidence.”
* “I suspect that left/right aisle orientation is a larger issue than the transcript suggests.”
* “Compare this with the previous Control Room study.”

Researcher Guidance influences processing and prioritization.

It must remain distinguishable from evidence and should be visible in the reasoning history where relevant.

---

32. Transparency and Explainability

Research OS should make its outputs understandable without exposing raw chain-of-thought reasoning.

For every important conclusion, the system should provide a concise explanation of:

* what it concluded
* which evidence supports it
* which evidence complicates it
* which method limitations apply
* what changed
* how confident the system is
* which agent or researcher approved the change

The goal is accountable reasoning, not opaque automation.

---

## Part IV — Deliverable Architecture

33. Deliverables as Projections

Deliverables are projections of approved knowledge into a specific communication format.

They are not independent knowledge stores.

Research OS supports four primary outputs:

1. Current Understanding
2. Research Documentation
3. Presentation Preparation
4. Design & Product Recommendations

### 33.1 Current Understanding

A living, continuously updated view used while the Research Round is active.

### 33.2 Research Documentation

A stable record of the completed research.

It may include:

* background
* objective
* method
* participants
* limitations
* answers to Research Questions
* Main Insights
* supporting evidence
* opportunities
* open questions
* appendix and traceability

### 33.3 Presentation Preparation

A plain-text presentation structure designed for a researcher or collaborator to turn into a presentation.

It may include, per slide:

* slide purpose
* key message
* supporting points
* suggested evidence or quote
* suggested visual
* speaker context

Research OS prepares the narrative. It does not need to become a full presentation editor in the first implementation.

### 33.4 Design & Product Recommendations

A structured set of Recommendations linked to Opportunities and insights.

Recommendations should include their rationale, expected effect, risks and validation needs.

---

34. Closing a Research Round

Deliverables are generated after a researcher explicitly closes a Research Round.

Before closure, the system may show previews or draft structures, but these should remain clearly labeled as provisional.

Closing triggers:

1. Validation of unresolved review items.
2. Creation of the immutable Round Knowledge snapshot.
3. Generation of Research Documentation.
4. Generation of Presentation Preparation.
5. Confirmation of Recommendations.
6. Comparison with existing Program Knowledge.
7. Creation of proposed cross-round links.
8. Preservation of the round’s final state and change history.

Closure is a deliberate research action.

AI may recommend closure when:

* Research Questions have credible answers
* new sources no longer change understanding materially
* confidence is sufficient for the intended decision
* remaining gaps are explicitly documented
* unresolved contradictions have been accepted or converted into open questions

AI may not close the round automatically.

---

35. Regeneration and Versioning

Because deliverables are derived from knowledge, they can be regenerated.

However, historical versions should remain available.

For each generated deliverable, Research OS should preserve:

* generation date
* originating Current Understanding or Round Knowledge version
* template or output settings
* researcher edits
* final approved version
* links to relevant decisions

A deliverable may be manually refined for communication.

These edits should not silently rewrite the underlying knowledge.

When a manual change introduces a new interpretation, the system should allow the researcher to propose that change back into Current Understanding or Program Knowledge.

---

## Part V — Knowledge Evolution

36. Incremental Knowledge Development

Research OS should become more useful with every source and Research Round.

The system must avoid two failure modes:

Constant regeneration

Recreating the entire synthesis after every source causes instability, makes changes difficult to explain and may cause previously accepted knowledge to disappear.

Permanent accumulation

Adding new insights without updating or retiring existing ones creates duplication and makes the knowledge base increasingly noisy.

Research OS instead uses incremental knowledge development.

New evidence is compared with existing understanding.

The system makes the smallest meaningful change required.

---

37. Knowledge Change Types

Knowledge may evolve through several explicit change types:

Strengthen

New evidence supports an existing insight.

Weaken

New evidence challenges an existing insight or reduces its applicability.

Refine

The core insight remains valid, but wording, scope or conditions become clearer.

Merge

Multiple cards appear to describe the same underlying phenomenon.

Split

A card is too broad and contains multiple distinct insights.

Contradict

Evidence supports a competing interpretation.

Supersede

A newer insight better represents the current understanding.

Archive

An insight is no longer active but remains historically relevant.

Reopen

Previously stable knowledge becomes uncertain because of new evidence.

Each change should preserve a relationship to the previous state.

---

38. Historical Integrity

History should be preserved at three levels:

Source history

Original sources and corrected derivatives.

Insight history

All meaningful versions and status changes of Insight Cards.

Round history

The final knowledge state at the closure of each Research Round.

This allows researchers to reconstruct:

* what was known
* when it was known
* why it changed
* which evidence caused the change
* which decisions were based on it

Historical integrity is essential for long-term trust.

---

39. Cross-Round Learning

Future Research Rounds should begin with relevant existing knowledge.

When a new round is created, Research OS may propose:

* relevant Program Insights
* previously unanswered questions
* earlier assumptions
* applicable methods
* known participant segments
* historical contradictions
* Recommendations awaiting validation
* previous evidence that should be reconsidered

The researcher decides what becomes part of the new Research Context.

This prevents old knowledge from dictating new research while ensuring that the team does not unnecessarily start from zero.

---

## Part VI — Domain Relationships

40. Conceptual Domain Model

The main domain relationships are:

Research Program
```
```
```
```
│
├── has one Project Context
│
├── contains many Research Rounds
│
└── maintains Program Knowledge
        │
        └── contains Program Insights
                │
                └── links to Round Insight Cards
Research Round
│
├── belongs to one Research Program
├── has one Research Context
├── has many Research Questions
├── contains many Sources
├── contains many Evidence objects
├── contains many Patterns
├── contains many Insight Cards
├── has one Current Understanding
├── contains Review Items
├── produces one immutable Round Knowledge snapshot
└── produces Deliverables
Source
│
├── belongs to one Research Round
├── may have derived representations
└── supports many Evidence objects
Evidence
│
├── belongs to one Source
├── may answer multiple Research Questions
├── may support multiple Insight Cards
└── may contradict multiple Insight Cards
Insight Card
│
├── belongs to one Research Round
├── links to supporting Evidence
├── links to contradictory Evidence
├── answers Research Questions
├── may create Opportunities
├── belongs to Main Insight clusters
├── has Confidence
├── has Status
└── maintains History
Opportunity
│
├── derives from one or more Insight Cards
└── may lead to multiple Recommendations
Recommendation
│
├── responds to an Opportunity
├── links to supporting Insight Cards
└── includes assumptions, risks and validation needs
```

```
---
```
```

41. Knowledge Flow

Knowledge flows forward:

Source
```
```
```
```
   ↓
Evidence
   ↓
Pattern
   ↓
Insight Card
   ↓
Current Understanding
   ↓
Opportunity
   ↓
Recommendation
   ↓
Deliverable
```
```
```

```
Traceability flows backward:

Recommendation
```
```
```
```
   ↓
Opportunity
   ↓
Insight Card
   ↓
Evidence
   ↓
Source
```
```
```

```
Historical knowledge flows upward:

Research Round
```
```
```
```
   ↓
Round Knowledge
   ↓
Program Knowledge
```
```
```

```
Research planning flows back downward:

Program Knowledge
```
```
```
```
   ↓
New Research Context
   ↓
New Research Questions
   ↓
New Research Round
```
```
```

```
This creates a continuous research loop rather than a linear project lifecycle.

---

## Part VII — System Boundaries

42. What Research OS Owns

Research OS owns:

* research context
* Research Questions
* source processing
* evidence structures
* insight structures
* traceability
* knowledge evolution
* confidence and uncertainty
* cross-round linking
* deliverable generation
* research decision history

43. What Research OS Does Not Automatically Own

Research OS should not automatically become:

* the canonical product analytics platform
* the product backlog
* the design file repository
* the organization’s general document management system
* the participant recruitment platform
* the final product decision-maker
* the replacement for researcher ethics and judgement

It may integrate with these systems.

Integration should not blur responsibility.

---

## Part VIII — Architectural Consequences

44. Consequences of Knowledge-First Architecture

Choosing knowledge as the primary asset has several consequences.

### 44.1 There is no independent report truth

A report cannot silently diverge from Current Understanding.

### 44.2 Editing a deliverable does not automatically edit knowledge

Communication choices and research conclusions remain separate.

### 44.3 Sources must remain available

Deleting traceability would undermine trust in all downstream knowledge.

### 44.4 Insight Cards require stable identifiers

Insights must be updated and linked over time rather than recreated as anonymous text.

### 44.5 History must be versioned

The system must explain how knowledge changed.

### 44.6 AI outputs must be structured

Free-form summaries alone are insufficient for a durable knowledge system.

---

45. Consequences of Continuous Research

Continuous research means:

* sources can be added over time
* Current Understanding updates progressively
* knowledge changes must be explainable
* researchers need change summaries
* Research Rounds require explicit closure
* Program Knowledge must distinguish current and historical interpretations
* new research should start from relevant prior knowledge

---

46. Consequences of Human Control

Keeping researchers in control means:

* significant changes require review
* closure is a human decision
* Program Knowledge merges require confirmation
* uncertainty may remain unresolved
* AI must provide evidence and rationale
* researchers can override AI
* researcher changes remain visible in history
* the system must be useful even when the researcher disagrees with its synthesis

---

47. Consequences of Multi-Agent Collaboration

Using specialized AI roles means:

* responsibilities must remain bounded
* outputs must use shared structures
* critique should occur before human review
* disagreements must be represented explicitly
* agents may be replaced without changing the domain architecture
* no agent should directly rewrite the source of truth without governed change handling

---

## Part IX — Future Extensibility

48. UX Research as the First Use Case

The first implementation should be deeply optimized for UX Research.

This includes support for:

* interviews
* usability testing
* field observation
* concept validation
* workshops
* multi-method synthesis
* product and design opportunities
* presentation preparation
* continuous product knowledge

The architecture should not be prematurely generalized at the expense of a strong UX Research workflow.

---

49. Potential Future Domains

The same architecture may later support:

* Product Discovery
* Customer Research
* Operations Research
* Employee Research
* Market Research
* Service Design
* Voice of Customer programs

These domains share the core flow:

Sources
```
```
```
```
   ↓
Evidence
   ↓
Interpretation
   ↓
Current Understanding
   ↓
Decisions and Deliverables
```
```
```

```
Their methods, evidence types and deliverables may differ.

The core architecture should remain stable.

---

50. Model and Technology Independence

Research OS should not depend conceptually on one AI provider or model.

Different stages may use:

* large language models
* speech models
* vision models
* retrieval systems
* deterministic rules
* statistical methods
* human review

The correct tool should be selected for each responsibility.

The architecture defines the work that must happen, not which provider must perform it.

---

## Part X — Summary

Research OS is organized around a continuous cycle of learning.

A Research Program preserves long-term context.

Research Rounds create coherent boundaries around individual research efforts.

Sources are transformed into atomic Evidence.

Evidence forms Patterns.

Patterns support living Insight Cards.

Insight Cards build Current Understanding.

AI agents synthesize, critique and curate that understanding.

Meaningful changes are presented to researchers through a Review Queue.

Researchers retain authority over interpretation, major knowledge changes and Research Round closure.

Closing a round creates immutable Round Knowledge and generates documentation, presentation preparation and Recommendations.

Knowledge from completed rounds contributes to Program Knowledge, which informs future research without replacing historical context.

The architecture can therefore be summarized as:

Research continuously creates evidence.
Evidence continuously updates understanding.
Understanding is challenged before it is accepted.
Researchers remain in control.
History is preserved.
Documentation is generated from knowledge.
Every new Research Round builds on what came before.

The purpose of Research OS is not to automate research.

Its purpose is to make research knowledge more continuous, trustworthy, traceable and useful over time.
