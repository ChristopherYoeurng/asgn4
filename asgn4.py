from Crypto.Hash import SHA256 
import random
from time import time
from itertools import product



def arbitrary_hash(s):
    h = SHA256.new()
    h.update(s)
    bytes = bytearray(h.digest())
    print(' '.join(hex(a) for a in bytes))


# arbitrary_hash(b"hello")
# arbitrary_hash(b"eello")

# print("\n\n")
# arbitrary_hash(b"aslalsdkfja")
# arbitrary_hash(b"aslilsdkfja")
# print("\n\n")
# arbitrary_hash(b"zzzzzzzzzz")
# arbitrary_hash(b"zzzzyzzzzz")


def arbitrary_hash_trunc(s, trunc): 
    numBytes = trunc//8 if trunc % 8 == 0 else trunc//8 + 1
    h = SHA256.new()
    h.update(s)
    bytes= bytearray(h.digest())[:numBytes] # First 16 bits

    return ''.join(hex(a) for a in bytes)[:trunc]


# def brute_force_collision(s, trunc=2):
#     target_collision_in = s
#     target_collision_out = arbitrary_hash_trunc(target_collision_in, trunc)  
#     candidate = b""
#     collisions = 0 
#     startTime = time()
#     while True:
#         for i in range(256):  
#             collisions += 1
#             subCandidate = bytes([i]) + candidate
#             if arbitrary_hash_trunc(subCandidate, trunc) == target_collision_out:
#                 print("Collisions: ", collisions)
#                 print("Time: ", time() - startTime)
#                 return (target_collision_in, candidate)
            
#         # Increment the candidate byte by byte
#         for j in range(len(candidate)):
#             if candidate[j] < 255:
#                 candidate = candidate[:j] + bytes([candidate[j] + 1]) + candidate[j+1:]
#                 break
#             else:
#                 candidate = bytes([0]) + candidate
#     # while True:
#     #     for i in range (256):
#     #         collisions += 1
#     #         subCandidate = bytes([i]) + candidate
#     #         if arbitrary_hash_trunc(subCandidate, trunc) == target_collision_out:
#     #             print("Collisions: ", collisions)
#     #             print("Time: ", time() - startTime)
#     #             return (target_collision_in, candidate)
            
#     #     candidate = bytes([random.randint(0, 255)]) + candidate

# print(brute_force_collision(b"target"))

# def brute_force_collision(s, trunc):
#     target_collision_in = s
#     target_collision_out = arbitrary_hash_trunc(target_collision_in, trunc)
#     candidate = b""
#     collisions = 0
#     startTime = time()
#     len()
#     while True:

# def generate_all_combinations():
#     charset = [chr(i) for i in range(256)]
#     length = 1

#     while True:
#         password = [charset[0]]
#         yield ''.join(password)

#         # Increase the length and generate longer passwords
#         length += 1
#         print("this is the len:", length)
#         while len(password) < length:
#             carry = 1
#             i = 0
#             while carry != 0 and i < len(password):
#                 carry, code = divmod(ord(password[i]) + carry, 256)
#                 password[i] = charset[code]
#                 i += 1
#             if carry != 0:
#                 password.append(charset[carry])
#             yield ''.join(password)

#             # Exit loop if all characters are at the maximum value
#             if password[-1] == charset[-1]:
#                 break


# password_generator = generate_all_combinations()
# while True:
#     newPass = bytes(next(password_generator), 'utf-8') 
#     print(newPass)
#     if newPass == "target":
#         print("Found it")
#         break

def brute_force(trunc_size, s):
    target = arbitrary_hash_trunc(s, trunc_size)
    print("target", target)
    chars = [chr(i) for i in range(256)]
    count = 0
    startTime = time()
    for length in range(0, 256):
        for p in product(chars, repeat=length):
            count += 1
            guess = bytes(''.join(p), 'utf-8')
            print("guess", guess)
            if arbitrary_hash_trunc(guess, trunc_size) == target:
                print("Collisions: ", count)
                print("Time: ", time() - startTime)
                return guess


# for i in range (8, 51, 2):
#     print(i)


    # brute_force_collision(b"target", i)
print(brute_force(10, b'target'))
    