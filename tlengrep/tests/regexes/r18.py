from regex import Char, Concat, Star

# (ab)*
__regex__ = Star(Concat(Char('a'), Char('b')))

__should_match__ = r"(ab)*"

__min_afd_size__ = 3
