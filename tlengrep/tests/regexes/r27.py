from regex import Char, Union, Plus, Concat, Star, Empty

# (a|b|c)(d|e)+f|g*|∅
__regex__ = Union(
    Concat(
        Union(Char('a'), Union(Char('b'), Char('c'))),
        Concat(
            Plus(Union(Char('d'), Char('e'))),
            Char('f')
        )
    ),
    Union(
        Star(Char('g')),
        Empty()
    )
)

__should_match__ = r"(a|b|c)(d|e)+f|g*"

__min_afd_size__ = 6
