from regex import Plus, Char

# a+
__regex__ = Plus(Char('a'))

__should_match__ = r"a+"

__min_afd_size__ = 2
