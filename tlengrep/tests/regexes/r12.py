from regex import Char, Lambda, Union

# a|λ
__regex__ = Union(Char('a'), Lambda())

__should_match__ = r"a|"

__min_afd_size__ = 3
