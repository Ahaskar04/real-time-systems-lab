````markdown
# State Machines — Foundations and Login System FSM

This project introduces **State Machines (FSMs — Finite State Machines)** from absolute scratch and applies them to a real-world system: a **login / logout flow**.

State machines are not a programming trick — they are a **way of designing correct systems**.

---

## 1. What Is a State Machine?

A **state machine** is a system that:

1. Has a **finite set of states**
2. Is always in **exactly one state at a time**
3. Changes state **only via defined transitions**
4. Rejects or ignores **invalid transitions**

In short:

> **State = what the system is right now**  
> **Transition = a legal way to move to another state**

---

## 2. Why State Machines Exist

Without state machines, systems are often implemented using multiple flags.

Example (bad design):

```python
is_logged_in = True
is_logging_in = True   # impossible but allowed by code
```
````

This allows **invalid combinations** that should never exist.

State machines fix this by enforcing:

```python
state = LOGGED_IN
```

There is **no way** to be both LOGGED_IN and LOGGING_IN.

---

## 3. Why We Use `enum` for States

States must be:

- finite
- explicit
- impossible to misspell
- impossible to invent accidentally

Using `enum` guarantees this.

Example:

```python
from enum import Enum

class LoginState(Enum):
    LOGGED_OUT = 1
    LOGGING_IN = 2
    LOGGED_IN = 3
```

Benefits of `enum`:

- Only valid states can exist
- Readable and self-documenting
- Prevents invalid assignments
- Easy to debug and log
- Forces disciplined design

Enums turn _implicit assumptions_ into _explicit rules_.

---

## 4. Events vs States

A **state** represents a condition:

```
LOGGED_IN
```

An **event** represents something that happened:

```
START_LOGIN
LOGIN_SUCCESS
LOGOUT
```

Key rule:

> **Events do not change state directly.
> State machines decide whether a transition is allowed.**

---

## 5. Invalid Transitions (Core FSM Idea)

An **invalid transition** is an event that makes no sense in the current state.

Examples:

- LOGIN_SUCCESS while LOGGED_OUT
- LOGOUT while LOGGED_OUT
- START_LOGIN while already LOGGED_IN

FSM Rule:

> **Invalid transitions must be rejected immediately.**

This prevents:

- security flaws
- race conditions
- inconsistent system behavior

---

## 6. Login System FSM (Project)

### States:

```
LOGGED_OUT → LOGGING_IN → LOGGED_IN
```

### Events:

- START_LOGIN
- LOGIN_SUCCESS
- LOGIN_FAILURE
- LOGOUT

### Key Design Decisions:

- FSM enforces all transitions internally
- Invalid transitions return `False`
- Credential checking is external business logic
- FSM only manages state correctness

---

## 7. Why Business Logic Is External

The FSM does **not** check passwords or tokens.

Why?

- FSMs model **flow**, not computation
- Business logic changes more often than state logic
- Keeping them separate prevents bugs and simplifies testing

Correct separation:

```
FSM: controls allowed transitions
Auth logic: decides success or failure
```

---

## 8. Why State Machines Are the Backbone of Serious Systems

State machines are used in:

- Authentication flows
- Network protocols (TCP)
- Operating systems
- Embedded controllers
- Distributed systems
- UI navigation
- Game engines

Most critical bugs in real systems are **state bugs**, not syntax bugs.

FSMs eliminate entire classes of errors **by design**.

---

## 9. Key Takeaways

- A system must be in exactly one state at a time
- State transitions must be explicit and controlled
- Enums make invalid states impossible
- FSMs exist to reject illegal transitions
- Correct FSMs simplify reasoning and debugging

If a system is hard to reason about, it probably needs a state machine.

```

```
