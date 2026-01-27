import time
import asyncio

async def run_task(task, seconds, start):
    now = time.perf_counter() - start
    print(f'Starting {task} at {now:.2f} s')
    await asyncio.sleep(seconds)

    now = time.perf_counter() - start
    print(f'{task} is completed at {now:.2f} s')

async def main():
    start = time.perf_counter()
    await asyncio.gather(
    run_task('task1', 2, start),
    run_task('task2', 1, start),
    run_task('task3', 3, start))
    print(f'Total time taken: {time.perf_counter() - start:.2f} s')


if __name__ == "__main__":
    asyncio.run(main())