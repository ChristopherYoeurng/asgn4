from bcrypt import * 
from nltk.corpus import words 
import nltk
import multiprocessing

class Password: 
    def __init__(self, shadow_line): 
        self.user = shadow_line[0][:-1]
        self.algo = shadow_line[1] 
        self.workfactor = shadow_line[2]
        self.salt = shadow_line[3][:22]
        self.hash = shadow_line[3][22:]

def crack_chunk(wordlist_chunk, hashpw_input, hash, user):
    for word in wordlist_chunk:
        hashed = hashpw(word, bytes(hashpw_input.encode("utf-8")))
        if hashed == hash:
            return f"Password for {user} is {word}"
    return None

def crack(person):
    hashpw_input = "$".join((person.algo, person.workfactor, person.salt))
    wordlist = [word for word in words.words() if 6 <= len(word) <= 10]
    
    # Split wordlist into chunks for each core
    cores = multiprocessing.cpu_count()
    chunk_size = len(wordlist) // cores
    wordlist_chunks = [wordlist[i:i + chunk_size] for i in range(0, len(wordlist), chunk_size)]
    
    # Create a multiprocessing Pool
    pool = multiprocessing.Pool(processes=cores)
    print(cores)
    
    # Use map to distribute the workload
    results = pool.starmap(crack_chunk, [(chunk, hashpw_input, person.hash, person.user) for chunk in wordlist_chunks])
    
    # Close the pool and wait for the work to finish
    pool.close()
    pool.join()
    
    # Process results
    for result in results:
        if result:
            print(result)
            return
    
    print(f"Password for {person.user} not found")

def main(): 
    shadow = []
    with open("shadow.txt", "r") as f: 
        for line in f:
            shadow.append(Password(line.split("$")))
    
    for person in shadow:
        crack(person)
if __name__ == "__main__":
    main()
