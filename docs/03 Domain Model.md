# Domain Model

> This document defines the core domain model of Research OS.
>
> It describes the entities, relationships, states, responsibilities and invariants that form the foundation of the system.
>
> The Domain Model translates the conceptual architecture into a structured model that can guide product design, data modelling, AI workflows and technical implementation.

---

## 1. Purpose

The Architecture describes how Research OS organizes knowledge and how research understanding evolves.

The Domain Model makes that architecture concrete.

It defines:

- which entities exist
- what each entity represents
- which information belongs to each entity
- how entities relate to one another
- which entities may change
- which entities must remain immutable
- which actions require researcher approval
- how traceability is preserved
- how knowledge evolves across Research Rounds

The model is conceptual.

It is not yet a database schema, API contract or implementation specification. Technical representations may differ, but they must preserve the meaning and constraints defined here.

---

## 2. Modelling Principles

The Domain Model follows several principles.

### 2.1 Domain concepts should reflect research practice

The model should use language that researchers recognize.

Technical implementation concepts should not leak into the research experience unless they are necessary.

### 2.2 Evidence and interpretation remain separate

A Source is not Evidence.

Evidence is not an Insight.

An Insight is not an Opportunity.

An Opportunity is not a Recommendation.

Each represents a different step in the development of understanding.

### 2.3 Knowledge objects require stable identities

Knowledge should evolve by updating, linking, superseding or archiving stable objects.

The system should not regenerate anonymous summaries that cannot be compared over time.

### 2.4 Original inputs remain immutable

Original Sources and closed Round Knowledge snapshots must remain historically trustworthy.

Corrections and annotations may be added, but the original state must remain recoverable.

### 2.5 Relationships are first-class information

The value of Research OS does not only exist in individual objects.

It exists in the connections between:

- Sources and Evidence
- Evidence and Findings
- Evidence and Insights
- Insights and Research Questions
- Insights and Opportunities
- Opportunities and Recommendations
- Round Knowledge and Program Knowledge

These relationships must be explicitly represented.

### 2.6 Uncertainty belongs in the model

Confidence, contradictions, assumptions, limitations and open questions are not side notes.

They are core domain entities or properties.

### 2.7 Human and AI contributions remain distinguishable

Research OS must preserve:

- what was created by AI
- what was created by a researcher
- what was approved by a researcher
- what was automatically accepted
- what remains unresolved

### 2.8 Historical changes are preserved

Meaningful changes to knowledge should create a revision or change record.

Important research history should never be silently overwritten.

---

## 3. Domain Overview

The main domain entities are organized into six groups.

### 3.1 Research organization

- Research Program
- Project Context
- Research Round
- Research Context
- Research Question

### 3.2 Research inputs

- Source
- Source Representation
- Project Source
- Participant
- Researcher Note

### 3.3 Research evidence

- Evidence
- Finding
- Pattern
- Quote
- Method Assessment

### 3.4 Research knowledge

- Insight Card
- Main Insight Cluster
- Current Understanding
- Confidence Assessment
- Contradiction
- Open Question
- Assumption
- Limitation

### 3.5 Product and design direction

- Opportunity
- Recommendation

### 3.6 Governance and outputs

- Review Item
- Decision Record
- Round Knowledge
- Program Insight
- Program Knowledge
- Deliverable
- Change Record

The high-level relationship is:

```text
Research Program
│
├── Project Context
├── Research Rounds
│   │
│   ├── Research Context
│   ├── Research Questions
│   ├── Sources
│   ├── Evidence
│   ├── Patterns
│   ├── Insight Cards
│   ├── Current Understanding
│   ├── Review Items
│   ├── Opportunities
│   ├── Recommendations
│   ├── Round Knowledge
│   └── Deliverables
│
└── Program Knowledge
    └── Program Insights
```

---

# Part I — Shared Domain Concepts

## 4. Entity Identity

Every persistent domain entity has a stable identifier.

An identifier must:

- remain stable throughout the entity lifecycle
- never be reused for another entity
- allow relationships to survive wording changes
- support historical comparison
- remain independent of display names

Examples include:

- Program ID
- Round ID
- Source ID
- Evidence ID
- Finding ID
- Insight ID
- Opportunity ID
- Recommendation ID

Names and titles may change.

Identity does not.

---

## 4.1 Evidence, Findings and Review

Research OS distinguishes between Evidence and Findings.

**Evidence** is a small, traceable observation from a Source.

Examples:

- a participant hesitated before choosing a metric;
- a participant used a specific label differently than the prototype;
- a participant compared the concept to an existing spreadsheet workflow.

Evidence should be numerous enough to preserve the texture of the research session.

**Finding** is a reviewable statement that Research OS may use in synthesis.

Examples:

- users need clearer separation between exposure percentage and variant split;
- automated balance checks need explainability before teams will trust them.

A Finding may be based on one Evidence item or several Evidence items.

The Review Queue should normally ask researchers to decide on Findings or meaningful knowledge changes, not every tiny Evidence item. However, every review card must expose the Evidence behind it so the researcher can understand what is being approved.

This preserves two qualities at once:

- rich evidence for traceability and later re-analysis;
- simple review decisions for human usability.

---

## 5. Provenance

Provenance describes where an entity or change originated.

Every AI-generated or researcher-created object should contain provenance information.

Provenance may include:

- created by
- creator type
- creation timestamp
- source agent
- model or process version
- originating entity
- approval status
- approved by
- approval timestamp
- last meaningful change
- change reason

Creator types may include:

- researcher
- AI agent
- imported system
- automated rule

Provenance supports trust and accountability.

---

## 6. Lifecycle Status

Entities that evolve should have explicit lifecycle states.

A lifecycle status should describe the domain meaning of the entity, not a technical processing state.

Examples include:

- Draft
- Proposed
- Under Review
- Active
- Superseded
- Archived
- Rejected

Different entities may use different subsets of these states.

Status changes that materially affect research understanding must be recorded in a Change Record.

---

## 7. Processing Status

Processing Status is separate from Lifecycle Status.

It describes whether an entity has completed a technical or AI workflow.

Possible Processing Status values include:

- Not Started
- Queued
- Processing
- Completed
- Needs Review
- Failed
- Partially Processed

For example:

- a Source may be `Active` as a domain object
- while its Processing Status is `Processing`

These concepts should never be combined into one field.

---

## 8. Versioning

Not every edit requires a new version.

A new meaningful version should be created when a change affects:

- interpretation
- scope
- confidence
- applicability
- supporting evidence
- contradiction status
- lifecycle status
- approval state

Minor formatting changes do not require a meaningful version.

Each meaningful version should retain:

- previous version reference
- change type
- change summary
- change author
- timestamp
- evidence or reasoning that triggered the change

---

# Part II — Research Organization

## 9. Research Program

A Research Program is the long-lived container for research about a product, domain, service, workflow or problem space.

Examples:

- Fulfillment Operations
- Workflow Tools
- Customer Messaging
- Field Operations

### 9.1 Responsibilities

A Research Program:

- provides a stable knowledge boundary
- contains multiple Research Rounds
- contains shared Project Context
- maintains Program Knowledge
- preserves long-term terminology
- connects related research over time

### 9.2 Core properties

A Research Program contains:

- ID
- name
- description
- status
- Project Context
- owners
- stakeholders
- creation date
- archived date
- Research Rounds
- Program Knowledge

### 9.3 Program status

Possible statuses:

- Active
- Paused
- Archived

Archiving a program must not remove its research knowledge.

### 9.4 Relationships

A Research Program:

- has exactly one active Project Context
- contains zero or more Research Rounds
- has exactly one Program Knowledge space
- may reference related Research Programs

### 9.5 Invariants

- Every Research Round belongs to exactly one Research Program.
- A Research Program may exist without Research Rounds.
- Program Knowledge cannot exist independently of a Research Program.
- Archiving a Research Program must preserve all Sources, Evidence and knowledge history.

---

## 10. Project Context

Project Context contains durable background information relevant across multiple Research Rounds.

It helps researchers and AI understand the product or domain.

### 10.1 Core properties

Project Context may contain:

- purpose
- product description
- user groups
- environments
- key workflows
- terminology
- operational constraints
- business constraints
- stakeholders
- related systems
- product principles
- known historical decisions
- enduring assumptions
- enduring open questions
- source references
- version history

Project Context is updated from direct researcher edits, accepted Program
Context proposals and reviewed project-level Sources.

### 10.2 Evidentiary role

Project Context is not automatically Evidence.

A statement in Project Context may be:

- established organizational context
- imported documentation
- researcher-provided information
- a current assumption
- a previously supported conclusion

Its role must be explicit.

### 10.3 Relationships

Project Context:

- belongs to one Research Program
- may be informed by many project-level Sources
- may reference Sources
- may reference Program Insights
- may inform multiple Research Contexts
- may contain Researcher Notes
- may be versioned

### 10.4 Invariants

- Project Context must never be cited as primary user evidence unless it links to an underlying Source and Evidence object.
- Project-level Sources must not automatically create Round Evidence, Patterns or Insights.
- Historical versions must remain available.
- Changes to Project Context do not retroactively change closed Research Rounds.

## 10.5 Project-level Sources

A project-level Source is a Source whose scope is the Research Program rather
than a specific Research Round.

Examples include:

- stakeholder interviews
- meeting recordings
- slide decks
- product frameworks
- research documents
- product documentation
- historical reports
- strategy or roadmap material

Project-level Sources have the same identity, provenance, immutability and
representation requirements as round Sources.

Their purpose is to help maintain Project Context and, where appropriate,
Program Knowledge. Their default evidentiary role is contextual.

A project-level Source may produce:

- Source Metadata
- Source Representations
- Project Context Proposals
- Research Context suggestions for future rounds
- assumptions, constraints, terminology and open questions for review

A project-level Source must not directly produce:

- Round Evidence
- Round Patterns
- Round Insight Cards
- accepted Program Knowledge
- Recommendations

If a project-level Source contains prior research findings, those findings must
remain labelled as imported or historical until the researcher reviews their
origin, quality and applicability.

---

## 11. Research Round

A Research Round is a bounded research effort within a Research Program.

Examples:

- Discovery
- Concept Test 1
- Pilot
- Rollout Evaluation

### 11.1 Responsibilities

A Research Round:

- defines a coherent research objective
- groups relevant Sources
- contains the Evidence and knowledge created during the round
- maintains Current Understanding
- creates a stable Round Knowledge snapshot when closed
- produces Deliverables

### 11.2 Core properties

A Research Round contains:

- ID
- name
- description
- Research Program reference
- status
- start date
- target end date
- closure date
- owners
- Research Context
- Research Questions
- Sources
- Evidence
- Patterns
- Insight Cards
- Current Understanding
- Review Items
- Opportunities
- Recommendations
- Round Knowledge
- Deliverables

### 11.3 Round status

Possible statuses:

```text
Planned
   ↓
Active
   ↓
Ready for Closure
   ↓
Closed
```

Additional statuses may include:

- Paused
- Cancelled

### 11.4 Status rules

#### Planned

The round may contain:

- Research Context
- Research Questions
- research plans
- Researcher Notes

It should not yet contain accepted research Evidence unless imported intentionally.

#### Active

Sources may be added and processed.

Current Understanding evolves continuously.

#### Ready for Closure

AI or a researcher believes the round may be closed.

This state does not freeze the round.

#### Closed

The researcher has explicitly closed the round.

Round Knowledge becomes immutable.

#### Cancelled

The round ended without normal closure.

Its collected Sources and Evidence remain available and must not be deleted automatically.

### 11.5 Invariants

- Every Research Round belongs to exactly one Research Program.
- A round cannot be closed automatically by AI.
- A closed round has exactly one final Round Knowledge snapshot.
- New research Sources should normally not be added to a closed round.
- Corrections to a closed round must preserve the original snapshot.
- Deliverables generated at closure must reference the originating Round Knowledge version.

---

## 12. Research Context

Research Context defines the scope and intent of a Research Round.

### 12.1 Core properties

Research Context may contain:

- background
- problem statement
- research objective
- target users
- product or concept being studied
- intended methods
- known constraints
- stakeholder needs
- prior knowledge
- assumptions
- exclusions
- ethical considerations
- decision to be informed
- intended audience
- closure criteria

### 12.2 Relationships

Research Context:

- belongs to one Research Round
- may reference Project Context
- may reference Program Insights
- contains or references Research Questions
- may contain Researcher Notes
- may reference previous Research Rounds

### 12.3 Invariants

- Research Context is guidance, not Evidence.
- Prior knowledge included in Research Context must retain its original references.
- AI may propose changes to Research Context, but the researcher owns the final scope.

---

## 13. Research Question

A Research Question defines what the Research Round aims to understand.

### 13.1 Core properties

A Research Question contains:

- ID
- question
- rationale
- priority
- status
- parent question
- subquestions
- answer state
- current answer
- confidence
- linked Insight Cards
- linked Evidence
- open gaps
- closure relevance

### 13.2 Question status

Possible statuses:

- Draft
- Active
- Partially Answered
- Answered
- Unresolved
- Out of Scope
- Superseded

### 13.3 Relationships

A Research Question:

- belongs to one Research Round
- may have a parent Research Question
- may contain subquestions
- may link to many Evidence objects
- may link to many Insight Cards
- may create Open Questions
- contributes to round closure assessment

### 13.4 Invariants

- A Research Question may be supported by multiple Insights.
- An Insight may contribute to multiple Research Questions.
- An answer must not exist without links to supporting Insight Cards or an explicit statement that no evidence was found.
- Marking a question as Answered does not imply certainty.
- An answered question may retain contradictions and limitations.

---

# Part III — Research Inputs

## 14. Source

A Source is an original input added to a Research Round.

Examples:

- interview recording
- transcript
- observation notes
- photograph
- screenshot
- research document
- survey export
- workshop output

### 14.1 Core properties

A Source contains:

- ID
- title
- source type
- source role
- Research Round reference
- original file or content reference
- date created
- date collected
- contributor
- participants
- researcher
- language
- location
- method
- access classification
- consent classification
- processing status
- metadata
- Source Representations
- annotations

### 14.2 Source type

Possible Source Types include:

- Audio
- Video
- Transcript
- Document
- Presentation
- Image
- Screenshot
- Observation Notes
- Survey Data
- Workshop Output
- Structured Dataset
- Researcher Notes

### 14.3 Source role

Possible Source Roles include:

- Primary Research
- Supporting Context
- Researcher Guidance
- Imported Historical Research
- Product or Operational Documentation

### 14.4 Immutability

The original Source must remain immutable.

Research OS may add:

- metadata
- annotations
- corrected representations
- classifications
- access restrictions

It must not silently replace the original content.

### 14.5 Relationships

A Source:

- belongs to one Research Round
- may involve zero or more Participants
- may have multiple Source Representations
- may generate many Evidence objects
- may contain many Quotes
- may have Researcher Notes
- may be referenced by Project Context

### 14.6 Invariants

- Every Evidence object must ultimately trace to at least one Source.
- Deleting or restricting a Source must not leave unsupported Evidence presented as valid.
- A Source classified as Researcher Guidance must not be treated as primary Evidence.
- Source access restrictions must propagate to derived content.

---

## 15. Source Representation

A Source Representation is a derived, processable form of a Source.

Examples:

- audio transcript
- translated transcript
- speaker-separated transcript
- image description
- extracted document text
- timestamped event sequence
- structured survey rows

### 15.1 Core properties

A Source Representation contains:

- ID
- Source reference
- representation type
- content
- language
- creation method
- creator or agent
- created date
- processing version
- confidence
- correction status
- superseded representation
- location mapping to original Source

### 15.2 Relationships

A Source Representation:

- belongs to exactly one Source
- may supersede another representation
- may generate Evidence
- may contain Quotes
- retains location mapping to the original Source

### 15.3 Invariants

- A Source Representation is not the original Source.
- Correcting a representation must not alter the original Source.
- Evidence must retain sufficient location data to return to the original Source where possible.
- A translated representation must remain linked to the original-language representation.

---

## 16. Participant

A Participant represents a person or participant unit involved in primary research.

The model must avoid collecting unnecessary personal data.

### 16.1 Core properties

A Participant may contain:

- ID
- research-safe label
- participant group
- relevant characteristics
- Research Rounds
- Sources
- consent status
- data retention status
- access restrictions

Examples of research-safe labels:

- Participant 01
- Experienced Shopper 03
- Captain 02

### 16.2 Relationships

A Participant:

- may participate in multiple Sources
- may participate in multiple Research Rounds
- may be referenced by Evidence
- may contribute Quotes
- may belong to one or more participant segments

### 16.3 Invariants

- Research-facing labels should not expose unnecessary personal information.
- Participant data access must respect consent and retention rules.
- Removing personally identifying information should not remove the analytical value of linked Evidence where lawful and appropriate.
- AI should not infer sensitive participant characteristics unless explicitly relevant, supported and permitted.

---

## 17. Researcher Note

A Researcher Note contains human guidance, reflection, interpretation or context.

Examples:

- a hypothesis
- a field observation not captured in the recording
- a prototype limitation
- an analytical direction
- an instruction to compare findings
- a concern about evidence quality

### 17.1 Core properties

A Researcher Note contains:

- ID
- content
- author
- timestamp
- note type
- scope
- linked entities
- status

### 17.2 Note types

Possible note types include:

- Guidance
- Reflection
- Hypothesis
- Method Limitation
- Context
- Correction
- Follow-up
- Interpretation

### 17.3 Scope

A Researcher Note may apply to:

- a Research Program
- a Research Round
- a Source
- a Source Representation
- an Evidence object
- an Insight Card
- a Review Item
- a Deliverable

### 17.4 Invariants

- A Researcher Note is not Evidence by default.
- A Researcher Note must be visually distinguishable from Source-derived Evidence.
- AI may use Researcher Notes to guide analysis.
- If a Researcher Note describes a direct observation, it may only become Evidence through an explicit conversion that records its researcher-observed origin.

---

# Part IV — Evidence Model

## 18. Evidence

Evidence is an atomic, traceable observation derived from a Source.

### 18.1 Core properties

An Evidence object contains:

- ID
- evidence statement
- evidence type
- Source reference
- Source Representation reference
- source location
- Participant reference
- Research Question links
- context
- Method Assessment
- extraction confidence
- evidence quality
- creator
- review status
- correction history
- linked Patterns
- supporting Insight links
- contradicting Insight links

### 18.2 Evidence types

Possible Evidence Types include:

- Observed Behaviour
- Participant Statement
- Task Outcome
- Error
- Workaround
- Preference
- Emotional Response
- Environmental Condition
- Quantitative Result
- Interaction Sequence
- Researcher-Observed Event
- Absence or Non-use

### 18.3 Evidence statement

An Evidence statement should:

- describe one observation
- avoid unsupported interpretation
- remain understandable outside the original transcript
- preserve necessary context
- use neutral wording
- identify uncertainty where appropriate

Good example:

> Participant 03 looked at the product image before reading the location code during 8 of 10 picks.

Weak example:

> Participant 03 prefers visual picking because it is cognitively easier.

The first describes behaviour.

The second introduces interpretation that belongs in an Insight.

### 18.4 Evidence review status

Possible statuses:

- Proposed
- Automatically Accepted
- Researcher Confirmed
- Corrected
- Rejected
- Restricted

### 18.5 Relationships

Evidence:

- belongs to one primary Source
- may use one Source Representation
- may reference one Participant
- may answer multiple Research Questions
- may belong to multiple Patterns
- may support multiple Insight Cards
- may contradict multiple Insight Cards
- may contain or link to Quotes

### 18.6 Invariants

- Every Evidence object must have a Source reference.
- Every Evidence object must have a source location where the Source supports precise location references.
- Evidence must not contain an unsupported causal conclusion.
- Rejected Evidence must not contribute to active confidence calculations.
- Corrected Evidence must preserve its previous version.
- The same Evidence may support more than one Insight.

---

## 19. Quote

A Quote is a verbatim or lightly cleaned extract from a Source.

Quotes help communicate participant language but are not independent proof.

### 19.1 Core properties

A Quote contains:

- ID
- text
- original text
- translated text
- Source reference
- source location
- Participant reference
- language
- cleaning status
- context
- linked Evidence
- linked Insight Cards

### 19.2 Cleaning status

Possible values:

- Verbatim
- Lightly Cleaned
- Translated
- Paraphrased

Paraphrased content should not be presented using quotation marks.

### 19.3 Invariants

- Every Quote must trace to a Source location.
- Translation must not replace the original text.
- A Quote should not be used as a substitute for broader Evidence.
- Quote selection should not hide contradictory Evidence.
- A paraphrase is not a Quote.

---

## 20. Method Assessment

A Method Assessment describes how the research method affects the interpretation of Evidence.

### 20.1 Core properties

A Method Assessment may contain:

- method
- evidence directness
- ecological validity
- prototype fidelity
- facilitator influence
- self-report risk
- sample limitations
- context limitations
- methodological cautions
- assessment confidence

### 20.2 Relationships

A Method Assessment may apply to:

- one Evidence object
- a group of Evidence
- one Source
- an entire Research Round

### 20.3 Invariants

- Method limitations should affect confidence and interpretation, not automatically remove Evidence.
- Method Assessment must remain distinguishable from Evidence.
- The absence of a Method Assessment must not imply that the method has no limitations.

---

## 21. Pattern

A Pattern is a descriptive grouping of related Evidence.

### 21.1 Core properties

A Pattern contains:

- ID
- title
- description
- Research Round reference
- Evidence links
- participant coverage
- contexts
- exceptions
- status
- creation method
- linked Insight Cards

### 21.2 Pattern status

Possible statuses:

- Proposed
- Active
- Merged
- Split
- Challenged
- Retired

### 21.3 Relationships

A Pattern:

- belongs to one Research Round
- contains two or more related Evidence objects in normal use
- may contribute to multiple Insight Cards
- may overlap with other Patterns
- may include exceptions

### 21.4 Invariants

- A Pattern should remain descriptive.
- A Pattern does not need to explain why the behaviour occurs.
- Pattern membership must remain inspectable.
- An outlier may remain visible without being forced into a Pattern.
- A Pattern with one Evidence object should normally remain provisional.

---

# Part V — Knowledge Model

## 22. Insight Card

An Insight Card is the primary interpreted knowledge object within a Research Round.

### 22.1 Core properties

An Insight Card contains:

- ID
- title
- insight statement
- why this matters
- Research Round reference
- Research Question links
- supporting Evidence
- contradicting Evidence
- related Patterns
- Quotes
- Confidence Assessment
- applicability
- user groups
- contexts
- Open Questions
- Assumptions
- Limitations
- Opportunities
- lifecycle status
- approval state
- version history
- provenance

### 22.2 Insight statement

An Insight statement should:

- express a meaningful interpretation
- remain grounded in Evidence
- avoid unnecessary solution language
- define its scope
- avoid claiming certainty beyond the research
- be understandable outside the immediate research team

### 22.3 Why this matters

The `Why this matters` field describes the consequence of the insight.

It may address:

- user experience
- user behaviour
- product effectiveness
- operational impact
- business risk
- design decisions
- future research

It should not automatically become a Recommendation.

### 22.4 Applicability

Applicability describes where the Insight is expected to hold.

It may include:

- user groups
- experience levels
- environments
- workflows
- product versions
- research conditions
- known exclusions

### 22.5 Insight lifecycle

```text
Proposed
   ↓
Under Review
   ↓
Active
   ↓
Strengthened / Weakened / Refined
   ↓
Superseded or Archived
```

Possible statuses:

- Proposed
- Under Review
- Active
- Challenged
- Superseded
- Archived
- Rejected

`Strengthened`, `Weakened` and `Refined` are change types rather than permanent statuses.

### 22.6 Approval state

Approval state may include:

- Not Reviewed
- Automatically Accepted
- Researcher Confirmed
- Researcher Revised
- Researcher Rejected

### 22.7 Relationships

An Insight Card:

- belongs to one Research Round
- answers one or more Research Questions
- links to supporting Evidence
- links to contradicting Evidence
- may link to Patterns
- may contain representative Quotes
- has one current Confidence Assessment
- may have multiple historical Confidence Assessments
- may belong to multiple Main Insight Clusters
- may create multiple Opportunities
- may link to Program Insights
- maintains multiple versions

### 22.8 Invariants

- An Active Insight must have at least one supporting Evidence object.
- An Insight without sufficient Evidence must remain Proposed or be explicitly marked as a hypothesis.
- Supporting and contradicting Evidence must remain distinguishable.
- An Insight may not cite a Researcher Note as Evidence without explicit conversion.
- An Insight change must preserve history.
- A superseded Insight must remain accessible.
- Deleting an Insight must not delete its underlying Evidence.

---

## 23. Main Insight Cluster

A Main Insight Cluster groups related Insight Cards into a higher-level narrative.

It is a presentation and synthesis structure, not an independent source of truth.

### 23.1 Core properties

A Main Insight Cluster contains:

- ID
- title
- summary
- Research Round reference
- Insight Card links
- ordering
- rationale
- status
- provenance

### 23.2 Relationships

A Main Insight Cluster:

- belongs to one Research Round
- contains one or more Insight Cards
- may relate to multiple Research Questions
- may be used in Current Understanding
- may be used in Deliverables

### 23.3 Invariants

- Main Insight Clusters do not own Evidence directly.
- Evidence traceability flows through Insight Cards.
- The same Insight Card may appear in more than one cluster when justified.
- Changing a cluster does not change the underlying Insight Cards.
- AI may propose clusters; researchers may confirm or reorganize them.

---

## 24. Current Understanding

Current Understanding is the current structured knowledge state of an active Research Round.

It is a projection over approved and proposed domain objects.

### 24.1 Core properties

Current Understanding contains or references:

- Research Round
- Research Questions
- current answers
- Main Insight Clusters
- Insight Cards
- Opportunities
- Contradictions
- Open Questions
- Assumptions
- Limitations
- confidence overview
- unresolved Review Items
- recent meaningful changes
- current version
- last updated date

### 24.2 Nature of the entity

Current Understanding should not duplicate every underlying object.

It is a curated structure that references the current versions of those objects.

### 24.3 Relationships

Current Understanding:

- belongs to one active Research Round
- references current Research Questions
- references active and proposed Insight Cards
- references active Opportunities
- references unresolved knowledge objects
- generates Review Items
- becomes the basis for Round Knowledge at closure
- may generate provisional Deliverables

### 24.4 Invariants

- An active Research Round has one Current Understanding.
- Current Understanding may change while the round is active.
- Current Understanding must expose unresolved contradictions and uncertainty.
- Current Understanding must not include rejected Evidence as supporting material.
- Closing a round freezes a version of Current Understanding into Round Knowledge.
- Current Understanding is not itself primary Evidence.

---

## 25. Confidence Assessment

A Confidence Assessment explains the current strength of a knowledge claim.

### 25.1 Core properties

A Confidence Assessment contains:

- ID
- confidence level
- explanation
- supporting Evidence assessment
- contradicting Evidence assessment
- participant coverage
- method coverage
- applicability
- limitations
- evaluator
- timestamp
- previous assessment

### 25.2 Confidence levels

Recommended qualitative levels:

- Low
- Emerging
- Moderate
- Strong

These levels should not be treated as mathematically exact.

### 25.3 Confidence factors

Confidence may consider:

- number of supporting observations
- independence of observations
- source quality
- method fit
- consistency across participants
- participant diversity
- consistency across methods
- contradictory Evidence
- environmental validity
- prototype fidelity
- researcher confirmation

### 25.4 Relationships

A Confidence Assessment may belong to:

- an Insight Card
- a Research Question answer
- an Opportunity
- a Recommendation
- a Program Insight

### 25.5 Invariants

- Every confidence level must have an explanation.
- Confidence must not be based only on Evidence count.
- Contradictory Evidence must be considered.
- A confidence change that materially affects understanding creates a Review Item.
- Historical assessments must remain available.

---

## 26. Contradiction

A Contradiction represents tension between Evidence, Insights or contexts.

### 26.1 Core properties

A Contradiction contains:

- ID
- description
- contradiction type
- linked entities
- contexts
- possible explanations
- status
- impact
- owner
- resolution
- history

### 26.2 Contradiction types

Possible types include:

- Evidence versus Evidence
- Evidence versus Insight
- Insight versus Insight
- Round versus Round
- Self-report versus Observed Behaviour
- Contextual Difference
- Segment Difference
- Method Difference
- Temporal Change

### 26.3 Status

Possible statuses:

- Detected
- Under Review
- Explained
- Accepted as Contextual
- Converted to Open Question
- Resolved
- Archived

### 26.4 Invariants

- A Contradiction should not be silently resolved by removing one side.
- Both sides must remain traceable.
- A resolution must explain why the tension no longer affects the current understanding.
- An unresolved Contradiction must remain visible when it materially affects an Insight.

---

## 27. Open Question

An Open Question captures a meaningful gap in understanding.

### 27.1 Core properties

An Open Question contains:

- ID
- question
- origin
- priority
- linked Research Questions
- linked Insight Cards
- linked Contradictions
- linked Assumptions
- status
- suggested method
- suggested future round
- answer reference

### 27.2 Origin

An Open Question may originate from:

- incomplete Evidence
- contradictory Evidence
- an Insight limitation
- researcher input
- AI critique
- a Recommendation risk
- missing participant coverage
- Program Knowledge

### 27.3 Status

Possible statuses:

- Open
- Prioritized
- Planned
- In Research
- Answered
- No Longer Relevant
- Archived

### 27.4 Invariants

- An Open Question should retain the context that created it.
- Answering an Open Question should link to the Evidence or Insight that answers it.
- Closing a Research Round does not require every Open Question to be answered.
- Unanswered Open Questions may contribute to Program Knowledge or future planning.

---

## 28. Assumption

An Assumption is a belief being used without sufficient direct Evidence.

### 28.1 Core properties

An Assumption contains:

- ID
- statement
- origin
- scope
- importance
- risk if false
- linked Research Questions
- linked Insights
- linked Recommendations
- status
- validation plan
- outcome

### 28.2 Status

Possible statuses:

- Unvalidated
- Partially Supported
- Supported
- Challenged
- Rejected
- No Longer Relevant

### 28.3 Invariants

- Assumptions must be explicitly labeled.
- An Assumption must not be displayed as an Insight.
- An Assumption may later become supported by Evidence, but its original status must remain in history.
- High-risk Assumptions should be visible in Current Understanding and Recommendations.

---

## 29. Limitation

A Limitation describes a constraint on the validity, interpretation or applicability of research knowledge.

### 29.1 Core properties

A Limitation contains:

- ID
- description
- limitation type
- scope
- severity
- linked Sources
- linked Evidence
- linked Insights
- linked Research Round
- mitigation
- impact on confidence

### 29.2 Limitation types

Possible types include:

- Sample
- Method
- Prototype
- Environment
- Facilitation
- Data Quality
- Source Completeness
- Time
- Scope
- Participant Coverage
- Translation

### 29.3 Invariants

- Limitations must remain visible in final Round Knowledge.
- Important Limitations must affect confidence or applicability.
- Limitations should not be hidden because they weaken the narrative.
- A Limitation is not the same as a Contradiction.

---

# Part VI — Opportunities and Recommendations

## 30. Opportunity

An Opportunity describes an area where a product, service, workflow or research approach could improve.

### 30.1 Core properties

An Opportunity contains:

- ID
- title
- description
- opportunity type
- Research Round reference
- Insight Card links
- user groups
- contexts
- expected value
- affected outcomes
- Confidence Assessment
- priority
- status
- Recommendations
- history

### 30.2 Opportunity types

Possible types include:

- User Experience
- Workflow
- Product
- Operational
- Communication
- Training
- Research
- Strategic

### 30.3 Status

Possible statuses:

- Proposed
- Under Review
- Active
- Prioritized
- Addressed
- Superseded
- Rejected
- Archived

### 30.4 Relationships

An Opportunity:

- derives from one or more Insight Cards
- may relate to multiple Research Questions
- may create multiple Recommendations
- may link to a Program Insight
- may remain relevant across Research Rounds

### 30.5 Invariants

- An Active Opportunity must link to at least one Insight Card.
- An Opportunity describes a problem or value space, not a specific solution.
- An Opportunity must not present an untested Recommendation as fact.
- Opportunity confidence depends on supporting Insights, not only stakeholder preference.

---

## 31. Recommendation

A Recommendation proposes a possible response to an Opportunity.

In active rounds, a Recommendation may also be proposed directly from a strong,
traceable Evidence item, Pattern or Insight when the action is clear enough to
review. Opportunities remain useful for grouping problem spaces, but they are
not required before a lightweight Recommendation can be drafted.

### 31.1 Core properties

A Recommendation contains:

- ID
- title
- type or labels
- what we learned
- what we should do
- Opportunity reference when available
- Evidence, Pattern or Insight links
- options
- affected users
- assumptions
- risks
- trade-offs
- unresolved questions
- Confidence Assessment
- suggested validation
- status
- owner
- decision link
- history

### 31.2 Recommendation status

Possible statuses:

- Draft
- Proposed
- Under Review
- Accepted
- Rejected
- Planned
- Implemented
- Validated
- Invalidated
- Superseded
- Archived

### 31.3 Relationships

A Recommendation:

- responds to a primary Opportunity when one exists
- may link directly to Evidence, Patterns or Insight Cards
- may link to Assumptions
- may create Open Questions
- may be included in multiple Deliverables
- may link to a product Decision Record

### 31.4 Invariants

- A Recommendation must remain traceable to an Opportunity, Insight, Pattern or Evidence item.
- A Recommendation should state what was learned and what should be done.
- A Recommendation is a hypothesis until validated.
- An accepted Recommendation does not become research truth.
- Implementation status must remain separate from research confidence.
- Invalidating a Recommendation does not invalidate the underlying Insight automatically.

---

# Part VII — Review and Governance

## 32. Review Item

A Review Item represents a proposed change or unresolved issue requiring researcher judgement.

### 32.1 Core properties

A Review Item contains:

- ID
- review type
- Research Round reference
- affected entity
- proposed change
- previous state
- what this helps us understand
- supporting Evidence
- contradicting Evidence
- agent assessment
- confidence
- priority
- status
- assigned researcher
- available actions
- resolution
- Decision Record

### 32.2 Review types

Possible Review Types include:

- New Insight
- Insight Revision
- Insight Merge
- Insight Split
- Confidence Change
- Contradiction
- Opportunity
- Recommendation
- Program Knowledge Link
- Round Closure
- Source or Evidence Correction
- Privacy or Access Issue

### 32.3 Status

Possible statuses:

- Open
- In Review
- Deferred
- Resolved
- Rejected
- Escalated

### 32.4 Relationships

A Review Item:

- belongs to one Research Round or Program Knowledge space
- affects one primary entity
- may reference multiple supporting entities
- may produce one Decision Record
- may create a Researcher Note
- may create another Review Item

### 32.5 Invariants

- Routine automatic updates should not create unnecessary Review Items.
- Every Review Item must explain why human judgement is required.
- Resolving a Review Item must record the selected action.
- Rejected proposals must remain available in history.
- A closed round must not contain unresolved critical Review Items unless explicitly accepted as unresolved.

---

## 33. Decision Record

A Decision Record captures an explicit human or governed system decision.

### 33.1 Core properties

A Decision Record contains:

- ID
- decision
- decision type
- decision maker
- timestamp
- affected entity
- options considered
- rationale
- supporting Evidence
- unresolved concerns
- resulting changes
- reversibility
- previous decision reference

### 33.2 Decision types

Possible types include:

- Approve
- Revise
- Reject
- Merge
- Split
- Resolve Contradiction
- Accept Uncertainty
- Close Research Round
- Add to Program Knowledge
- Accept Recommendation
- Restrict or Remove Data

### 33.3 Invariants

- Researcher-only actions must create a Decision Record.
- Decision Records must not be silently edited.
- Reversing a decision creates a new Decision Record.
- A decision rationale may reference Evidence but is not itself Evidence.

---

## 34. Change Record

A Change Record describes a meaningful change to a domain entity.

### 34.1 Core properties

A Change Record contains:

- ID
- entity reference
- previous version
- new version
- change type
- change summary
- change trigger
- author or agent
- timestamp
- Evidence references
- Review Item reference
- Decision Record reference
- meaningful change classification

### 34.2 Change types

Possible types include:

- Create
- Strengthen
- Weaken
- Refine
- Merge
- Split
- Contradict
- Supersede
- Archive
- Reopen
- Correct
- Approve
- Reject

### 34.3 Invariants

- Every meaningful knowledge change creates a Change Record.
- Change Records are immutable.
- Minor formatting changes may be omitted.
- A Change Record must explain what changed without requiring comparison of raw data.
- Change history must remain navigable from the affected entity.

---

# Part VIII — Round and Program Knowledge

## 35. Round Knowledge

Round Knowledge is the immutable final knowledge snapshot of a closed Research Round.

### 35.1 Core properties

Round Knowledge contains:

- ID
- Research Round reference
- closure timestamp
- closed by
- final Research Context
- final Research Questions
- final question answers
- final Insight Cards
- final Main Insight Clusters
- Opportunities
- Recommendations
- Confidence Assessments
- Contradictions
- Open Questions
- Assumptions
- Limitations
- unresolved items accepted at closure
- source and Evidence references
- generated Deliverables
- version identifier

### 35.2 Creation

Round Knowledge is created when a researcher closes a Research Round.

The system freezes the approved Current Understanding version and related entities.

### 35.3 Relationships

Round Knowledge:

- belongs to exactly one Research Round
- contributes to Program Knowledge
- generates Deliverables
- may link to Program Insights
- may be referenced by future Research Contexts

### 35.4 Invariants

- A closed Research Round has exactly one canonical Round Knowledge snapshot.
- Round Knowledge must remain immutable.
- Corrections create an annotation or corrected edition without deleting the original snapshot.
- Round Knowledge must preserve unresolved uncertainty.
- Round Knowledge must retain traceability to Sources and Evidence.

---

## 36. Program Insight

A Program Insight represents curated knowledge that spans one or more Research Rounds.

### 36.1 Core properties

A Program Insight contains:

- ID
- title
- insight statement
- why this matters
- Research Program reference
- linked Round Insights
- linked Round Knowledge
- supporting Evidence references
- contradicting Evidence references
- applicability
- contexts
- Confidence Assessment
- Contradictions
- Open Questions
- status
- version history
- approval state

### 36.2 Program Insight status

Possible statuses:

- Proposed
- Active
- Challenged
- Context-Specific
- Superseded
- Archived
- Rejected

### 36.3 Relationships

A Program Insight:

- belongs to one Research Program
- links to one or more Round Insight Cards
- may reference multiple Research Rounds
- may create Program-level Opportunities
- may inform future Research Contexts
- may be contradicted by later Round Knowledge

### 36.4 Invariants

- AI may propose a Program Insight, but significant cross-round merges require researcher confirmation.
- A Program Insight must preserve links to the Round Insights from which it originated.
- Round Insights must not be deleted after merging.
- Context-specific differences should be retained rather than flattened into one broad statement.
- A Program Insight may be reopened when new Round Knowledge challenges it.

---

## 37. Program Knowledge

Program Knowledge is the curated collection of cross-round knowledge within a Research Program.

### 37.1 Core properties

Program Knowledge contains:

- Research Program reference
- Program Insights
- enduring Open Questions
- cross-round Contradictions
- long-term Assumptions
- recurring Opportunities
- historical development
- relevant Round Knowledge links
- recent meaningful changes
- curation status

### 37.2 Nature of the entity

Program Knowledge is not one large summary document.

It is a structured knowledge space composed of stable linked entities.

### 37.3 Relationships

Program Knowledge:

- belongs to one Research Program
- contains Program Insights
- references Round Knowledge
- informs new Research Contexts
- may generate program-level Deliverables
- may create future research priorities

### 37.4 Invariants

- Program Knowledge must not silently rewrite historical Round Knowledge.
- New Round Knowledge does not automatically merge into Program Knowledge.
- Important cross-round changes require review.
- Program Knowledge should remain curated rather than accumulate every minor finding.
- Every Program Insight must remain traceable to Round Knowledge.

---

# Part IX — Deliverables

## 38. Deliverable

A Deliverable is a generated or researcher-refined communication artifact based on research knowledge.

### 38.1 Deliverable types

Primary types include:

- Research Documentation
- Presentation Preparation
- Design Recommendations
- Product Recommendations
- Executive Summary
- Program Knowledge Summary
- Stakeholder Slack Message

### 38.2 Core properties

A Deliverable contains:

- ID
- type
- title
- Research Round or Research Program reference
- originating knowledge version
- generation timestamp
- generated by
- template
- audience
- status
- content
- researcher edits
- approval state
- version history
- export references

### 38.3 Deliverable status

Possible statuses:

- Draft
- Generated
- Under Review
- Approved
- Published
- Superseded
- Archived

### 38.4 Relationships

A Deliverable:

- derives from Current Understanding, Round Knowledge or Program Knowledge
- may reference Insight Cards
- may reference Opportunities
- may reference Recommendations
- may include Quotes
- may link to Decision Records
- may have multiple versions

### 38.5 Invariants

- Every Deliverable must reference its originating knowledge version.
- Editing a Deliverable must not silently alter underlying knowledge.
- A new interpretation introduced during editing should be proposed back into the knowledge model.
- Historical Deliverable versions must remain reproducible or inspectable.
- Deliverables are not primary Sources unless intentionally imported into a later Research Round as supporting context.

---

# Part X — Relationship Model

## 39. Core Cardinalities

The main cardinalities are:

```text
Research Program
    1 ─── 1 Project Context
    1 ─── * Research Round
    1 ─── 1 Program Knowledge
    1 ─── * Program Insight

Research Round
    * ─── 1 Research Program
    1 ─── 1 Research Context
    1 ─── * Research Question
    1 ─── * Source
    1 ─── * Evidence
    1 ─── * Pattern
    1 ─── * Insight Card
    1 ─── 1 Current Understanding
    1 ─── * Review Item
    1 ─── * Opportunity
    1 ─── * Recommendation
    1 ─── 0..1 Round Knowledge
    1 ─── * Deliverable

Source
    * ─── 1 Research Round
    1 ─── * Source Representation
    1 ─── * Evidence
    * ─── * Participant

Evidence
    * ─── 1 Source
    * ─── 0..1 Source Representation
    * ─── * Research Question
    * ─── * Pattern
    * ─── * Insight Card

Insight Card
    * ─── 1 Research Round
    * ─── * Evidence
    * ─── * Research Question
    * ─── * Main Insight Cluster
    1 ─── * Confidence Assessment
    1 ─── * Open Question
    1 ─── * Limitation
    * ─── * Opportunity
    * ─── * Program Insight

Opportunity
    * ─── * Insight Card
    1 ─── * Recommendation

Recommendation
    * ─── 1 Opportunity
    * ─── * Insight Card
    * ─── * Assumption
    * ─── * Deliverable
```

`*` represents zero or more unless otherwise constrained by an invariant.

---

## 40. Traceability Chain

The complete traceability chain is:

```text
Deliverable
    ↓
Recommendation
    ↓
Opportunity
    ↓
Insight Card
    ↓
Pattern
    ↓
Evidence
    ↓
Source Representation
    ↓
Source
```

Not every chain must contain every intermediate entity.

For example, an Insight may link directly to Evidence without using a Pattern.

However:

- every Recommendation must link to an Opportunity, Insight, Pattern or Evidence item
- every active Opportunity must link to an Insight
- every active Insight must link to Evidence
- every Evidence object must link to a Source

---

## 41. Knowledge Evolution Chain

Knowledge evolves across Research Rounds through the following chain:

```text
Active Current Understanding
    ↓
Closed Round Knowledge
    ↓
Program Link Proposal
    ↓
Researcher Review
    ↓
Program Insight
    ↓
Future Research Context
```

This creates a controlled loop between completed research and future research planning.

---

# Part XI — Domain Invariants

## 42. Evidence Invariants

1. Evidence always traces to a Source.
2. Evidence and interpretation remain separate.
3. Researcher Notes are not Evidence by default.
4. Rejected Evidence does not support active Insights.
5. Original Sources remain recoverable.
6. Quotes retain their original wording and location.
7. Access restrictions propagate to derived entities.

---

## 43. Insight Invariants

1. Every Active Insight has supporting Evidence.
2. Contradictory Evidence remains visible.
3. Insight history is preserved.
4. Confidence is explained.
5. Insight scope and applicability are explicit.
6. Main Insights cluster Insight Cards rather than replace them.
7. Superseded Insights remain accessible.

---

## 44. Round Invariants

1. Every Research Round belongs to one Research Program.
2. Every active round has one Current Understanding.
3. AI cannot close a Research Round.
4. Closing creates one immutable Round Knowledge snapshot.
5. Closed rounds preserve unresolved uncertainty.
6. New research normally enters a new Research Round.
7. Historical Round Knowledge cannot be silently rewritten.

---

## 45. Program Knowledge Invariants

1. Program Knowledge does not replace Round Knowledge.
2. Cross-round merges require explicit review when meaningful.
3. Program Insights retain links to contributing Round Insights.
4. Context differences are preserved.
5. New evidence may challenge existing Program Insights.
6. Program Knowledge remains curated.

---

## 46. Recommendation Invariants

1. Recommendations derive from Opportunities, Insights, Patterns or Evidence.
2. Opportunities derive from Insights, Patterns or Evidence.
3. Recommendations remain hypotheses.
4. Product acceptance does not increase research confidence automatically.
5. Recommendation implementation and research validity are separate.
6. Risks and assumptions remain visible.

---

## 47. Governance Invariants

1. Meaningful changes create Change Records.
2. Researcher-only actions create Decision Records.
3. AI and researcher authorship remain distinguishable.
4. Rejected proposals remain historically available.
5. Human review focuses on meaningful changes.
6. Sensitive data restrictions apply to all derived entities.

---

# Part XII — Example

## 48. Example Research Flow

The following example shows how the domain entities work together.

### 48.1 Research Program

```text
Fulfillment Operations
```

### 48.2 Research Round

```text
Shelf Visualisation Concept Test
```

### 48.3 Research Question

```text
How do new and experienced shoppers use visual guidance compared with location codes?
```

### 48.4 Source

```text
Usability test recording — Participant 04
```

### 48.5 Source Representation

```text
Timestamped transcript and observed action sequence
```

### 48.6 Evidence

```text
Participant 04 looked at the product image before reading the shelf code during 8 of 10 observed picks.
```

### 48.7 Pattern

```text
New shoppers repeatedly begin product location using visual recognition.
```

### 48.8 Insight Card

```text
Insight:
Product recognition is often the first orientation strategy for new shoppers.

Why this matters:
Prioritizing the product image may reduce the effort required to begin a pick.

Supporting Evidence:
E-014, E-028, E-043, E-051

Contradictory Evidence:
Two experienced shoppers ignored the product image when the location code was available.

Confidence:
Moderate
```

### 48.9 Opportunity

```text
Make product recognition the primary entry point while keeping precise location information available when needed.
```

### 48.10 Recommendation

```text
Increase the visual prominence of the product image and present the full location code as secondary information.
```

### 48.11 Current Understanding

The Insight Card appears within the Main Insight Cluster:

```text
Visual guidance reduces cognitive effort for new shoppers but competes with learned code-based behaviour among experienced shoppers.
```

### 48.12 Round closure

When the researcher closes the round:

- the Insight Card becomes part of Round Knowledge
- the final confidence is preserved
- the Opportunity and Recommendation are included
- Research Documentation is generated
- Presentation Preparation is generated
- the system proposes a link to relevant Fulfillment Operations Program Knowledge

---

# Part XIII — Summary

The Research OS Domain Model is designed around a traceable transformation:

```text
Source
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

Research Programs preserve long-term context.

Research Rounds create meaningful boundaries.

Sources preserve original research material.

Evidence records atomic observations.

Patterns group recurring Evidence.

Insight Cards turn Evidence into interpreted knowledge.

Current Understanding represents the living knowledge state of an active round.

Opportunities identify areas for improvement.

Recommendations propose testable responses.

Review Items focus researcher attention on meaningful changes.

Round Knowledge preserves the final state of completed research.

Program Knowledge connects learning across Research Rounds without erasing historical context.

The central rule of the model is:

> Every important conclusion remains connected to the Evidence that supports it, the Source from which that Evidence originated, and the decisions that shaped its interpretation.

This makes research knowledge continuous, explainable, governable and reusable over time.
