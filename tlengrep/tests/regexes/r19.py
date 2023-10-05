from regex import Char, Concat, Plus

# (ab)+
__regex__ = Plus(Concat(Char('a'), Char('b')))

__should_match__ = r"(ab)+"

__min_afd_size__ = 4
