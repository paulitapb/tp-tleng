from regex import Char, Union, Star, Concat, Empty

# (a|b)(cd|ef)*g|h|∅
__regex__ = Union(
    Concat(
        Union(Char('a'), Char('b')),
        Concat(
            Star(Union(
                Concat(Char('c'), Char('d')),
                Concat(Char('e'), Char('f'))
            )),
            Char('g')
        )
    ),
    Union(
        Char('h'),
        Empty()
    )
)

__should_match__ = r"(a|b)(cd|ef)*g|h"

__min_afd_size__ = 6
