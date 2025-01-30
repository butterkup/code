import sys
import tqdm
import itertools

sys.set_int_max_str_digits(0)

TOTAL = 60_000

with open('fibs.py.txt', 'w') as file:
    a, b = 0, 1
    for _ in tqdm.tqdm(itertools.repeat(0, 60_000), desc="fib(n)", colour="green", total=TOTAL):
        a += b
        a, b = b, a
        print(b, file=file)

