# Work Timer - A Stateful Timer with Pause/Resume

A Python implementation of a work timer that tracks elapsed time with support for pausing and resuming. Think of it like a stopwatch that knows how long it should run for.

## Core Concepts

### The Problem This Solves

Imagine you want to work for 25 minutes (Pomodoro technique). You need:

- A timer that counts up to 25 minutes
- The ability to pause if interrupted (phone call, bathroom break)
- Resume exactly where you left off
- Know when you've reached your target time

### How It Works - The Mental Model

The timer works like a stopwatch with memory:

```
STOPPED → RUNNING → PAUSED → RUNNING → (when elapsed >= duration) → FINISHED
   ↑         ↓         ↑         ↓
   └─────────┘         └─────────┘
     (start)          (pause/resume)
```

## Implementation Deep Dive

### 1. Timer States (The Brain)

```python
class TimerState(Enum):
    STOPPED = auto()  # Timer hasn't started or was reset
    RUNNING = auto()  # Timer is actively counting time
    PAUSED = auto()   # Timer is paused, preserving elapsed time
```

**Why these states?**

- **STOPPED**: Fresh timer, elapsed_time = 0, ready to start
- **RUNNING**: Actively accumulating time, clock is ticking
- **PAUSED**: Frozen in time, maintains progress but clock stopped

### 2. The WorkTimer Class - Core Architecture

```python
class WorkTimer:
    def __init__(self, total_duration: float):
        self.total_duration = total_duration  # Target duration (never changes)
        self.state = TimerState.STOPPED       # Always start in STOPPED state
        self.elapsed_time = 0.0                # Accumulated time (survives pauses)
        self.last_start_timestamp = None      # When we last hit "start/resume"
```

**Key Design Decisions:**

1. **`total_duration`**: Immutable target - this is your goal (e.g., 1500 seconds = 25 minutes)

2. **`elapsed_time`**: The "memory bank" - stores accumulated work time

   - When RUNNING: This is outdated (need to add current session)
   - When PAUSED/STOPPED: This is accurate total

3. **`last_start_timestamp`**: The "bookmark" - marks when current counting session began
   - Only meaningful when RUNNING
   - Used to calculate: "How long have we been running since last start/resume?"

### 3. Method-by-Method Breakdown

#### `start()` - Begin Fresh

```python
def start(self) -> bool:
    if self.state != TimerState.STOPPED:
        return False  # Can only start from STOPPED

    self.elapsed_time = 0.0                    # Reset progress
    self.last_start_timestamp = time.time()    # Mark current time
    self.state = TimerState.RUNNING            # Update state
    return True
```

**Logic**: Wipes slate clean, begins counting from zero. Returns `False` if timer is already running/paused.

#### `pause()` - Freeze Time

```python
def pause(self) -> bool:
    if self.state != TimerState.RUNNING:
        return False  # Can only pause if running

    now = time.time()
    self.elapsed_time += now - self.last_start_timestamp  # Bank the time

    self.last_start_timestamp = None  # Clear bookmark
    self.state = TimerState.PAUSED
    return True
```

**The Magic**: Before pausing, it "banks" the current session's time into `elapsed_time`.

- Calculates: "How long have we been running?"
- Adds that to our accumulated time
- Clears the timestamp (we're not actively timing anymore)

#### `resume()` - Continue Where We Left Off

```python
def resume(self) -> bool:
    if self.state != TimerState.PAUSED:
        return False  # Can only resume from pause

    self.last_start_timestamp = time.time()  # New bookmark
    self.state = TimerState.RUNNING
    return True
```

**Note**: Doesn't touch `elapsed_time` - that already has our previous progress!

#### `get_elapsed_time()` - The Smart Calculator

```python
def get_elapsed_time(self) -> float:
    if self.state == TimerState.RUNNING:
        # Add "banked time" + "current session time"
        return (
            self.elapsed_time +
            (time.time() - self.last_start_timestamp)
        )

    return self.elapsed_time  # If paused/stopped, banked time is accurate
```

**Why Two Cases?**

- **RUNNING**: Need to add current session (not yet banked) to saved time
- **PAUSED/STOPPED**: All time is already banked in `elapsed_time`

#### `is_finished()` - Simple Completion Check

```python
def is_finished(self) -> bool:
    return self.get_elapsed_time() >= self.total_duration
```

## Complete Usage Example with Timeline

```python
from work_timer import WorkTimer
import time

# Create a 10-second timer
timer = WorkTimer(total_duration=10.0)

# T=0s: Start the timer
timer.start()
print(f"Started - Elapsed: {timer.get_elapsed_time():.1f}s")  # ~0.0s

# T=3s: Still running
time.sleep(3)
print(f"Running - Elapsed: {timer.get_elapsed_time():.1f}s")  # ~3.0s

# T=3s: Pause for a break
timer.pause()
print(f"Paused - Elapsed: {timer.get_elapsed_time():.1f}s")   # 3.0s (frozen)

# T=5s: Still paused (2 seconds pass, but timer doesn't count them)
time.sleep(2)
print(f"Still Paused - Elapsed: {timer.get_elapsed_time():.1f}s")  # Still 3.0s!

# T=5s: Resume working
timer.resume()
print(f"Resumed - Elapsed: {timer.get_elapsed_time():.1f}s")  # 3.0s (continuing)

# T=8s: Check progress
time.sleep(3)
print(f"Running - Elapsed: {timer.get_elapsed_time():.1f}s")  # ~6.0s

# T=12s: Check if finished
time.sleep(4)
print(f"Final - Elapsed: {timer.get_elapsed_time():.1f}s")    # ~10.0s
print(f"Finished? {timer.is_finished()}")                     # True
```

## State Transition Rules

```
STOPPED --start()--> RUNNING
RUNNING --pause()--> PAUSED
PAUSED --resume()--> RUNNING

Invalid transitions return False:
- Cannot pause from STOPPED or PAUSED
- Cannot resume from STOPPED or RUNNING
- Cannot start from RUNNING or PAUSED
```

## Why This Design?

1. **Separation of Concerns**: State management separate from time tracking
2. **Single Source of Truth**: `elapsed_time` + current session = total time
3. **Immutable Target**: `total_duration` never changes (safety)
4. **Clear State Machine**: Each state has specific allowed transitions
5. **Accurate Timing**: Uses `time.time()` for real-world time tracking

## Common Use Cases

- **Pomodoro Timer**: 25-minute work sessions with breaks
- **Exercise Timer**: Track workout duration with pause for rest
- **Time Tracking**: Bill clients for actual work time (minus interruptions)
- **Game Timer**: Pause game timer when game is paused
