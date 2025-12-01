import asyncio


# ---------------- Stage A: Fan-out ----------------
async def stage_a_fanout(queue_b, queue_c):
    items = ["hello", "world", "this", "is", "an", "async", "pipeline"]

    for item in items:
        await queue_b.put(item)
        await queue_c.put(item)

    # One sentinel per branch
    await queue_b.put(None)
    await queue_c.put(None)


# ---------------- Stage B1: Uppercase ----------------
async def stage_b1_uppercase(queue_b, queue_merge):
    while True:
        item = await queue_b.get()

        if item is None:
            await queue_merge.put(None)   # forward sentinel
            queue_b.task_done()
            break

        await queue_merge.put(item.upper())
        queue_b.task_done()


# ---------------- Stage B2: Reverse ----------------
async def stage_b2_reverse(queue_c, queue_merge):
    while True:
        item = await queue_c.get()

        if item is None:
            await queue_merge.put(None)   # forward sentinel
            queue_c.task_done()
            break

        await queue_merge.put(item[::-1])
        queue_c.task_done()


# ---------------- Stage C: Merge ----------------
async def stage_c_merge(queue_merge):
    counter = 0

    while True:
        item = await queue_merge.get()

        if item is None:
            counter += 1
            queue_merge.task_done()
            if counter == 2:   # number of branches
                break
        else:
            print("OUTPUT:", item)
            queue_merge.task_done()


# ---------------- Coordinator ----------------
async def main():
    queue_b = asyncio.Queue()
    queue_c = asyncio.Queue()
    queue_merge = asyncio.Queue()

    await asyncio.gather(
        stage_a_fanout(queue_b, queue_c),
        stage_b1_uppercase(queue_b, queue_merge),
        stage_b2_reverse(queue_c, queue_merge),
        stage_c_merge(queue_merge),
    )


asyncio.run(main())
