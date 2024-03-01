from itertools import product
from multiprocessing import Pool
from Crypto.Hash import SHA256
from itertools import product
from time import time

attempts = 1

def arbitrary_hash_trunc(s, trunc, flag=False):
    numBytes = trunc//8-1 if trunc % 8 == 0 else trunc//8 
    h = SHA256.new()
    h.update(s)
    bytes= bytearray(h.digest())[:numBytes+1]
    print(f"bytes before {bytes}") if flag else None
    bytes[-1] &= (0b11111111<<(8-trunc%8)) if trunc %8 != 0 else bytes[-1]
    print(f"bytes after {bytes}") if flag else None
    # print(len(''.join(format(a, '02x') for a in bytes)))
    # return ''.join(format(a, '02x') for a in bytes)
    return bytes

def attempt_collision(args):
    global attempts 
    attempts += 1
    target, chars, length, trunc_size = args
    for p in product(chars, repeat=length):
        guess = bytes(''.join(p), 'utf-8')
        if arbitrary_hash_trunc(guess, trunc_size) == target:
            return guess
    return None

def parallel_brute_force(trunc_size, s, max_length=10):
    global attempts
    target = arbitrary_hash_trunc(s, trunc_size)
    print(f"target is {target} of length {len(target)}")
    chars = [chr(i) for i in range(256)]
    
    with Pool(processes=6) as pool:  # Adjust the number of processes based on your machine
        for length in range(1, max_length + 1):  # Limiting the maximum length for practicality
            args = [(target, chars, length, trunc_size) for _ in range(4)]  # Prepare arguments for parallel processing
            results = pool.map(attempt_collision, args)
            for result in results:
                if result:
                    return result
def main():
    global attempts
    for i in range(2, 50, 2):
        startTime = time()
        print(f"starting it for len: {i}")
        result = parallel_brute_force(i, b'target')
        print(result)
        print("Time: ", time() - startTime)
        print("attempted", attempts)
if __name__ == "__main__":
    main()