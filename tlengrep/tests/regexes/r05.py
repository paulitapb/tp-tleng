from regex import Char, Concat

# abc
__regex__ = Concat(Char('a'), Concat(Char('b'), Char('c')))

__should_match__ = r"abc"

__min_afd_size__ = 5
