```markdown
# Async Fan-Out / Fan-In Pipeline (MERGE)

This project demonstrates a **parallel async pipeline** using `asyncio.Queue`,
implementing the classic **fan-out / fan-in (MERGE)** pattern.

The goal is to understand **decoupling, parallel processing, termination logic,
and sentinels** — not just to make the code work.

---

## Pipeline Architecture
```

```
          ┌─── B1: Uppercase ───┐
```

A: Fan-Out ───┤ ├──▶ Queue (merge) ───▶ C: Merge
└─── B2: Reverse ────┘

```

### Stages

| Stage | Responsibility |
|-----|----------------|
| A | Produces input and **duplicates** it to all branches |
| B1 / B2 | Independent workers that transform data |
| C | Merges outputs and coordinates termination |

---

## Fan-Out vs Fan-In (Key Idea)

### Fan-Out
- One input → **multiple downstream queues**
- Same data is **duplicated**, not split
- Upstream stages stay simple and stateless

### Fan-In (MERGE)
- Multiple producers → **one consumer**
- Results are processed **as they arrive**
- No ordering or pairing guarantees

This project uses **MERGE semantics**, not JOIN.

---

## The Sentinel Concept (Critical)

### What is a Sentinel?
A **sentinel** is a special value (`None` in this project) that signals:

> “No more data will be produced by this branch.”

Sentinels are **control messages**, not data.

---

### Sentinel Rules (Memorize These)

1. **Each producer sends exactly ONE sentinel**
2. **Sentinels flow downstream**
3. **Consumers never generate sentinels**
4. **Termination is decided only at the merge stage**

In this pipeline:
- Stage A sends **one sentinel per branch**
- Each B stage forwards **one sentinel to the merge queue**
- Stage C counts sentinels and exits **only after all branches finish**

---

## Why Counting Sentinels Matters

With fan-out, branches complete **independently**.

Stage C must answer only one question:
> “Have *all* upstream branches finished?”

This is why it counts sentinels instead of relying on timing, queue emptiness,
or ordering.

⚠️ Stopping after the *first* sentinel causes silent data loss.

---

## Backpressure & Decoupling

- `asyncio.Queue` buffers data between stages
- Slow stages do **not** block fast ones immediately
- Backpressure propagates naturally through the queues
- Each stage has a single, clear responsibility

This is how real streaming systems stay stable.

---

## Key Takeaways

- Fan-out duplicates data; fan-in coordinates termination
- Parallel workers must be **globally ignorant**
- Merge stages are responsible for correctness, not workers
- Sentinels are the safest way to signal completion in async systems
- Termination logic is harder than data processing

---

## What This Pattern Is Used For

- Log aggregation
- Stream processing
- Event pipelines
- Async task runners
- Distributed systems

Understanding this pattern means understanding **systems design**, not just Python.

---

## Next Possible Extensions

- Convert MERGE → JOIN (pair outputs per input)
- Add bounded queues to observe backpressure
- Add multiple workers per branch
- Handle worker failure propagation
```
