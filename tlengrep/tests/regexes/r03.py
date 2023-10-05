from regex import Char, Union

# a|b
__regex__ = Union(Char('a'), Char('b'))

__should_match__ = r"a|b"

__min_afd_size__ = 3
