import time

def run_task(task, seconds, start):
    now = time.perf_counter() - start
    print(f'Starting {task} at {now:.2f} s')
    time.sleep(seconds)

    now = time.perf_counter() - start
    print(f'{task} is completed at {now:.2f} s')

def main():
    start = time.perf_counter()
    run_task('task1', 2, start)
    run_task('task2', 1, start)
    run_task('task3', 3, start)
    print(f'Total time taken: {time.perf_counter() - start:.2f} s')

if __name__ == "__main__":
    main()