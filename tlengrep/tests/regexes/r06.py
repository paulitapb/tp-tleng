from regex import Char, Union

# a|b|c
__regex__ = Union(Char('a'), Union(Char('b'), Char('c')))

__should_match__ = r"a|b|c"

__min_afd_size__ = 3
