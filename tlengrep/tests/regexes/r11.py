from regex import Empty, Char, Concat

# ∅a
__regex__ = Concat(Empty(), Char('a'))

__should_match__ = lambda string: False

__min_afd_size__ = 1
