import timeit
import statistics

def benchmark(stmt, n, globals):
    try:
        times = timeit.repeat(stmt, number=1, globals=globals, repeat=n)
    except Exception as e:
        print("="*60)
        print(stmt)
        print(e)
        print("="*60)
        return
    print('Function:', stmt)
    print('  --------------')
    print(f'  Min:      {min(times)}')
    print(f'  Median:   {statistics.median(times)}')
    print(f'  Mean:     {statistics.mean(times)}')
    print(f'  Stdev:    {statistics.stdev(times) if len(times) > 1 else "N.A."}')
    print(f'  Max:      {max(times)}')
    print('  --------------')
    print(f'  samples:  {len(times)}')
    print()

def benchmark_autorange(stmt: str, globals: dict, n: None) -> float:
    timer = timeit.Timer(stmt, globals=globals)
    if n is None:
        count, total_time = timer.autorange()
    else:
        count = n
        total_time = timer.timeit(number=n)
    print('Function:', stmt)
    print('  --------------')
    print(f'  Total time: {total_time}')
    print(f'  Count:      {count}')
    print(f'  Mean:       {(avg_time := total_time / count)}')
    return avg_time

