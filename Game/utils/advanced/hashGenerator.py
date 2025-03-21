from string  import ascii_letters, digits
from secrets import choice


_letterPool = ascii_letters+digits
main        = lambda length=6: ''.join(choice(_letterPool)for _ in range(length))