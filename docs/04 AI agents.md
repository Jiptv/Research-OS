# AI Agents

> This document defines the AI agent architecture of Research OS.
>
> It describes the specialized AI roles that support researchers, the responsibilities and boundaries of each agent, how agents collaborate, which actions they may perform automatically, and where human judgement is required.
>
> The agent architecture implements the principles and domain structures defined in:
>
> - `01 Research Principles.md`
> - `02 Architecture.md`
> - `03 Domain Model.md`

---

## 1. Purpose

Research OS uses AI to reduce the effort required to turn research material into trustworthy and reusable knowledge.

AI supports activities such as:

- preparing research
- processing Sources
- extracting Evidence
- identifying Patterns
- creating and updating Insight Cards
- surfacing contradictions
- maintaining Current Understanding
- linking knowledge across Research Rounds
- drafting Opportunities and Recommendations
- generating research Deliverables

These activities require different forms of reasoning.

A single general-purpose agent that performs the entire process would create several risks:

- Evidence and interpretation may be mixed
- unsupported claims may go unchallenged
- method limitations may be ignored
- broad conclusions may be created from isolated observations
- contradictions may be removed instead of preserved
- changes may become difficult to explain
- researchers may receive too much unstructured AI output
- one model failure may affect the entire knowledge pipeline

Research OS therefore uses specialized AI agents with bounded responsibilities.

Each agent performs a specific part of the research process.

Agents collaborate through shared domain objects rather than through unstructured conversation alone.

The purpose of the agent architecture is not to imitate a team of human researchers.

Its purpose is to create a governed system in which:

- responsibilities are explicit
- outputs are structured
- reasoning is challenged
- changes are traceable
- uncertainty remains visible
- researchers remain in control

---

## 2. Agent Architecture Principles

The following principles apply to all AI agents.

### 2.1 Agents operate on domain objects

Agents should create, read and propose changes to structured entities such as:

- Research Context
- Research Questions
- Sources
- Evidence
- Patterns
- Insight Cards
- Confidence Assessments
- Opportunities
- Recommendations
- Review Items
- Program Insights
- Deliverables

Free-form text may be used during processing, but persistent outputs must map to the Domain Model.

### 2.2 Every agent has a bounded responsibility

An agent should only perform tasks within its defined role.

For example:

- the Evidence Extractor identifies observations
- the Insight Synthesizer interprets those observations
- the Quality Critic challenges the interpretation
- the Knowledge Curator decides how the proposed knowledge relates to existing knowledge

These responsibilities should not be silently combined.

### 2.3 AI proposes; researchers decide

Agents may propose:

- new entities
- changes to entities
- confidence updates
- relationships
- Opportunities
- Recommendations
- Research Round closure

Researchers retain authority over meaningful research decisions.

### 2.4 Agents do not own the source of truth

No agent directly and silently rewrites Current Understanding, Round Knowledge or Program Knowledge.

Changes occur through governed workflows that preserve:

- the previous state
- the proposed state
- the reason for change
- supporting Evidence
- review requirements
- approval status

### 2.5 AI challenges AI

Important interpretive outputs should be reviewed by another agent before being presented to a researcher.

The purpose of critique is to detect:

- unsupported conclusions
- over-generalization
- ignored contradictions
- method misuse
- duplicate knowledge
- inflated confidence
- weak traceability
- assumptions presented as facts

### 2.6 Agents preserve uncertainty

Agents should not force ambiguous research into a single conclusion.

Valid outputs include:

- multiple plausible interpretations
- unresolved contradictions
- low-confidence findings
- explicit knowledge gaps
- requests for researcher judgement

### 2.7 Agents explain meaningful proposals

Every meaningful proposal should communicate:

- what is being proposed
- why it is being proposed
- which Evidence supports it
- which Evidence complicates it
- what changed from the previous state
- whether human review is required

### 2.8 Agent outputs are replaceable

The architecture should not depend on one model provider or implementation.

An agent is a conceptual responsibility.

It may be implemented using:

- one language model
- multiple model calls
- deterministic logic
- retrieval
- statistical analysis
- rules
- human input
- a combination of these

---

## 3. Agent System Overview

The conceptual agent system consists of the following roles:

1. Research Planner
2. Source Intake Agent
3. Source Processor
4. Evidence Extractor
5. Method Specialist
6. Pattern Detector
7. Insight Synthesizer
8. Quality Critic
9. Knowledge Curator
10. Opportunity Agent
11. Recommendation Agent
12. Program Linker
13. Deliverable Editor
14. Privacy and Governance Agent
15. Workflow Orchestrator

The main processing sequence is:

```text
Research Planner
       ↓
Source Intake Agent
       ↓
Source Processor
       ↓
Evidence Extractor
       ↓
Method Specialist
       ↓
Pattern Detector
       ↓
Insight Synthesizer
       ↓
Quality Critic
       ↓
Knowledge Curator
       ↓
Meaningful Change Detection
       ↓
Review Queue
       ↓
Researcher Decision
```

Additional agents operate around this core flow:

```text
Opportunity Agent
Recommendation Agent
Program Linker
Deliverable Editor
Privacy and Governance Agent
Workflow Orchestrator
```

---

## 4. Shared Agent Contract

Every agent follows a shared conceptual contract.

### 4.1 Inputs

An agent receives:

- a defined task
- the domain entities required for that task
- relevant Research Context
- relevant Project Context
- permissions
- processing constraints
- provenance information
- required output schema

An agent should receive only the information required for its responsibility.

### 4.2 Outputs

An agent produces one or more of the following:

- a proposed domain entity
- a proposed change to an entity
- an assessment
- a critique
- a relationship proposal
- a Review Item
- a structured explanation
- a no-change decision
- a processing failure or uncertainty state

### 4.3 Required output metadata

Every persistent agent output should contain:

- agent role
- agent version
- generation timestamp
- input entity references
- output confidence
- rationale summary
- Evidence references where applicable
- review requirement
- processing status

### 4.4 No-change outputs

Agents should be able to conclude that no meaningful action is required.

Examples:

- no new Evidence was found
- new Evidence only strengthens an existing Insight without changing confidence
- no relevant Program Knowledge connection exists
- a Source is insufficiently complete to process
- the existing wording remains more accurate than a proposed revision

A no-change result is a valid and useful output.

### 4.5 Failure handling

When an agent cannot perform its task reliably, it should return:

- failure type
- explanation
- affected entities
- missing information
- whether retry is appropriate
- whether researcher input is required

Agents should not invent missing information to complete a workflow.

---

# Part I — Research Planning Agents

## 5. Research Planner

The Research Planner helps researchers define and refine a Research Round.

It operates before and during research planning.

### 5.1 Purpose

The Research Planner reduces administrative effort while helping the researcher create a coherent research setup.

It supports, but does not own, research design.

### 5.2 Inputs

The Research Planner may use:

- Project Context
- Program Knowledge
- previous Research Rounds
- stakeholder questions
- product or design context
- researcher-provided goals
- known constraints
- intended decisions
- existing Researcher Notes

### 5.3 Responsibilities

The Research Planner may:

- clarify the research objective
- identify ambiguity in the problem statement
- propose Research Questions
- identify subquestions
- suggest participant groups
- suggest suitable methods
- identify relevant previous knowledge
- identify existing assumptions
- propose exclusions
- propose research risks
- propose closure criteria
- identify potential ethical or privacy concerns
- draft Research Context
- identify unanswered Program-level questions

### 5.4 Outputs

Possible outputs include:

- draft Research Context
- proposed Research Questions
- proposed methods
- participant group suggestions
- assumption list
- relevant Program Insight links
- research risk assessment
- closure criteria proposal
- planning Review Items

### 5.5 Boundaries

The Research Planner may not:

- make the final method decision
- determine that a participant group is ethically appropriate without researcher oversight
- create user Evidence
- present prior knowledge as new Evidence
- close or activate a Research Round automatically
- determine research success without reference to researcher intent

### 5.6 Review rules

Researcher approval is required for:

- final Research Context
- final Research Questions
- research methods
- participant groups
- scope exclusions
- closure criteria

Minor wording changes may be accepted automatically after the Research Round has been approved.

### 5.7 Example

Input:

```text
We want to understand how Internal Admin Tools should support users in fulfillment operations.
```

The Research Planner may propose:

```text
Research objective:
Understand how Internal Admin Tools are currently used in fulfillment operations, which user and operational needs are not sufficiently supported, and what future role the product should fulfill.

Proposed Research Questions:
- Which roles use Internal Admin Tools in fulfillment operations?
- Which workflows depend on it?
- Where do users rely on workarounds or other tools?
- Which information and decisions are most critical?
- How should the product support proactive rather than reactive work?
```

---

# Part II — Source Processing Agents

## 6. Source Intake Agent

The Source Intake Agent prepares an incoming Source for further processing.

### 6.1 Purpose

The agent ensures that every Source has sufficient context, metadata and classification before Evidence Extraction begins.

### 6.2 Inputs

The Source Intake Agent receives:

- original Source
- Research Round
- Research Context
- available metadata
- uploader information
- access and consent settings

### 6.3 Responsibilities

The Source Intake Agent may:

- identify Source Type
- identify Source Role
- detect language
- identify likely method
- validate required metadata
- identify participants or speakers where permitted
- detect missing information
- classify access level
- identify possible sensitive content
- select required processing steps
- create Source Processing tasks
- identify duplicate uploads
- link related Source files

### 6.4 Outputs

Possible outputs include:

- updated Source metadata
- Source classification
- processing plan
- missing-context warning
- duplicate Source proposal
- privacy Review Item
- Source Processing task

### 6.5 Boundaries

The Source Intake Agent may not:

- interpret the research findings
- create Insight Cards
- classify Researcher Notes as primary Evidence
- override access or consent rules
- delete duplicate files automatically
- merge Sources without preserving originals

### 6.6 Automatic actions

The agent may automatically:

- detect language
- classify common file types
- assign routine metadata
- queue transcription
- link an uploaded transcript to its corresponding audio recording
- identify exact duplicate files

### 6.7 Review required

Review is required when:

- Source Role is ambiguous
- personal or sensitive data is detected
- consent status is missing
- a Source may belong to another Research Round
- a Source appears incomplete
- a duplicate is similar but not exact
- participant identity is uncertain

---

## 7. Source Processor

The Source Processor converts original Sources into usable Source Representations.

### 7.1 Purpose

The agent creates structured and searchable representations while preserving a precise connection to the original Source.

### 7.2 Inputs

The Source Processor may receive:

- audio
- video
- transcript
- image
- screenshot
- presentation
- document
- survey export
- observation notes
- processing instructions

### 7.3 Responsibilities

Depending on Source Type, the Source Processor may:

- transcribe audio
- separate speakers
- align timestamps
- extract document text
- detect document structure
- describe images
- describe interface screenshots
- extract tables
- translate text
- normalize formatting
- create event sequences
- create structured survey records
- preserve original location mappings

### 7.4 Outputs

The Source Processor creates Source Representations such as:

- timestamped transcript
- speaker-separated transcript
- translated transcript
- extracted document text
- visual description
- structured observation sequence
- structured survey dataset

### 7.5 Boundaries

The Source Processor may not:

- create research interpretations
- remove uncertain passages without marking them
- silently correct participant statements
- replace original-language material with a translation
- summarize content in a way that loses Source traceability

### 7.6 Confidence

The processor should attach confidence or quality signals to uncertain elements such as:

- unclear speech
- uncertain speaker assignment
- unreadable text
- incomplete file extraction
- uncertain translation
- ambiguous visual elements

### 7.7 Review rules

Researcher review may be required when:

- transcript quality is too low
- important speakers cannot be separated
- specialist terminology is unclear
- a translation materially affects meaning
- visual interpretation is uncertain
- processing is incomplete

---

# Part III — Evidence Agents

## 8. Evidence Extractor

The Evidence Extractor identifies atomic, traceable observations in Sources.

### 8.1 Purpose

The Evidence Extractor turns Source material into reusable Evidence without prematurely interpreting its meaning.

Its job is to preserve research richness before later agents compress observations into Patterns, Findings and Insights. It should not reduce a long interview to one broad observation per topic or screen.

### 8.2 Inputs

The Evidence Extractor receives:

- Source
- Source Representations
- Research Context
- Research Questions
- participant metadata
- Source Role
- relevant Researcher Notes
- method information

### 8.3 Responsibilities

The Evidence Extractor may:

- identify observed behaviour
- identify participant statements
- identify task outcomes
- identify errors
- identify workarounds
- identify preferences
- identify environmental conditions
- identify interaction sequences
- identify emotional responses
- identify quantitative results
- identify absences or non-use
- select representative Quotes
- link Evidence to Research Questions
- identify potentially contradictory observations
- split one topic into separate Evidence items when the participant shows separate reactions, confusions, expectations, suggestions or changes in understanding

### 8.4 Evidence quality rules

The agent should:

- create one primary observation per Evidence object
- favor high recall with practical precision
- use neutral language
- preserve necessary context
- distinguish observation from inference
- distinguish participant statements from observed behaviour
- identify Source location
- identify participant where permitted
- record uncertainty
- avoid unsupported causal claims
- use salience and uncertainty instead of silently dropping useful but small observations

### 8.5 Outputs

Possible outputs include:

- proposed Evidence objects
- proposed Quote objects
- Evidence-to-Research-Question links
- extraction confidence
- insufficient Evidence warning
- Source quality warning
- low-density extraction warning when a long source produced unexpectedly few Evidence items

### 8.6 Boundaries

The Evidence Extractor may not:

- create final Insight Cards
- collapse several distinct observations into one broad finding
- explain why behaviour occurred unless directly stated and classified as a statement
- generalize across participants
- turn a Researcher Note directly into Evidence
- ignore observations because they conflict with existing knowledge
- remove outliers
- determine final confidence in an Insight

### 8.7 Automatic acceptance

Evidence may be accepted automatically when:

- the Source is clear
- the Source Role is unambiguous
- the observation is directly traceable
- the statement is neutral
- extraction confidence is high
- no sensitive interpretation is involved

### 8.8 Review required

Evidence should enter review when:

- behaviour and interpretation are difficult to separate
- Source quality is low
- the participant or speaker is uncertain
- a Researcher Note is being converted into researcher-observed Evidence
- the observation contains sensitive content
- the extraction materially affects an existing Insight
- multiple plausible Evidence statements exist

### 8.9 Example

Source passage:

```text
I normally look at the location code, but here I noticed the product picture first. It was faster because I immediately recognized the cereal.
```

Possible Evidence objects:

```text
Evidence 1:
The participant stated that they normally use the location code.

Type:
Participant Statement
```

```text
Evidence 2:
The participant looked at the product image before the location code in this task.

Type:
Observed Behaviour
```

```text
Evidence 3:
The participant stated that immediate product recognition made the task feel faster.

Type:
Participant Statement
```

The Evidence Extractor should not create:

```text
The product image is more efficient than the location code.
```

That is an interpretation requiring synthesis across Evidence.

---

## 9. Method Specialist

The Method Specialist assesses how the research method affects the meaning and strength of Evidence.

### 9.1 Purpose

The Method Specialist prevents Research OS from treating all Evidence as equally direct or reliable.

### 9.2 Method specializations

Research OS may use one general Method Specialist or specialized variants for:

- interviews
- usability tests
- field observations
- surveys
- diary studies
- workshops
- concept tests
- longitudinal research
- mixed-method research

### 9.3 Inputs

The Method Specialist receives:

- Research Context
- method
- Source
- Evidence
- facilitator notes
- prototype information
- participant information
- research setup
- known limitations

### 9.4 Responsibilities

The Method Specialist may:

- assess Evidence directness
- distinguish self-report from observed behaviour
- identify prototype fidelity risks
- identify facilitator influence
- assess environmental validity
- identify sample limitations
- identify task artificiality
- identify missing context
- propose Method Assessments
- propose Limitations
- advise how Evidence should affect confidence
- flag inappropriate generalization

### 9.5 Outputs

Possible outputs include:

- Method Assessment
- Limitation
- Evidence quality adjustment
- caution attached to Evidence
- synthesis guidance
- Review Item

### 9.6 Boundaries

The Method Specialist may not:

- reject Evidence solely because the method has limitations
- create a final Insight
- choose the research method retrospectively
- convert methodological caution into certainty
- determine business priority
- resolve contradictory Evidence without synthesis

### 9.7 Example

Evidence:

```text
Five participants stated that they would use the new filter every day.
```

Method Specialist assessment:

```text
This is stated future intent in a concept evaluation. It indicates perceived relevance but should not be treated as evidence of actual future usage.
```

---

## 10. Pattern Detector

The Pattern Detector identifies meaningful repetition, variation and relationships across Evidence.

### 10.1 Purpose

The Pattern Detector creates a descriptive intermediate layer between atomic Evidence and interpreted Insights.

### 10.2 Inputs

The Pattern Detector receives:

- accepted and proposed Evidence
- Research Questions
- participant segments
- Method Assessments
- existing Patterns
- existing Insight Cards
- relevant contexts

### 10.3 Responsibilities

The Pattern Detector may:

- group similar Evidence
- identify repeated behaviours
- identify recurring statements
- identify common errors
- identify recurring workarounds
- compare participant groups
- compare contexts
- identify behavioural sequences
- identify outliers
- identify negative cases
- identify contradictions
- update existing Patterns
- propose Pattern merges or splits

### 10.4 Outputs

Possible outputs include:

- new Pattern proposal
- updated Pattern
- participant-group comparison
- context comparison
- outlier set
- contradiction proposal
- no-pattern result

### 10.5 Boundaries

The Pattern Detector may not:

- claim why a Pattern exists
- create causal conclusions
- hide minority behaviour
- force all Evidence into a Pattern
- create a Pattern based solely on semantic wording when contexts differ
- determine final Insight confidence

### 10.6 Pattern quality rules

A Pattern should include:

- clear descriptive title
- linked Evidence
- participant coverage
- relevant contexts
- known exceptions
- creation rationale
- status

### 10.7 Review rules

Review may be required when:

- participant segmentation materially changes the finding
- a proposed Pattern merge combines different contexts
- an outlier may represent a separate user group
- the Pattern affects a high-confidence Insight
- Evidence membership is disputed

---

# Part IV — Synthesis Agents

## 11. Insight Synthesizer

The Insight Synthesizer creates and updates Insight Cards.

### 11.1 Purpose

The agent transforms Evidence and Patterns into meaningful interpretations that help answer Research Questions.

### 11.2 Inputs

The Insight Synthesizer receives:

- Research Context
- Research Questions
- Evidence
- Patterns
- Method Assessments
- Limitations
- existing Insight Cards
- existing Current Understanding
- relevant Researcher Notes
- relevant Program Knowledge

### 11.3 Responsibilities

The Insight Synthesizer may:

- propose new Insight Cards
- update existing Insight Cards
- connect Insights to Research Questions
- write `Why this matters`
- define applicability
- identify supporting Evidence
- identify contradicting Evidence
- propose representative Quotes
- identify Open Questions
- identify Assumptions
- propose Confidence Assessments
- propose Main Insight groupings
- identify when an Insight should be refined
- identify possible merges or splits
- identify when an Insight has been challenged
- identify possible Opportunities

### 11.4 Synthesis rules

The Synthesizer should:

- interpret rather than repeat Evidence
- avoid claims broader than the Evidence
- distinguish behaviour from reported preference
- account for Method Assessments
- preserve contradictions
- define context and applicability
- compare with existing Insights
- prefer updating an existing Insight over creating a duplicate
- explain why the Insight matters
- avoid recommendation language in the Insight statement
- preserve uncertainty

### 11.5 Outputs

Possible outputs include:

- proposed Insight Card
- Insight revision
- merge proposal
- split proposal
- Confidence Assessment proposal
- Main Insight Cluster proposal
- Open Question
- Assumption
- Limitation
- Opportunity candidate
- no-change result

### 11.6 Boundaries

The Insight Synthesizer may not:

- approve its own Insight
- silently change Current Understanding
- ignore contradicting Evidence
- convert stakeholder preference into user Insight
- treat Program Knowledge as new Evidence
- create final Recommendations
- close a Research Round
- merge Program Insights automatically

### 11.7 Example

Evidence Pattern:

```text
New shoppers frequently begin by matching the product image.
Experienced shoppers frequently return to the location code when it is visible.
```

Possible Insight:

```text
Visual guidance reduces the knowledge required to begin a pick, but experienced shoppers continue to rely on learned code-based behaviour when familiar location information is available.
```

Why this matters:

```text
A new design must support immediate visual orientation without making experienced shoppers feel that efficient familiar information has been removed.
```

---

## 12. Quality Critic

The Quality Critic independently evaluates proposed research interpretations.

### 12.1 Purpose

The Quality Critic reduces the risk that plausible-sounding AI output becomes accepted research knowledge without sufficient challenge.

### 12.2 Independence

The Critic should evaluate the proposal independently.

Where practical, it should not rely solely on the Synthesizer’s explanation.

It should inspect:

- proposed Insight
- supporting Evidence
- contradicting Evidence
- Patterns
- Method Assessments
- Research Questions
- relevant existing knowledge

### 12.3 Responsibilities

The Quality Critic may challenge:

- unsupported claims
- over-generalization
- vague wording
- hidden assumptions
- unsupported causal language
- method misuse
- weak Evidence coverage
- ignored Evidence
- missing contradictions
- duplicate Insights
- misleading confidence
- unclear applicability
- opportunity or recommendation language inside Insights
- Researcher Notes treated as Evidence
- selective Quote usage
- unjustified merging
- premature Program Knowledge links

### 12.4 Critique categories

The Critic may classify issues as:

- Traceability Issue
- Evidence Issue
- Interpretation Issue
- Method Issue
- Scope Issue
- Confidence Issue
- Contradiction Issue
- Duplication Issue
- Wording Issue
- Governance Issue

### 12.5 Outputs

Possible outputs include:

- Accept
- Accept with minor revision
- Revise
- Reject
- Human judgement required
- additional Evidence required
- split recommended
- merge not supported
- confidence adjustment recommended
- unresolved contradiction

### 12.6 Boundaries

The Quality Critic may not:

- rewrite Current Understanding directly
- reject an Insight merely because uncertainty exists
- force one interpretation when multiple are plausible
- prioritize business impact
- approve final research knowledge
- resolve ethical issues without researcher involvement

### 12.7 Critic explanation

Every critique should include:

- issue
- why it matters
- affected wording or relationship
- supporting domain references
- proposed correction
- severity
- whether human review is required

---

## 13. Agent Resolution Loop

The Insight Synthesizer and Quality Critic collaborate through a controlled revision loop.

### 13.1 Flow

```text
Insight Synthesizer
        ↓
Creates proposal
        ↓
Quality Critic
        ↓
Accepts or challenges
        ↓
Insight Synthesizer revises
        ↓
Quality Critic re-evaluates
```

### 13.2 Possible outcomes

The loop may end with:

- accepted proposal
- accepted proposal with explicit uncertainty
- revised proposal
- rejected proposal
- unresolved agent disagreement
- request for additional Evidence
- request for researcher judgement

### 13.3 Iteration limit

The system should use a safe iteration limit.

Repeated agent disagreement should not create an endless loop.

After the limit is reached, the system should create a Review Item containing:

- latest proposal
- Critic objections
- attempted revisions
- unresolved issue
- supporting and contradicting Evidence
- suggested researcher actions

### 13.4 Artificial consensus

The system must not optimize for agreement at all costs.

A valid final state is:

```text
Two interpretations remain plausible based on the available Evidence.
```

This state should be preserved as uncertainty rather than hidden.

---

## 14. Knowledge Curator

The Knowledge Curator maintains the organization and internal consistency of research knowledge.

### 14.1 Purpose

The Curator decides how an accepted or proposed change relates to existing Current Understanding.

It focuses on knowledge structure rather than primary interpretation.

### 14.2 Inputs

The Knowledge Curator receives:

- accepted Evidence
- Patterns
- synthesized Insight proposals
- Critic assessments
- existing Insight Cards
- Current Understanding
- Main Insight Clusters
- Research Questions
- Review Items
- Change Records

### 14.3 Responsibilities

The Knowledge Curator may:

- attach Evidence to an existing Insight
- update Insight relationships
- propose new Insight Cards
- detect duplicate Insights
- propose Insight merges
- propose Insight splits
- reorganize Main Insight Clusters
- update Research Question answers
- update confidence overviews
- surface contradictions
- create Open Questions
- mark Insights as challenged
- propose superseding an Insight
- propose archiving an Insight
- maintain Current Understanding structure
- generate Change Records
- determine whether a change is meaningful
- create Review Items

### 14.4 Meaningful change classification

The Curator classifies changes as:

#### Routine

Examples:

- another supporting Quote
- another supporting Evidence object
- minor wording normalization
- metadata correction
- relationship repair

#### Meaningful

Examples:

- new Insight
- changed answer to a Research Question
- confidence level change
- new Contradiction
- merge or split
- changed applicability
- new Opportunity
- previously stable Insight becoming uncertain
- Insight becoming superseded

### 14.5 Outputs

Possible outputs include:

- Current Understanding update proposal
- Change Record
- Review Item
- Main Insight Cluster update
- Research Question answer update
- no-meaningful-change result

### 14.6 Boundaries

The Knowledge Curator may not:

- approve major knowledge changes
- close a Research Round
- merge Program Insights
- remove historical versions
- resolve an unresolved contradiction without governance
- change Source content
- create product Recommendations independently

---

# Part V — Opportunity and Recommendation Agents

## 15. Opportunity Agent

The Opportunity Agent identifies areas where the product, service, workflow or research process could improve.

### 15.1 Purpose

The agent translates accepted or proposed Insights into problem and value spaces without jumping directly to solutions.

### 15.2 Inputs

The Opportunity Agent receives:

- Insight Cards
- Main Insight Clusters
- Research Questions
- Current Understanding
- user groups
- contexts
- Project Context
- relevant operational or product constraints
- existing Opportunities

### 15.3 Responsibilities

The Opportunity Agent may:

- propose Opportunities
- connect multiple Insights to one Opportunity
- identify duplicate Opportunities
- define affected user groups
- define affected contexts
- describe expected value
- identify affected outcomes
- propose Opportunity confidence
- identify research Opportunities
- identify cross-round Opportunity candidates

### 15.4 Opportunity framing

An Opportunity should:

- describe a need or improvement area
- remain solution-neutral
- link to supporting Insights
- explain affected users or workflows
- define expected value
- remain appropriately scoped

### 15.5 Outputs

Possible outputs include:

- proposed Opportunity
- Opportunity revision
- Opportunity merge proposal
- Opportunity split proposal
- duplicate warning
- no-opportunity result

### 15.6 Boundaries

The Opportunity Agent may not:

- present a solution as an Opportunity
- prioritize based only on business preference
- create Opportunities without linked Insights
- approve an Opportunity
- create final Recommendations
- convert every Insight into an Opportunity

### 15.7 Review rules

Researcher review is required for:

- new significant Opportunities
- Opportunity merges
- Opportunity prioritization
- Program-level Opportunities
- Opportunities with major business or operational implications

---

## 16. Recommendation Agent

The Recommendation Agent proposes possible responses to accepted or reviewable
research knowledge.

### 16.1 Purpose

The agent creates traceable and testable Recommendations while preserving the distinction between research knowledge and solution hypotheses.

### 16.2 Inputs

The Recommendation Agent receives:

- Opportunities when available
- supporting Insight Cards
- supporting Patterns
- supporting Evidence
- Research Context
- Project Context
- constraints
- existing Recommendations
- Assumptions
- Open Questions
- relevant product principles
- known previous decisions

### 16.3 Responsibilities

The Recommendation Agent may:

- propose one or more Recommendations
- describe what Research OS learned
- propose what should be done
- identify affected users
- identify risks
- identify trade-offs
- identify Assumptions
- identify unresolved questions
- propose validation approaches
- compare alternative Recommendations
- connect Recommendations to existing product decisions

### 16.4 Outputs

Possible outputs include:

- Recommendation proposal
- alternative Recommendations
- Recommendation risk assessment
- validation proposal
- Assumption
- Open Question
- no-recommendation result

### 16.5 Boundaries

The Recommendation Agent may not:

- present a Recommendation as proven
- mark a Recommendation as accepted
- determine implementation priority
- create a Recommendation without traceable Evidence, Pattern, Insight or Opportunity support
- claim expected effect as measured fact
- treat product implementation as validation
- invalidate an Insight when a Recommendation fails

### 16.6 Review rules

Researcher or product-team review is required before a Recommendation becomes:

- Accepted
- Planned
- Implemented
- Validated
- Invalidated

Research OS should preserve who made each decision.

---

# Part VI — Program Knowledge Agents

## 17. Program Linker

The Program Linker compares completed Round Knowledge with existing Program Knowledge.

### 17.1 Purpose

The agent helps research accumulate across Research Rounds without flattening context or silently rewriting history.

### 17.2 Inputs

The Program Linker receives:

- closed Round Knowledge
- Program Knowledge
- Program Insights
- contributing Round Insight Cards
- applicability
- confidence
- contexts
- Contradictions
- Open Questions
- prior cross-round link decisions

### 17.3 Responsibilities

The Program Linker may:

- identify related Round Insights
- identify support for existing Program Insights
- identify challenges to Program Insights
- propose a new Program Insight
- propose a Program Insight refinement
- identify temporal changes
- identify context-specific differences
- identify participant-segment differences
- propose Program Insight merges
- propose Program Insight splits
- identify recurring Opportunities
- carry forward Open Questions
- identify outdated Program Knowledge

### 17.4 Relationship types

The Program Linker may propose relationships such as:

- Supports
- Strengthens
- Weakens
- Refines
- Contradicts
- Supersedes
- Contextualizes
- Applies to Different Segment
- Applies to Different Environment
- Related but Distinct

### 17.5 Outputs

Possible outputs include:

- Program link proposal
- new Program Insight proposal
- Program Insight change proposal
- cross-round Contradiction
- recurring Opportunity
- future research question
- no-relevant-link result

### 17.6 Boundaries

The Program Linker may not:

- merge Program Insights automatically
- rewrite Round Knowledge
- remove context differences
- treat similar wording as equivalent knowledge
- increase confidence solely because multiple documents repeat the same claim
- create Program Knowledge from an active, unclosed Research Round by default

### 17.7 Review rules

Researcher review is required for:

- creation of a Program Insight
- material Program Insight revision
- Program Insight merge or split
- confidence change
- superseding or archiving Program Knowledge
- resolution of cross-round contradictions

Routine links to an existing Program Insight may be accepted automatically when they do not change meaning or confidence.

---

# Part VII — Deliverable Agents

## 18. Deliverable Editor

The Deliverable Editor transforms approved research knowledge into communication artifacts.

### 18.1 Purpose

The agent reduces the effort required to create consistent, traceable and audience-appropriate research outputs.

### 18.2 Inputs

The Deliverable Editor may receive:

- Current Understanding
- Round Knowledge
- Program Knowledge
- Insight Cards
- Main Insight Clusters
- Opportunities
- Recommendations
- Quotes
- Research Context
- audience
- communication goal
- output template
- researcher instructions

### 18.3 Supported outputs

The Deliverable Editor may create:

- Research Documentation
- Presentation Preparation
- Design Recommendations
- Product Recommendations
- Executive Summary
- Program Knowledge Summary
- stakeholder update
- research handover
- concise decision brief

### 18.4 Responsibilities

The Deliverable Editor may:

- select relevant knowledge
- structure a narrative
- adapt detail to the audience
- draft headings
- draft summaries
- select representative Quotes
- create slide-by-slide structures
- create appendices
- preserve traceability
- include limitations
- include confidence and uncertainty
- maintain consistent terminology
- identify gaps in the requested output

### 18.5 Deliverable rules

The Deliverable Editor should:

- use approved knowledge where available
- label provisional knowledge
- preserve uncertainty
- avoid creating new unsupported Insights
- avoid overstating Recommendations
- include important Limitations
- avoid selective Evidence presentation
- reference the originating knowledge version
- separate researcher edits from generated content

### 18.6 Boundaries

The Deliverable Editor may not:

- change underlying knowledge silently
- create new Evidence
- resolve contradictions for narrative convenience
- exclude material Limitations because they weaken the message
- present draft Recommendations as approved decisions
- create an independent version of research truth

### 18.7 New interpretation during editing

If the agent or researcher introduces a new interpretation while editing a Deliverable, the system should create a proposal to add that interpretation to the knowledge model.

The Deliverable should not become the only location where the new interpretation exists.

---

# Part VIII — Governance Agents

## 19. Privacy and Governance Agent

The Privacy and Governance Agent identifies risks related to access, consent, sensitive data and research governance.

### 19.1 Purpose

The agent supports safe handling of research material.

It does not replace legal, ethical or organizational accountability.

### 19.2 Inputs

The agent may inspect:

- Sources
- Source metadata
- participant data
- consent classifications
- access settings
- Source Representations
- Evidence
- Quotes
- Deliverables
- export requests
- retention policies

### 19.3 Responsibilities

The Privacy and Governance Agent may:

- detect personal information
- detect potentially sensitive information
- identify missing consent metadata
- flag inappropriate access
- propagate Source restrictions
- recommend pseudonymization
- identify unsafe Quote usage
- detect prohibited exports
- identify retention issues
- create governance Review Items
- block automated processing when required

### 19.4 Outputs

Possible outputs include:

- privacy warning
- access restriction proposal
- pseudonymization proposal
- retention warning
- blocked action
- governance Review Item
- audit log entry

### 19.5 Boundaries

The Privacy and Governance Agent may not:

- grant consent
- infer legal permission
- permanently delete material without governed approval
- override researcher or organizational policy
- expose restricted Source content in explanations
- make final legal decisions

### 19.6 Priority

Privacy and governance constraints override ordinary workflow automation.

An agent should not complete a task when doing so would violate access or consent rules.

---

## 20. Workflow Orchestrator

The Workflow Orchestrator coordinates agent tasks and state transitions.

### 20.1 Purpose

The Orchestrator ensures that agents run in the correct sequence, receive the correct inputs and do not exceed their permissions.

It manages workflow, not research interpretation.

### 20.2 Responsibilities

The Workflow Orchestrator may:

- create agent tasks
- determine task sequence
- pass domain references between agents
- monitor Processing Status
- retry recoverable failures
- stop unsafe workflows
- enforce iteration limits
- route unresolved issues to the Review Queue
- trigger downstream processing
- prevent duplicate work
- record agent execution history
- detect workflow completion
- notify researchers of meaningful changes

### 20.3 Example workflow

```text
Source uploaded
    ↓
Source Intake Agent validates Source
    ↓
Privacy Agent checks permissions
    ↓
Source Processor creates transcript
    ↓
Evidence Extractor proposes Evidence
    ↓
Method Specialist assesses Evidence
    ↓
Pattern Detector updates Patterns
    ↓
Insight Synthesizer proposes changes
    ↓
Quality Critic evaluates changes
    ↓
Knowledge Curator prepares update
    ↓
Routine updates applied
Meaningful updates sent to Review Queue
```

### 20.4 Boundaries

The Workflow Orchestrator may not:

- create research conclusions
- approve Insight Cards
- close Research Rounds
- override governance restrictions
- resolve agent disagreement
- rewrite agent outputs to create consensus
- determine research priority

---

# Part IX — Agent Collaboration

## 21. Shared Knowledge State

Agents collaborate through domain entities and proposals.

They should not rely on one continuously expanding conversation history as the source of truth.

The shared state includes:

- current domain entities
- entity versions
- proposals
- Change Records
- Review Items
- Decision Records
- relevant context
- processing history

This makes collaboration:

- inspectable
- reproducible
- replaceable
- easier to test
- less dependent on one model session

---

## 22. Proposal Model

Agents do not directly change governed knowledge.

They create proposals.

A proposal should contain:

- proposal ID
- proposed action
- target entity
- previous state
- proposed state
- rationale
- supporting entities
- contradicting entities
- agent confidence
- risk level
- review requirement
- expiration or supersession status

Possible actions include:

- Create
- Update
- Link
- Unlink
- Merge
- Split
- Strengthen
- Weaken
- Refine
- Supersede
- Archive
- Reopen
- Reject
- No Change

---

## 23. Agent Handoffs

A handoff occurs when one agent’s output becomes another agent’s input.

Every handoff should specify:

- task
- expected output
- relevant domain entities
- unresolved uncertainty
- prohibited actions
- review status of upstream material

Example:

```text
Evidence Extractor → Method Specialist

Task:
Assess the methodological strength and limitations of Evidence E-104.

Inputs:
- Evidence E-104
- Source S-021
- Research Context RC-004
- Method: Moderated usability test
- Prototype fidelity notes

Prohibited:
- Do not create or modify an Insight Card.
```

Explicit handoffs reduce role overlap.

---

## 24. Agent Disagreement

Agent disagreement is a normal part of the architecture.

Examples:

- the Synthesizer sees one broad Insight
- the Critic believes two narrower Insights are required
- the Program Linker proposes a merge
- the Curator believes the contexts are too different
- the Method Specialist recommends lower confidence
- the Synthesizer argues the cross-method Evidence remains strong

### 24.1 Resolution categories

Disagreements may be:

- resolved through revision
- resolved through additional Evidence
- accepted as uncertainty
- escalated to researcher judgement
- deferred until future research

### 24.2 Disagreement record

A meaningful unresolved disagreement should record:

- agents involved
- disputed entity
- positions
- Evidence used
- attempted revisions
- unresolved question
- recommended human action

---

# Part X — Human Review Model

## 25. Automatic Actions

Agents may perform automatic actions when they are:

- low risk
- reversible
- traceable
- high confidence
- unlikely to affect interpretation materially

Examples:

- file-type classification
- language detection
- transcript generation
- metadata extraction
- exact duplicate detection
- Quote linking
- Source-location linking
- adding supporting Evidence to an existing Insight
- minor wording normalization
- generating a Change Record
- updating Processing Status

---

## 26. Review-Required Actions

Human review is required when an action materially changes research understanding.

Examples:

- creating an Insight Card
- materially revising an Insight
- changing confidence
- resolving a Contradiction
- merging or splitting Insights
- changing applicability
- creating a significant Opportunity
- creating a Recommendation
- creating or revising a Program Insight
- accepting a new interpretation
- marking an Insight as superseded
- recommending Round closure

---

## 27. Researcher-Only Actions

The following actions remain researcher-only:

- approving final Research Context
- approving final Research Questions
- making final method choices
- resolving important ambiguity
- accepting or rejecting major Insights
- confirming Program Knowledge merges
- accepting unresolved contradictions at closure
- closing a Research Round
- approving final Recommendations
- making sensitive-data decisions
- correcting material research interpretation
- approving final Deliverables where required

AI may prepare these actions but may not execute them independently.

---

## 28. Review Queue Generation

Agents should create a Review Item only when researcher judgement adds meaningful value.

A Review Item should explain:

- what changed
- what this helps us understand
- which Evidence is relevant
- what the agents agree on
- what remains uncertain
- available decisions
- consequences of each decision

The Review Queue should not become a list of all AI activity.

`What this helps us understand` should describe the interpretation value of the
item itself. It should not be a generic explanation of why human review is required.

---

# Part XI — Agent Permissions

## 29. Permission Levels

Each agent action belongs to one permission level.

### Read

The agent may inspect an entity.

### Propose

The agent may create a proposal but not change the active entity.

### Apply Routine Change

The agent may apply a low-risk, reversible update.

### Escalate

The agent may create a Review Item.

### Restricted

The action is not permitted for the agent.

---

## 30. Conceptual Permission Matrix

| Agent | Read Sources | Create Evidence | Propose Insights | Update Current Understanding | Create Opportunities | Create Recommendations | Update Program Knowledge | Generate Deliverables | Close Round |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Research Planner | Limited | No | No | No | No | No | No | Draft only | No |
| Source Intake Agent | Yes | No | No | No | No | No | No | No | No |
| Source Processor | Yes | No | No | No | No | No | No | No | No |
| Evidence Extractor | Yes | Propose | No | No | No | No | No | No | No |
| Method Specialist | Yes | Assess | No | No | No | No | No | No | No |
| Pattern Detector | Through Evidence | No | No | No | No | No | No | No | No |
| Insight Synthesizer | Through Evidence | No | Propose | No | Candidate | No | No | No | No |
| Quality Critic | Through Evidence | No | Critique | No | Critique | Critique | Critique | No | No |
| Knowledge Curator | Through references | No | Organize | Propose or routine | Link | No | No | No | No |
| Opportunity Agent | Through Insights | No | No | No | Propose | No | Candidate | No | No |
| Recommendation Agent | Through Insights | No | No | No | Read | Propose | No | Draft | No |
| Program Linker | Through Round Knowledge | No | No | No | Program candidate | No | Propose | No | No |
| Deliverable Editor | Through approved knowledge | No | No | No | Read | Read | Read | Generate | No |
| Privacy and Governance Agent | As required | No | No | Restrict only | No | No | Restrict only | Restrict only | No |
| Workflow Orchestrator | Metadata and references | No | No | No | No | No | No | Trigger only | No |

This matrix is conceptual.

The Technical Specification should translate it into concrete authorization rules.

---

# Part XII — Agent Memory and Context

## 31. Context Scoping

Agents should receive the smallest relevant context required for their task.

Too little context may create incorrect interpretations.

Too much context may:

- increase cost
- increase distraction
- bias processing toward existing knowledge
- expose unnecessary sensitive data
- make outputs less reproducible

Context should be selected deliberately.

### 31.1 Typical context layers

An agent task may include:

- task-specific entity
- immediate linked entities
- Research Context
- relevant Research Questions
- selected Project Context
- selected Program Knowledge
- explicit Researcher Notes
- applicable governance rules

### 31.2 Existing knowledge bias

Existing Program Knowledge may help identify continuity, but it may also bias new research.

Agents should distinguish:

- prior knowledge used as context
- new Evidence from the current Research Round

The Evidence Extractor should generally operate with limited exposure to existing Insights where this reduces confirmation bias.

The Synthesizer and Program Linker require more prior knowledge to compare findings.

---

## 32. Agent Memory

Agents should not depend on hidden, unstructured long-term memory.

Persistent knowledge belongs in domain entities.

Agent memory may include:

- task state
- previous attempts
- processing checkpoints
- unresolved handoff information
- model-specific cache

Persistent research understanding must remain in:

- Evidence
- Insight Cards
- Current Understanding
- Round Knowledge
- Program Knowledge
- Change Records
- Decision Records

---

# Part XIII — Quality and Evaluation

## 33. Agent Evaluation Principles

Agents should be evaluated on more than fluent output.

Evaluation should measure whether the agent performs its bounded responsibility correctly.

### 33.1 Shared evaluation dimensions

Relevant dimensions include:

- traceability
- factual grounding
- role adherence
- uncertainty handling
- completeness
- precision
- consistency
- reproducibility
- privacy compliance
- usefulness to researchers

### 33.2 Agent-specific evaluation

#### Evidence Extractor

Evaluate:

- observation accuracy
- source-location accuracy
- atomicity
- separation of Evidence and interpretation
- recall of important Evidence
- handling of contradictions

#### Insight Synthesizer

Evaluate:

- Evidence grounding
- insight usefulness
- scope accuracy
- duplicate avoidance
- contradiction handling
- confidence calibration

#### Quality Critic

Evaluate:

- issue detection
- false-positive rate
- severity calibration
- usefulness of revisions
- independence from Synthesizer framing

#### Program Linker

Evaluate:

- correct cross-round connections
- preservation of context
- false merge rate
- contradiction detection
- historical traceability

#### Deliverable Editor

Evaluate:

- fidelity to approved knowledge
- narrative quality
- audience fit
- preservation of uncertainty
- absence of unsupported claims

---

## 34. Confidence Calibration

Agent confidence should refer to the reliability of the agent’s specific output.

It is different from research confidence.

Examples:

- Evidence extraction confidence describes confidence that the Source was interpreted correctly.
- Insight confidence describes strength of the research finding.
- Agent confidence describes confidence that the proposed action is appropriate.

These values must not be combined into one score.

---

## 35. Testing Strategy

Agent workflows should be tested using:

- synthetic Sources
- real anonymized research material
- known edge cases
- contradictory Evidence sets
- low-quality transcripts
- multi-language Sources
- misleading Researcher Notes
- duplicate Insights
- context-specific findings
- sensitive-data scenarios
- historical Program Knowledge

Tests should include both correct outputs and expected refusal or uncertainty behaviour.

---

# Part XIV — Example Agent Workflow

## 36. Example: Processing a Usability Test

### 36.1 Source Intake Agent

Input:

```text
Audio recording and observation notes from Participant 04.
```

Output:

```text
Source Type:
Audio

Source Role:
Primary Research

Method:
Moderated usability test

Language:
English

Required processing:
- transcription
- speaker separation
- timestamp alignment
- Evidence extraction
```

### 36.2 Source Processor

Output:

```text
Timestamped transcript with facilitator and participant speakers.
```

### 36.3 Evidence Extractor

Proposed Evidence:

```text
Participant 04 looked at the product image before reading the location code during 8 of 10 observed picks.
```

```text
Participant 04 returned to the location code when the product image did not match the shelf contents.
```

```text
Participant 04 stated that the product image made the task feel easier.
```

### 36.4 Method Specialist

Assessment:

```text
The first two Evidence objects describe observed behaviour.

The third is a self-reported perception and should not independently establish improved task performance.

The prototype did not include production-level error feedback, which limits interpretation of recovery behaviour.
```

### 36.5 Pattern Detector

Pattern proposal:

```text
New shoppers begin with visual product recognition but use the location code as a fallback when visual information is insufficient.
```

### 36.6 Insight Synthesizer

Insight proposal:

```text
Visual recognition reduces the knowledge required to begin a pick, while location codes remain valuable as a fallback when the product image or shelf state creates uncertainty.
```

### 36.7 Quality Critic

Critique:

```text
Accept with revision.

The phrase “reduces the knowledge required” is supported.

The proposal should not claim that visual recognition improves speed because the available Evidence only includes perceived ease and observed navigation order.
```

### 36.8 Insight Synthesizer revision

Revised Insight:

```text
Visual recognition gives new shoppers an immediate starting point, while location codes remain valuable as a fallback when visual information is insufficient.
```

### 36.9 Knowledge Curator

Proposed action:

```text
Update existing Insight IC-012 rather than create a new Insight.

Add Evidence E-104, E-105 and E-106.

Refine applicability to include fallback behaviour.

Confidence remains Moderate.
```

### 36.10 Meaningful change detection

Result:

```text
Meaningful change.

The existing Insight previously described product imagery only as primary guidance. New Evidence adds a fallback role for location codes.

Create Review Item.
```

### 36.11 Researcher review

Available actions:

```text
- Approve revision
- Edit revision
- Keep existing Insight and create separate fallback Insight
- Defer
- Request deeper comparison across participants
```

---

# Part XV — Minimal Initial Agent Set

## 37. MVP Recommendation

The full conceptual agent architecture does not need to be implemented at once.

A useful initial implementation may begin with:

1. Source Intake Agent
2. Source Processor
3. Evidence Extractor
4. Insight Synthesizer
5. Quality Critic
6. Knowledge Curator
7. Deliverable Editor
8. Workflow Orchestrator

The Method Specialist may initially be implemented as method-specific rules and prompts within the Evidence and Critic workflows.

The Opportunity Agent and Program Linker can be added once the core evidence-to-insight-to-recommendation pipeline is reliable.
For the Codex-controlled MVP, Recommendation synthesis is part of the core round
workflow after Insights.

The Privacy and Governance role should be present from the beginning, even if its first implementation is rule-based.

---

## 38. Suggested Evolution

### Phase 1 — Source to Evidence

Focus on:

- Source intake
- transcription and extraction
- atomic Evidence
- Source traceability
- researcher corrections

### Phase 2 — Evidence to Understanding

Add:

- Pattern Detection
- Insight Synthesis
- Quality Critique
- Current Understanding
- Review Queue

### Phase 3 — Research Outputs

Add:

- Opportunities
- Recommendations
- Research Documentation
- Presentation Preparation
- Research Round closure

### Phase 4 — Continuous Knowledge

Add:

- Program Linker
- Program Insights
- cross-round contradictions
- future research suggestions
- Program-level Deliverables

---

# Part XVI — Summary

Research OS uses specialized AI agents to support the complete research knowledge lifecycle.

The Research Planner helps define the research.

The Source Intake Agent prepares incoming material.

The Source Processor creates usable representations.

The Evidence Extractor identifies atomic observations.

The Method Specialist assesses methodological strength and limitations.

The Pattern Detector identifies repetition, variation and contradictions.

The Insight Synthesizer turns Evidence into interpreted knowledge.

The Quality Critic challenges that interpretation.

The Knowledge Curator maintains Current Understanding and identifies meaningful change.

The Opportunity Agent identifies problem and value spaces.

The Recommendation Agent proposes testable responses.

The Program Linker connects learning across Research Rounds.

The Deliverable Editor generates communication artifacts from approved knowledge.

The Privacy and Governance Agent protects participants and research material.

The Workflow Orchestrator coordinates the complete process.

The central collaboration model is:

```text
AI prepares
AI structures
AI proposes
AI challenges
AI explains

Researchers interpret
Researchers decide
Researchers approve
Researchers close
Researchers remain accountable
```

The purpose of the agent architecture is not to remove researchers from research.

Its purpose is to reduce mechanical work, improve consistency, preserve traceability and create more space for human judgement.
