import random

while True:
    num = random.randint(0, 1)
    num = num if num > 0 else -1
    print((num * 15) + (random.randint(0, 15) if num > 0 else random.randint(-15, 0)))