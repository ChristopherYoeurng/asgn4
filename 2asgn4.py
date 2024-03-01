

from Crypto.Hash import SHA256
import random
from time import time
from itertools import product

def arbitrary_hash_trunc(s, trunc, flag=False):
    numBytes = trunc//8-1 if trunc % 8 == 0 else trunc//8 
    h = SHA256.new()
    h.update(s)
    bytes= bytearray(h.digest())[:numBytes+1]
    print(f"bytes before {bytes}") if flag else None
    bytes[-1] &= (0b11111111<<(8-trunc%8)) if trunc %8 != 0 else bytes[-1]
    print(f"bytes after {bytes}") if flag else None

    return ''.join(format(a, '02x') for a in bytes)

def brute_force(trunc_size, s):
    target = arbitrary_hash_trunc(s, trunc_size)
    chars = [chr(i) for i in range(256)]
    count = 0
    startTime = time()
    for length in range(0, 256):
        for p in product(chars, repeat=length):
            if count % 1000000 == 0:
                print("+", end=" ")
            if count % 20000000 == 0:
                print()
            count += 1
            guess = bytes(''.join(p), 'utf-8')
            # print("guess", guess)
            if arbitrary_hash_trunc(guess, trunc_size) == target:
                print("Collisions: ", count)
                print("Time: ", time() - startTime)
                print(f"Target: {target}")
                return guess

for i in range(2, 50, 2):
  print(f"starting it for len: {i}")
  print(brute_force(i, b'target'))
