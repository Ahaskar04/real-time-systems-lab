import asyncio


async def stage_a_input(queue_ab):
    items = ["hello", "world", "this", "is", "an", "async", "pipeline"]
    for item in items:
        await queue_ab.put(item)
    await queue_ab.put(None)   # sentinel


async def stage_b_uppercase(queue_ab, queue_bc):
    while True:
        item = await queue_ab.get()
        if item is None:
            await queue_bc.put(None)
            queue_ab.task_done()
            break

        await queue_bc.put(item.upper())
        queue_ab.task_done()


async def stage_c_reverse(queue_bc):
    while True:
        item = await queue_bc.get()
        if item is None:
            queue_bc.task_done()
            break

        print(item[::-1])
        queue_bc.task_done()


async def main():
    queue_ab = asyncio.Queue()
    queue_bc = asyncio.Queue()

    task_a = asyncio.create_task(stage_a_input(queue_ab))
    task_b = asyncio.create_task(stage_b_uppercase(queue_ab, queue_bc))
    task_c = asyncio.create_task(stage_c_reverse(queue_bc))

    await asyncio.gather(task_a, task_b, task_c)


asyncio.run(main())
