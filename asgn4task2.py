import bcrypt
from nltk.corpus import words
import nltk
from concurrent.futures import ThreadPoolExecutor

# First-time NLTK setup: download the 'words' corpus
nltk.download('words')

# The target hash string from the shadow.docx
target_hash_str = "$2b$08$J9FW66ZdPI2nrIMcOxFYI.qx268uZn.ajhymLP/YHaAsfBGP3Fnmq"
# Extracting the salt (includes cost factor and salt, the first 29 characters)
salt = target_hash_str[:29].encode()

# Getting the list of words from NLTK; filtering for length between 6 and 10
word_list = [w for w in words.words() if 6 <= len(w) <= 10]

# Function to attempt cracking the bcrypt hash
def attempt_crack(word):
    word_bytes = word.encode()
    hashed_word = bcrypt.hashpw(word_bytes, salt)
    if hashed_word == target_hash_str.encode():
        return word
    return None

# Using ThreadPoolExecutor to utilize multiple threads
def crack_bcrypt_hash_parallel():
    with ThreadPoolExecutor(max_workers=24) as executor:
        futures = [executor.submit(attempt_crack, word) for word in word_list]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result is not None:
                return result
    return None

# Attempt to crack the hash in parallel
plaintext_password = crack_bcrypt_hash_parallel()

if plaintext_password:
    print(f"Cracked! The plaintext password is: {plaintext_password}")
else:
    print("Failed to crack the password.")
