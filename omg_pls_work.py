from bcrypt import hashpw
import time
from nltk.corpus import words
import nltk
from concurrent.futures import ProcessPoolExecutor

# Ensure the 'words' dataset is downloaded
nltk.download('words')

class Password: 
    def __init__(self, shadow_line): 
        self.user = shadow_line[0][:-1]
        self.algo = shadow_line[1] 
        self.workfactor = shadow_line[2]
        self.salt = shadow_line[3][:22]
        self.hash = shadow_line[3][22:]

def crack(person):
    hashpw_input = "$".join((person.algo, person.workfactor, person.salt))
    wordlist = [word for word in words.words() if len(word) <= 10 and len(word) >= 6]
    for word in wordlist: 
        hashed = hashpw(word.encode("utf-8"), hashpw_input.encode("utf-8"))
        if hashed[29:] == person.hash: 
            print(f"Password for {person.user} is {word}")
            return
    print(f"Password for {person.user} not found")

def main(): 
    shadow = []
    with open("shadow.txt", "r") as f: 
        for line in f:
            shadow.append(Password(line.split("$")))
    
    # Use ProcessPoolExecutor to utilize all cores
    with ProcessPoolExecutor() as executor:
        # Map the crack function to each person in the shadow list
        results = executor.map(crack, shadow)
        
        # Optional: Process results if necessary
        for result in results:
            pass  # Results are handled inside the crack function

if __name__ == "__main__":
    main()