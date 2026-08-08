# D&D Character Companion

## 1. Project Overview

**Working name:** D&D Character Companion

The D&D Character Companion is a web application for creating, managing, and using Dungeons & Dragons characters during live tabletop sessions.

The application should not behave only as a digital character sheet. Its main goal is to act as an intelligent rules-aware companion that tracks the character's current state and helps the player remember:

- prepared spells;
- spell slots;
- class resources;
- active effects;
- concentration;
- temporary bonuses;
- conditions;
- action economy;
- rest recoveries;
- relevant rules and reminders during play.

The initial version will support **D&D 2024** only.

The architecture, however, should avoid tightly coupling the core system to a specific class whenever possible, allowing future expansion to additional classes, levels, editions, and possibly other tabletop RPG systems.

---

# 2. Product Philosophy

The core design principle is:

> **Character data describes what the character has.  
> The Rules Engine determines what those things do.  
> The Companion determines what the player needs to know.**

The application should avoid class-specific conditionals scattered throughout the codebase.

Avoid patterns such as:

```python
if character.class_name == "Paladin":
    restore_channel_divinity()
```

Prefer generic domain concepts such as:

- Resource
- Feature
- Effect
- Modifier
- Trigger
- RecoveryRule
- SessionEvent
- Reminder

For example, a resource should declare when it recovers, and the rest engine should evaluate that rule.

---

# 3. Primary Goal of Version 1

Version 1 must prove that the application can represent a character as a **dynamic stateful entity**, rather than a static character sheet.

The MVP should allow a player to:

1. Create a character.
2. View calculated character statistics.
3. Track HP and temporary HP.
4. Track class resources.
5. Manage known and prepared spells.
6. Track spell slots.
7. Cast spells and consume resources.
8. Track active effects and their duration.
9. Track concentration.
10. Perform short and long rests.
11. Enter a Session Mode.
12. Receive rule-based reminders.

---

# 4. Initial Scope Restrictions

To prevent scope creep, the first implementation should be intentionally limited.

## Supported initially

- D&D 2024 rules.
- One reference class: **Paladin**.
- Character levels **1 to 5**.
- Single-class characters.
- One authenticated user can own multiple characters.
- Web application.
- REST API.
- PostgreSQL persistence.

## Explicitly out of scope for V1

Do NOT implement initially:

- AI assistant;
- multiplayer;
- Dungeon Master dashboard;
- campaigns;
- encounters;
- battle maps;
- virtual tabletop;
- 3D dice;
- chat;
- WebSockets;
- multiclassing;
- levels 6–20;
- complex inventory management;
- crafting;
- homebrew rule editor;
- D&D 2014;
- Pathfinder;
- Tormenta;
- other RPG systems;
- NPC generators;
- encounter generators.

These features belong to the roadmap after V1.

---

# 5. Recommended Technology Stack

## Frontend

- React
- TypeScript
- Vite
- Material UI
- React Router
- TanStack Query recommended

## Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic

## Database

- PostgreSQL

## Authentication

JWT-based authentication is acceptable for the MVP.

Suggested flow:

- Register
- Login
- Access Token
- Refresh Token
- Logout

Password recovery may be implemented later.

## Infrastructure

- Docker
- Docker Compose
- Nginx

The full development environment should eventually be startable with:

```bash
docker compose up
```

## Testing

Backend:

- Pytest

Frontend:

- Vitest
- React Testing Library

---

# 6. Suggested Repository Structure

A monorepo structure is recommended.

```text
dnd-character-companion/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── domain/
│   │   │   ├── character/
│   │   │   ├── spell/
│   │   │   ├── feature/
│   │   │   ├── resource/
│   │   │   ├── effect/
│   │   │   └── session/
│   │   │
│   │   ├── rules/
│   │   │   ├── effects/
│   │   │   ├── modifiers/
│   │   │   ├── triggers/
│   │   │   ├── recovery/
│   │   │   └── reminders/
│   │   │
│   │   ├── services/
│   │   ├── repositories/
│   │   ├── database/
│   │   ├── schemas/
│   │   └── main.py
│   │
│   └── tests/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── features/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── types/
│   │   └── utils/
│   │
│   └── tests/
│
├── docker-compose.yml
├── README.md
└── PROJECT_SCOPE.md
```

The **Rules Engine should not depend directly on FastAPI**.

It should be possible to unit test rules without starting an HTTP server.

---

# 7. Core Domain Model

The initial domain should contain approximately the following concepts:

```text
User
 │
 └── Character
      │
      ├── CharacterClass
      ├── Attributes
      ├── Skills
      ├── Features
      ├── Resources
      │
      ├── CharacterSpells
      │      │
      │      └── Spell
      │
      ├── ActiveEffects
      │      │
      │      └── Effect
      │
      └── Sessions
             │
             └── SessionEvents
```

Exact database normalization may change during implementation.

---

# 8. User System

A user should be able to:

- register;
- log in;
- log out;
- list their characters;
- create a character;
- edit a character;
- delete a character.

A user must never be able to access another user's characters.

---

# 9. Character Builder

Character creation should use a step-based wizard.

Suggested flow:

```text
1. Basic Information
        ↓
2. Species
        ↓
3. Background
        ↓
4. Class
        ↓
5. Attributes
        ↓
6. Skills
        ↓
7. Equipment
        ↓
8. Spells
        ↓
9. Review
```

For the MVP, not every D&D option must exist immediately.

The Paladin should be used as the reference implementation.

---

# 10. Character Basic Information

A character should support at least:

- Name
- Level
- Species
- Background
- Class
- Subclass
- Alignment
- Experience Points

Some fields may initially be informational only.

---

# 11. Attributes and Derived Statistics

Support all six standard attributes:

- Strength
- Dexterity
- Constitution
- Intelligence
- Wisdom
- Charisma

The application should automatically calculate applicable derived values, including:

- ability modifiers;
- proficiency bonus;
- saving throws;
- skill modifiers;
- initiative;
- passive perception;
- spell save DC;
- spell attack modifier.

Example:

```text
Strength

Score       18
Modifier    +4
Save        +7
```

Derived values should not be duplicated unnecessarily in persistent storage when they can safely be calculated from source data.

---

# 12. Character Dashboard

After character creation, the main character page should display the current state.

Example:

```text
─────────────────────────────────────

       ARTHUR — PALADIN 5

HP
████████████████░░
42 / 51

AC       Initiative      Speed
18          +2           30 ft

─────────────────────────────────────

RESOURCES

Lay on Hands
██████████████░░░░
18 / 25

Channel Divinity
● / ●

─────────────────────────────────────

SPELL SLOTS

1st      ● ● ● ●
2nd      ● ●

─────────────────────────────────────

ACTIVE EFFECTS

Bless
8 rounds

Shield of Faith
Concentration

─────────────────────────────────────
```

The dashboard should prioritize information needed during actual gameplay.

---

# 13. HP System

Character health must support:

- maximum HP;
- current HP;
- temporary HP.

Player actions:

- Take Damage
- Heal
- Add Temporary HP

Damage should consume temporary HP before current HP.

Example:

```text
Incoming Damage
      ↓
Temporary HP
      ↓
Current HP
```

The internal design should allow future support for:

- unconscious state;
- death saving throws;
- resistances;
- vulnerabilities;
- immunities.

These do not all need to be implemented in the first milestone.

---

# 14. Generic Resource System

The resource system is a critical architectural component.

Do not create dedicated infrastructure for every class resource.

Avoid designing separate systems for:

- Lay on Hands
- Rage
- Channel Divinity
- Wild Shape
- Bardic Inspiration

Instead define a generic resource concept.

Suggested model:

```text
Resource

id
character_id
name
source
maximum
current
recovery_type
metadata
```

Possible recovery types:

```text
SHORT_REST
LONG_REST
DAWN
MANUAL
CUSTOM
```

Example:

```text
Channel Divinity

Current: 0
Maximum: 1
Recovery: Short Rest
```

This generic resource engine should later support other classes without requiring major architectural changes.

---

# 15. Spell Model

Each spell should support structured information such as:

```text
Spell

Name
Level
School
Casting Time
Range
Components
Duration
Concentration
Ritual
Description
Higher Levels
```

Do not rely only on a large unstructured description field.

Important spell properties should be represented as structured data.

---

# 16. Character Spell System

A character should be able to have:

- available spells;
- known spells where applicable;
- prepared spells;
- spell slots.

The system should understand whether a spell is currently prepared.

---

# 17. Spell Preparation

Provide a dedicated spell preparation interface.

Example:

```text
PREPARE SPELLS

Prepared
8 / 9

[x] Bless
[x] Command
[x] Cure Wounds
[x] Shield of Faith
[x] Aid
[ ] Protection from Evil
[ ] Lesser Restoration
[ ] Zone of Truth
```

The system should:

- calculate the maximum number of prepared spells according to implemented rules;
- prevent invalid preparation counts;
- show how many additional spells may be prepared.

Future feature:

- spell preparation loadouts.

Examples:

```text
Combat
Exploration
Social
Undead
Avernus
```

Loadouts are NOT required for V1.

---

# 18. Spell Slots

Represent spell slots by spell level.

Example:

```text
SPELL SLOTS

Level 1

● ● ● ○

3 / 4

Level 2

● ○

1 / 2
```

Casting a leveled spell should request or determine which spell slot is consumed.

Example interaction:

```text
Cast Bless

Use Level 1 Spell Slot?

[Cancel] [Confirm]
```

After casting, the appropriate resource must be consumed.

---

# 19. Effect Engine

The Effect Engine is one of the most important technical parts of the project.

An effect represents a temporary or ongoing modification to a character.

Suggested concepts:

```text
Effect

id
name
source
target
duration
duration_type
concentration
modifiers
triggers
expiration_rule
metadata
```

Examples of effect sources:

- spell;
- feature;
- condition;
- equipment;
- external source.

Example effect:

```text
Bless

Source:
Spell

Duration:
10 rounds

Concentration:
Yes

Modifiers:

Attack Roll
+1d4

Saving Throw
+1d4
```

The architecture should allow effects to modify gameplay calculations later.

---

# 20. Active Effects

Characters should maintain a collection of active effects.

Example:

```text
ACTIVE EFFECTS

Bless
Caster: Cleric
Remaining: 7 rounds

Haste
Caster: Wizard
Remaining: 4 rounds

Poisoned
Duration: Unknown
```

Basic actions:

- Activate effect
- Remove effect
- Advance duration
- Expire effect

---

# 21. Concentration

The system must track concentration.

Only one concentration spell can be maintained by the same character at once.

Example:

Current concentration:

```text
CONCENTRATION

Shield of Faith
```

Attempt to cast another concentration spell:

```text
You are currently concentrating on:

Shield of Faith

Casting Bless will end the current concentration effect.

[Cancel] [Continue]
```

If the player continues:

1. End the previous concentration effect.
2. Consume the appropriate spell slot.
3. Activate the new spell.
4. Set the new concentration state.

---

# 22. Rest Engine

The application should provide:

- Short Rest
- Long Rest

Rest logic should operate using resource recovery rules instead of hardcoded class checks.

Pseudo-flow:

```text
Long Rest
    ↓
Get character resources
    ↓
Find resources with LONG_REST recovery
    ↓
Restore according to rule
```

Example result:

```text
LONG REST COMPLETED

HP
31 → 51

Spell Slots
4 / 6 → 6 / 6

Lay on Hands
8 → 25

Channel Divinity
0 → 1
```

The API should return a summary of changes caused by a rest.

---

# 23. Session Mode

The Character Companion should have a dedicated gameplay-oriented mode.

Action:

```text
Start Session
```

The Session Mode should reduce visual noise and show information most relevant during play.

Example:

```text
ARTHUR

HP
42 / 51

AC 18

────────────

MY TURN

ACTION
Available

BONUS ACTION
Available

REACTION
Available

MOVEMENT
30 / 30 ft

────────────

RESOURCES

Lay on Hands
18 / 25

Channel Divinity
1 / 1

────────────

CONCENTRATION

Shield of Faith
```

---

# 24. Action Economy

During a session, track:

- Action
- Bonus Action
- Reaction
- Movement

Suggested state:

```text
Action
AVAILABLE

Bonus Action
AVAILABLE

Reaction
AVAILABLE

Movement
30 / 30 ft
```

After the character uses an action:

```text
Action
USED
```

At the beginning of the next turn:

- Action resets.
- Bonus Action resets.
- Movement resets.

Reaction recovery should follow the proper game rule and be modeled independently.

The initial implementation may allow manual marking of action usage.

Automatic detection can be expanded later.

---

# 25. Session Events

Important actions should generate Session Events.

Suggested events:

```text
damage_received
healing_received
temporary_hp_added
spell_cast
spell_slot_used
resource_used
resource_restored
turn_started
turn_ended
effect_started
effect_ended
rest_completed
concentration_started
concentration_ended
```

Example:

```json
{
  "type": "damage_received",
  "character_id": 42,
  "value": 23
}
```

Session events are important because they will later support:

- reminders;
- session history;
- statistics;
- multiplayer synchronization;
- AI context.

---

# 26. Reminder Engine

The Reminder Engine converts character state and session events into useful player notifications.

The first version should be deterministic and rule-based.

Do NOT use AI for this system initially.

Example:

```text
damage_received
        ↓
Character concentrating?
        ↓
YES
        ↓
Create concentration reminder
```

Result:

```text
Concentration Check

You received 22 damage while concentrating.

Make a Constitution saving throw.
DC 11.
```

Another example:

```text
turn_started
      ↓
Effect expires this turn?
      ↓
YES
```

Result:

```text
Bless expires at the end of this turn.
```

Possible reminder categories:

- warning;
- informational;
- available ability;
- expiring effect;
- missing preparation;
- concentration;
- resource recovery.

---

# 27. Session Checklist

Before beginning a session, the player should be able to run a character readiness check.

Example:

```text
READY FOR ADVENTURE?

✓ HP Full
✓ Resources restored
⚠ Prepared Spells: 7 / 9
✓ Equipment
⚠ Level Up available
✓ No unresolved effects
```

The initial checklist should evaluate:

- HP state;
- missing prepared spells;
- depleted resources;
- unresolved effects;
- concentration still active from previous session.

Future checks may include:

- equipment;
- attunement;
- leveling;
- consumables.

---

# 28. Paladin Reference Implementation

Paladin levels 1–5 should act as the first reference class for validating the architecture.

The goal is NOT to hardcode the entire application around Paladin.

Paladin is used because it exercises several important systems:

- martial character statistics;
- spellcasting;
- prepared spells;
- spell slots;
- class resources;
- healing resources;
- concentration;
- active effects;
- rest recovery.

The implementation should demonstrate that Paladin features can be represented using the generic systems.

---

# 29. API Design

Use RESTful endpoints.

Exact endpoint names may change, but suggested resources include:

```text
/api/auth
/api/users
/api/characters
/api/characters/{id}/attributes
/api/characters/{id}/resources
/api/characters/{id}/spells
/api/characters/{id}/effects
/api/characters/{id}/rests
/api/characters/{id}/sessions
/api/sessions/{id}/events
/api/sessions/{id}/reminders
```

FastAPI's OpenAPI documentation should remain functional.

---

# 30. Important Engineering Requirements

## Separation of concerns

Keep separate:

- API layer
- application services
- domain models
- persistence
- rules engine

Do not place significant game logic inside route handlers.

## Rules engine independence

Rules should be testable without HTTP or database access whenever practical.

## Database migrations

Use Alembic.

Do not manually modify production database schemas.

## Validation

Use Pydantic models for request and response validation.

## Security

At minimum:

- hashed passwords;
- authenticated protected routes;
- ownership checks for character resources;
- environment variables for secrets;
- no credentials committed to Git.

---

# 31. Testing Requirements

Core game rules should have unit tests.

Priority test areas:

1. Ability modifier calculation.
2. Proficiency bonus calculation.
3. HP damage behavior.
4. Temporary HP behavior.
5. Resource consumption.
6. Short rest recovery.
7. Long rest recovery.
8. Spell slot consumption.
9. Prepared spell limits.
10. Concentration replacement.
11. Effect expiration.
12. Reminder generation.

Example test concept:

```python
def test_damage_consumes_temporary_hp_first():
    ...
```

And:

```python
def test_casting_second_concentration_spell_ends_first():
    ...
```

The project should prefer testing domain behavior rather than only testing HTTP endpoints.

---

# 32. Development Milestones

## V0.1 — Character Core

Implement:

- project structure;
- PostgreSQL;
- migrations;
- authentication;
- User model;
- Character model;
- attributes;
- skills;
- class;
- basic derived calculations;
- character dashboard API.

Acceptance criteria:

- authenticated user can create and retrieve a character;
- character calculations are tested;
- a user cannot access another user's character.

---

## V0.2 — Resources

Implement:

- HP;
- temporary HP;
- generic Resource model;
- resource consumption;
- resource recovery rules;
- Short Rest;
- Long Rest.

Acceptance criteria:

- damage correctly affects temporary HP before current HP;
- generic resources can be created and consumed;
- rest restores resources according to recovery rules;
- no Paladin-specific logic exists inside the generic rest engine.

---

## V0.3 — Spellcasting

Implement:

- Spell model;
- CharacterSpell;
- available/prepared state;
- preparation limits;
- spell slots;
- spell casting;
- concentration state.

Acceptance criteria:

- player can prepare valid spells;
- invalid preparation count is rejected;
- spell slot is consumed when casting;
- second concentration spell replaces the first correctly.

---

## V0.4 — Rules and Effects Engine

Implement:

- Effect model;
- ActiveEffect;
- duration;
- modifiers structure;
- effect activation;
- effect removal;
- effect expiration;
- SessionEvent foundation;
- Reminder Engine foundation.

Acceptance criteria:

- effects can be activated and expired;
- duration advances correctly;
- relevant events generate expected reminders;
- rules engine is independently unit tested.

---

## V0.5 — Session Mode

Implement:

- Session model;
- start/end session;
- turns;
- action economy;
- active effects UI;
- resources UI;
- reminders UI;
- session checklist.

Acceptance criteria:

- player can begin a session;
- action state can be tracked;
- new turns restore the correct action states;
- reminders appear based on session events;
- current resources and effects are visible without opening the full character sheet.

---

# 33. V1.0 Definition of Done

Version 1 is complete when a user can:

1. Create an account.
2. Create a Paladin level 1–5.
3. View calculated character statistics.
4. Track HP and temporary HP.
5. Track generic class resources.
6. Prepare spells.
7. Track spell slots.
8. Cast spells.
9. Maintain concentration.
10. Activate and expire effects.
11. Take short and long rests.
12. Start a gameplay session.
13. Track action economy.
14. Receive deterministic reminders.
15. Use a session preparation checklist.

The project must also have:

- automated backend tests;
- frontend tests for important flows;
- database migrations;
- Docker development setup;
- OpenAPI documentation;
- README with installation instructions.

---

# 34. Post-V1 Roadmap

## V1.5 — Expanded Character Builds

Possible features:

- levels 1–20;
- all classes;
- subclasses;
- feats;
- equipment;
- advanced inventory;
- spell preparation loadouts;
- leveling workflow;
- multiclassing.

---

## V2 — Campaign and Dungeon Master Features

Possible concepts:

```text
Campaign
 │
 ├── Dungeon Master
 ├── Players
 ├── Characters
 ├── Encounters
 └── Shared Effects
```

Features may include:

- campaign creation;
- party management;
- encounter tracking;
- DM-applied conditions;
- shared party effects.

---

## V3 — Multiplayer

Add realtime synchronization.

Potential technologies:

- FastAPI WebSockets;
- Redis;
- event-based synchronization.

Example:

```text
                  Campaign Server
                        │
            ┌───────────┼───────────┐
            ↓           ↓           ↓
           DM        Player 1    Player 2
```

A condition applied by the DM should immediately appear in the player's Companion.

---

## V4 — AI Character Companion

Only after the deterministic character and rules systems are reliable should an AI assistant be added.

The AI should receive structured context such as:

```text
Character Sheet
+
Prepared Spells
+
Available Resources
+
Active Effects
+
Current Session State
+
Relevant D&D Rules
```

Example questions:

- "What can I do this turn?"
- "Do I have anything that can remove poison?"
- "How can I help our fighter?"
- "Which abilities have I not used yet?"
- "What should I remember before this fight?"

The AI should not become the authoritative rules engine.

The deterministic Rules Engine remains the source of truth.

---

# 35. Future Extensibility

The long-term architecture may evolve toward:

```text
RPG Companion Core
        │
        ├── D&D 2024
        ├── D&D 2014
        ├── Pathfinder
        ├── Tormenta
        └── Custom Systems
```

This is NOT a V1 requirement.

Do not introduce unnecessary abstractions solely to support hypothetical systems.

Prefer an architecture that is clean enough to be extracted later rather than building a universal RPG engine prematurely.

---

# 36. UX Principles

The product should prioritize usability at the table.

Important principles:

1. Important information should require as few clicks as possible.
2. Session Mode should be usable from a laptop or tablet.
3. Current HP, AC, resources, spell slots, concentration, and active effects should be immediately visible.
4. Warnings should be noticeable but not intrusive.
5. The application should help the player remember rules without playing the character automatically.
6. Advanced information may exist in secondary screens rather than cluttering Session Mode.

---

# 37. Coding Guidelines

Prefer:

- clean architecture boundaries;
- typed Python;
- typed TypeScript;
- small focused services;
- dependency injection where useful;
- domain-focused unit tests;
- clear naming;
- reusable generic rule components.

Avoid:

- large route handlers;
- game rules directly inside React components;
- duplicated derived data;
- hidden global state;
- excessive inheritance;
- premature microservices;
- premature generic RPG abstractions.

Start as a modular monolith.

---

# 38. First Codex Task

Do not attempt to implement the entire scope at once.

The recommended first implementation task is:

> Build milestone **V0.1 — Character Core**.

The first deliverable should include:

- backend and frontend project scaffolding;
- Docker Compose development environment;
- PostgreSQL;
- FastAPI;
- React + TypeScript;
- SQLAlchemy;
- Alembic;
- User authentication;
- Character entity;
- six attributes;
- basic derived calculations;
- character creation endpoint;
- character list endpoint;
- character detail endpoint;
- initial character creation UI;
- initial character dashboard UI;
- backend unit tests;
- README setup instructions.

Before implementing later milestones, keep the architecture compatible with the generic concepts documented in this file.

---

# 39. Instructions for Codex

When working from this specification:

1. Implement one milestone at a time.
2. Do not add major features outside the requested milestone.
3. Preserve separation between domain rules and HTTP/API code.
4. Do not hardcode Paladin-specific rules into generic engines.
5. Write tests for every important domain rule.
6. Prefer simple maintainable architecture over premature complexity.
7. Update README documentation when setup or behavior changes.
8. Add Alembic migrations for schema changes.
9. Never commit secrets or credentials.
10. Explain important architectural decisions in code comments or documentation when they are not obvious.
11. Before creating a new abstraction, verify that the current milestone actually requires it.
12. Treat the deterministic Rules Engine as the source of truth for character mechanics.
13. AI features must not be implemented before the core rule systems are reliable.

---

# 40. Success Criterion

The project is successful when the player can open the application during a real D&D session and rely on it to answer:

> **What does my character currently have, what can I use, what is active, what did I already spend, and what am I likely to forget?**

That is the central product requirement.
