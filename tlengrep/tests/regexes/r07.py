from regex import Char, Concat, Union

# ab|cd
__regex__ = Union(Concat(Char('a'), Char('b')), Concat(Char('c'), Char('d')))

__should_match__ = r"ab|cd"

__min_afd_size__ = 5
