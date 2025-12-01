# Async Text Transformer Pipeline (A → B → C)

This project implements a **multi-stage asynchronous pipeline** using Python’s `asyncio` and queues.
It demonstrates **flow control**, **backpressure**, and **graceful stream termination** using **sentinel values**.

---

## 📌 Project Overview

The pipeline consists of **three independent stages** connected by queues:

```
Stage A (Input)
   │
   ▼
queue_ab
   │
   ▼
Stage B (Uppercase)
   │
   ▼
queue_bc
   │
   ▼
Stage C (Reverse + Output)
```

Each stage runs in its own coroutine and communicates **only via queues**.

---

## 🔄 Pipeline Stages

### Stage A — Input Producer

- Emits a stream of input strings
- Pushes data into `queue_ab`
- Sends a **sentinel (`None`)** to signal end-of-stream

### Stage B — Uppercase Transformer

- Consumes items from `queue_ab`
- Converts text to uppercase
- Pushes results into `queue_bc`
- Forwards the sentinel downstream and stops

### Stage C — Reverse & Output

- Consumes items from `queue_bc`
- Reverses the string
- Prints the final output
- Terminates cleanly on sentinel

---

## 🧠 Key Concepts Demonstrated

### ✅ Multi-Stage Queues

- Queues exist **between pipeline stages**
- Each queue decouples producer and consumer speeds

### ✅ Backpressure

- If a downstream stage slows down, queues fill
- Pressure propagates upstream
- Fast stages automatically slow down
- Memory remains bounded

### ✅ Sentinel-Based Termination

- A special value (`None`) signals end-of-stream
- Ensures all stages terminate cleanly
- Prevents hanging consumers

### ✅ Correct Async Discipline

- `queue.get()` → exactly one `queue.task_done()`
- Producers never call `task_done()`
- Pipeline lifetime owned by a central coordinator

---

## ▶️ How to Run

```bash
python pipeline.py
```

Expected output:

```
OLLEH
DLROW
SIHT
SI
NA
CNYSA
ENILPIP
```

To observe **backpressure**, add a delay in Stage C:

```python
await asyncio.sleep(1)
```

You’ll see the entire pipeline slow down naturally — by design.

---

## 🏗 Why This Pattern Matters

This architecture is foundational to:

- Streaming ETL systems
- ML preprocessing pipelines
- Async job workers
- Message brokers
- Real-time analytics engines

Understanding this pattern enables you to reason about **real-world concurrent systems**, not just async syntax.

---

## 🚀 Possible Extensions

- Fan-out / fan-in stages
- Multiple workers per stage
- Dropping vs blocking policies
- Metrics and queue size monitoring
- Fault-tolerant restarts

---

## ✍️ Author Notes

Built as a learning project to develop **systems thinking with asyncio**, focusing on:

- flow control
- causality
- correctness over convenience

---
