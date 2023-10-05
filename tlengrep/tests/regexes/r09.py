from regex import Char, Star

# a*
__regex__ = Star(Char('a'))

__should_match__ = r"a*"

__min_afd_size__ = 1
