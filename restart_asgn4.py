from Crypto.Hash import SHA256
import random
import string
import time

def arbitrary_hash(s):
    h = SHA256.new()
    h.update(s)
    bytes = bytearray(h.digest())
    print(' '.join(hex(a) for a in bytes))

def arbitrary_hash_trunc(s, trunc):
    # Convert bits into bytes, adding 1 if the truncation is not on an 8-bit boundary
    numBytes = trunc // 8 + (1 if trunc % 8 != 0 else 0)
    
    # Calculate  hash and truncate to the specified number of bytes.
    h = SHA256.new()
    h.update(s)
    bytes = bytearray(h.digest())[:numBytes]
    
    # Only take the higher order bits when truncating to a non-8-bit boundary.
    if trunc % 8 != 0:
        mask = 0xFF << (8 - (trunc % 8)) & 0xFF
        bytes[-1] &= mask
    
    # Convert the truncated bytes back to a hexadecimal string.
    return ''.join(format(a, '02x') for a in bytes)

def find_collisions():
    for trunc in range(8, 51, 2): 
        # Store hashes we've already computed
        seen_hashes = {} 
        count = 0
        start_time = time.time()
        while True:
            # Generates string and hash
            random_str = (''.join(random.choices(string.ascii_letters + string.digits, k=10))).encode('utf-8')
            new_hash = arbitrary_hash_trunc(random_str, trunc)
            # Check for collisions
            if new_hash in seen_hashes:
                print(f"Collision found for {trunc} bits: {random_str} and {seen_hashes[new_hash]} with hash {new_hash}")
                print("Number of messages attempted:", count)
                print("Time taken:", time.time() - start_time)
                break 
            else:
                seen_hashes[new_hash] = random_str
            count += 1

def main():
    # arbitrary_hash(b"hello")
    # arbitrary_hash(b"iello")

    # print("\n\n")
    # arbitrary_hash(b"aslalsdkfja")
    # arbitrary_hash(b"aslblsdkfja")
    # print("\n\n")
    # arbitrary_hash(b"zzzzzzzzzz")
    # arbitrary_hash(b"zzzzyzzzzz")

    # print(arbitrary_hash_trunc(b"hello", 16))
    # print(arbitrary_hash_trunc(b"hello", 2))
    # print(arbitrary_hash_trunc(b"hello", 24))

    find_collisions()
     

if __name__ == "__main__":
    main()