from regex import Char, Union, Star, Concat

# (a|b)*c|d|e
__regex__ = Union(
    Concat(Star(Union(Char('a'), Char('b'))), Char('c')),
    Union(Char('d'), Char('e'))
)

__should_match__ = r"(a|b)*c|d|e"

__min_afd_size__ = 4
