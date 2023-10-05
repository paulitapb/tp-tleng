from regex import Char, Union, Star

# (a|b)*
__regex__ = Star(Union(Char('a'), Char('b')))

__should_match__ = r"(a|b)*"

__min_afd_size__ = 1
