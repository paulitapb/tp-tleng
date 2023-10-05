from regex import Char, Union, Plus, Concat

# (a|b|c)+d|e|f
__regex__ = Union(
    Concat(Plus(Union(Char('a'), Union(Char('b'), Char('c')))), Char('d')),
    Union(Char('e'), Char('f'))
)

__should_match__ = r"(a|b|c)+d|e|f"

__min_afd_size__ = 4
