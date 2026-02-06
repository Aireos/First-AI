import time

def is_even_second() -> bool:
    """Returns True if the current system second is even, False otherwise."""
    current_second = int(time.time())
    return current_second % 2 == 0

def random() -> bool:
  ""Smooths out is_even second with logic to make best home-made randomizer i can.""
  if is_even_second():
  else:
    
    
