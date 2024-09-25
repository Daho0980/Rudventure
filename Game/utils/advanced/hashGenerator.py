from string  import ascii_letters, digits
from secrets import choice

letterPool = ascii_letters+digits

def main(length:int=6) -> str:
    return ''.join(choice(letterPool)for _ in range(length))