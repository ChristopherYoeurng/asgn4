from bcrypt import hashpw, gensalt
import time
from nltk.corpus import words
import nltk
import multiprocessing

# Ensure nltk word list is downloaded (ideally, this should be done outside the script or in a setup routine)
nltk.download('words', quiet=True)

class Password: 
    def __init__(self, shadow_line): 
        self.user = shadow_line[0][:-1]
        self.algo = shadow_line[1] 
        self.workfactor = shadow_line[2]
        self.salt = shadow_line[3][:22]
        self.hash = shadow_line[3][22:]

def crack_chunk(wordlist_chunk, person):
    hashpw_input = "$".join((person.algo, person.workfactor, person.salt))
    # print(hashpw_input)
    for word in wordlist_chunk:
        hashed = hashpw(word.encode("utf-8"), hashpw_input.encode("utf-8"))
        # print(hashed)
        if hashed.decode()[29:] == person.hash:  # Ensure decoding if necessary
            return f"Password for {person.user} is {word}"
    return None

def crack(person):
    wordlist = [word for word in words.words() if 6 <= len(word) <= 10]
    
    # Split wordlist into chunks for multiprocessing
    cores = multiprocessing.cpu_count()
    chunk_size = len(wordlist) // cores
    wordlist_chunks = [wordlist[i:i + chunk_size] for i in range(0, len(wordlist), chunk_size)]
    print(cores)
    # Create a multiprocessing pool
    with multiprocessing.Pool(processes=cores) as pool:
        results = pool.starmap(crack_chunk, [(chunk, person) for chunk in wordlist_chunks])
        
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
        start_time = time.time()
        crack(person)
        print("Time taken:", time.time() - start_time)

if __name__ == "__main__":
    main()