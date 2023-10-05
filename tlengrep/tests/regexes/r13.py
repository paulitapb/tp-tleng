from regex import Empty, Char, Union

# a|∅
__regex__ = Union(Char('a'), Empty())

__should_match__ = r"a"

__min_afd_size__ = 3
