from regex import Char, Union, Star, Concat

# (a|b)c*
__regex__ = Concat(Union(Char('a'), Char('b')), Star(Char('c')))

__should_match__ = r"(a|b)c*"

__min_afd_size__ = 3
