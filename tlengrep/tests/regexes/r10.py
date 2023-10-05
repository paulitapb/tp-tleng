from regex import Lambda, Char, Concat

# abλ
__regex__ = Concat(Char('a'), Concat(Char('b'), Lambda()))

__should_match__ = r"ab"

__min_afd_size__ = 4
