from regex import Char, Concat, Union

# a|bc
__regex__ = Union(Char('a'), Concat(Char('b'), Char('c')))

__should_match__ = r"a|bc"

__min_afd_size__ = 4
