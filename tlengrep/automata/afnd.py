from enum import Enum
from typing import Hashable, Union

from automata.af import AF
from automata.afd import AFD


__all__ = ["AFND"]


class SpecialSymbol(Enum):
    Lambda = "λ"


class AFND(AF):
    """Autómata finito no determinístico (con transiciones lambda)."""

    def add_transition(self, state1: Hashable, state2: Hashable, char: Union[str, SpecialSymbol]):
        """Agrega una transición al autómata."""
        if state1 not in self.states:
            raise ValueError(f"El estado {state1} no pertenece al autómata.")
        if state2 not in self.states:
            raise ValueError(f"El estado {state2} no pertenece al autómata.")
        if char not in self.transitions[state1]:
            self.transitions[state1][char] = set()
        self.transitions[state1][char].add(state2)
        if char is not SpecialSymbol.Lambda:
            self.alphabet.add(char)

    def determinize(self) -> AFD:
        """Determiniza el autómata."""

        states_to_visit = {self.initial_state}
        visited_states = set()
        
        old_transitions = self.transitions
        old_states = self.states
        old_finals = self.final_states

        self.transitions = dict()
        self.states = set()
        self.final_states = set()

        while len(states_to_visit) > 0: 
            current_state = states_to_visit.pop()
            
            for symb in self.alphabet: 
                new_state = self.mover(current_state, symb)
                states_to_visit.add(visited_states.difference(new_state))
                #TO DO: sort estados- no los estoy pasando a strings aun 
                self.add_state(new_state, any(lambda state: state in old_finals, new_state.keys()))
                self.add_transition(current_state, new_state, symb)

            visited_states.add(current_state)
        
        return self
    
    def mover(self, estado_desde, symb_cons):
    
        estados_alcanzables = dict(filter( 
            lambda state_from, symb_states : state_from == estado_desde , self.transitions.items()))
        return set(filter(lambda symbol, state_to: symbol == symb_cons, estados_alcanzables.items()))
    
    def _rename_state_in_transitions(self, old_name: Hashable, new_name: Hashable):
        """Renombra un estado dentro de las transiciones del autómata."""
        self.transitions[new_name] = self.transitions[old_name]
        del self.transitions[old_name]
        for state in self.transitions:
            for char in self.transitions[state]:
                if old_name in self.transitions[state][char]:
                    self.transitions[state][char].remove(old_name)
                    self.transitions[state][char].add(new_name)

    def _get_extended_alphabet(self) -> list[str]:
        """Obtiene el alfabeto extendido del autómata (incluyendo símbolos especiales)."""
        return list(self.alphabet) + [SpecialSymbol.Lambda]

    def _transitions_to_str(self, state: Hashable) -> dict[Hashable, str]:
        """Devuelve las transiciones de un estado para cada símbolo como string."""
        transitions = {}
        for char in self._get_extended_alphabet():
            if char in self.transitions[state]:
                transitions[char] = ",".join(self.transitions[state][char])
            else:
                transitions[char] = "-"
        return transitions
