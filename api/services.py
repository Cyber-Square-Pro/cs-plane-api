import random
import string

def generate_verification_code():
    alphabet = string.ascii_lowercase
    random_words = [''.join(random.sample(alphabet, 3)) for _ in range(3)]
    random_string = '-'.join(random_words)
    return random_string
