from abc import ABC, abstractmethod

from automata import AFND

__all__ = [
    "RegEx",
    "Empty",
    "Lambda",
    "Char",
    "Union",
    "Concat",
    "Star",
    "Plus"
]


class RegEx(ABC):
    """Clase abstracta para representar expresiones regulares."""

    @abstractmethod
    def naive_match(self, word: str) -> bool:
        """
        Indica si la expresión regular acepta la cadena dada.
        Implementación recursiva, poco eficiente.
        """
        pass

    def match(self, word: str) -> bool:
        """Indica si la expresión regular acepta la cadena dada."""
        raise NotImplementedError

    @abstractmethod
    def to_afnd(self) -> AFND:
        """Convierte la expresión regular a un AFND."""
        pass

    @abstractmethod
    def _atomic(self) -> bool:
        """
        (Interno) Indica si la expresión regular es atómica. Útil para
        implementar la función __str__.
        """
        pass


class Empty(RegEx):
    """Expresión regular que denota el lenguaje vacío (∅)."""

    def naive_match(self, word: str):
        return False

    def to_afnd(self) -> AFND:
        return AFND()

    def _atomic(self):
        return True

    def __str__(self):
        return "∅"


class Lambda(RegEx):
    """Expresión regular que denota el lenguaje de la cadena vacía (Λ)."""

    def naive_match(self, word: str):
        return word == ""

    def to_afnd(self) -> AFND:
        automata = AFND() 
        automata.add_state('q0', True)
        automata.mark_initial_state('q0')
        return automata 

    def _atomic(self):
        return True

    def __str__(self):
        return "λ"


class Char(RegEx):
    """Expresión regular que denota el lenguaje de un determinado carácter."""

    def __init__(self, char: str):
        assert len(char) == 1
        self.char = char

    def naive_match(self, word: str):
        return word == self.char

    def to_afnd(self) -> AFND:
        automata = AFND()
        automata.add_state('q0', False) 
        automata.add_state('q1',True)
        automata.add_transition('q0','q1',self.char) 
        automata.mark_initial_state('q0')
        return automata
        
    def _atomic(self):
        return True

    def __str__(self):
        return self.char


class Concat(RegEx):
    """Expresión regular que denota la concatenación de dos expresiones regulares."""

    def __init__(self, exp1: RegEx, exp2: RegEx):
        self.exp1 = exp1
        self.exp2 = exp2

    def naive_match(self, word: str):
        for i in range(len(word) + 1):
            if self.exp1.naive_match(word[:i]) and self.exp2.naive_match(word[i:]):
                return True
        return False

    def to_afnd(self) -> AFND:
        automata_exp1 = self.exp1.to_afnd() 
        automata_exp2 = self.exp2.to_afnd()
        
        final_automata = AFND()
        for state in automata_exp1.states:
            final_automata.add_state(state+'_1',False)
            if state == automata_exp1.initial_state:
                final_automata.mark_initial_state(state+'_1')
        
        for state in automata_exp2.states: 
            final_automata.add_state(state+'_2', state in automata_exp2.final_states)
        
        self._add_transitions(automata_exp1, final_automata,'_1')
        self._add_transitions(automata_exp2, final_automata,'_2') 

        for final_state in automata_exp1.final_states:
            final_automata.add_transition(final_state+'_1',automata_exp2.initial_state+'_2','λ')
        
        return final_automata.normalize_states() 
    
    def _add_transitions(self, automata_exp1, final_automata,identifier):
        for stateFrom,transitionFrom in automata_exp1.transitions.items():
            for symbol,destinationStates in transitionFrom.items():
                for statesTo in destinationStates: 
                    final_automata.add_transition(stateFrom+identifier,statesTo+identifier,symbol)

    def _atomic(self):
        return False

    def __str__(self):
        return f"{f'({self.exp1})' if not self.exp1._atomic() else self.exp1}" \
            f"{f'({self.exp2})' if not self.exp2._atomic() else self.exp2}"


class Union(RegEx):
    """Expresión regular que denota la unión de dos expresiones regulares."""

    def __init__(self, exp1: RegEx, exp2: RegEx):
        self.exp1 = exp1
        self.exp2 = exp2

    def naive_match(self, word: str):
        return self.exp1.naive_match(word) or self.exp2.naive_match(word)

    def to_afnd(self) -> AFND:
        automata_exp1 = self.exp1.to_afnd()
        automata_exp2 = self.exp2.to_afnd()
        final_automata = AFND()
        
        for state in automata_exp1.states:
            final_automata.add_state(state+'_1',state in automata_exp1.final_states)
        
        for state in automata_exp2.states: 
            final_automata.add_state(state+'_2', state in automata_exp2.final_states)

        self._add_transitions(automata_exp1, final_automata,'_1')
        self._add_transitions(automata_exp2, final_automata,'_2')
        final_automata.add_state('q0',False)
        final_automata.mark_initial_state('q0')
        final_automata.add_transition('q0',automata_exp1.initial_state+'_1','λ')
        final_automata.add_transition('q0',automata_exp2.initial_state+'_2','λ')
        
        return final_automata.normalize_states()
    
    def _add_transitions(self, automata_exp1, final_automata,identifier):
        for stateFrom,transitionFrom in automata_exp1.transitions.items():
            for symbol,destinationStates in transitionFrom.items():
                for statesTo in destinationStates: 
                    final_automata.add_transition(stateFrom+identifier,statesTo+identifier,symbol)

    def _atomic(self):
        return False

    def __str__(self):
        return f"{f'({self.exp1})' if not self.exp1._atomic() else self.exp1}" \
            f"|{f'({self.exp2})' if not self.exp2._atomic() else self.exp2}"


class Star(RegEx):
    """Expresión regular que denota la clausura de Kleene de otra expresión regular."""

    def __init__(self, exp: RegEx):
        self.exp = exp

    def naive_match(self, word: str):
        if word == "" or self.exp.naive_match(word):
            return True
        for i in range(1, len(word) + 1):
            if self.exp.naive_match(word[:i]) and self.naive_match(word[i:]):
                return True
        return False

    def to_afnd(self) -> AFND:
        automata_exp = self.exp.to_afnd()
        
    
        automata_exp.add_state("q0'",True)

        
        automata_exp.add_transition("q0'",automata_exp.initial_state,'λ')
        automata_exp.mark_initial_state("q0'")

        for final_state in automata_exp.final_states:
            automata_exp.add_transition(final_state,automata_exp.initial_state+'_1','λ')
        return automata_exp.normalize_states()

    def _atomic(self):
        return False

    def __str__(self):
        return f"({self.exp})*" if not self.exp._atomic() else f"{self.exp}*"


class Plus(RegEx):
    """Expresión regular que denota la clausura positiva de otra expresión regular."""

    def __init__(self, exp: RegEx):
        self.exp = exp

    def naive_match(self, word: str):
        if self.exp.naive_match(word):
            return True
        for i in range(1, len(word) + 1):
            if self.exp.naive_match(word[:i]) and self.naive_match(word[i:]):
                return True
        return False

    def to_afnd(self) -> AFND:
        automata_exp = self.exp.to_afnd()
        
        for final_state in automata_exp.final_states: 
            automata_exp.add_transition(final_state,automata_exp.initial_state,'λ') 
        return automata_exp

    def _atomic(self) -> bool:
        return False

    def __str__(self):
        return f"({self.exp})+" if not self.exp._atomic() else f"{self.exp}+"
