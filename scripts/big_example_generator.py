import uuid
import random

with open('/usr/share/dict/words', 'r') as f:
    words = f.read().splitlines()

with open('big_example.data, 'w') as f:
    for i in range(1000000):
        key = str(uuid.uuid4())

        value = ' '.join(random.sample(words, random.randint(3, 6)))

        f.write(f"{key} {value}\n")
