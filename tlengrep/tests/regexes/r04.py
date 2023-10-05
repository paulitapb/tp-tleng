from regex import Char, Concat

# ab
__regex__ = Concat(Char('a'), Char('b'))

__should_match__ = r"ab"

__min_afd_size__ = 4
