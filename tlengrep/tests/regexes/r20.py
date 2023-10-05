from regex import Star, Union, Char, Plus

# a*|b+
__regex__ = Union(Star(Char('a')), Plus(Char('b')))

__should_match__ = r"a*|b+"

__min_afd_size__ = 4
