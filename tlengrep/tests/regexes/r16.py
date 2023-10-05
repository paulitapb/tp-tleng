from regex import Char, Plus, Union

# (a|b)+
__regex__ = Plus(Union(Char('a'), Char('b')))

__should_match__ = r"(a|b)+"

__min_afd_size__ = 2
