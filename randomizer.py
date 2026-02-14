import time


# goal is to have it make the fairest chance randomizer by constantly adjusting the chance based on the outcome of the last randomization
def is_even_second() -> bool:
    """Returns True if the current system second is even, False otherwise."""
    current_second = int(time.time())
    return current_second % 2 == 0

def random(wc,lc,cc) -> bool:
    # wc = wanted chance
    # lc = literal chance
    # cc = chance change