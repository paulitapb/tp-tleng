from typing import Hashable
from automata.af import AF

__all__ = ["AFD"]


class AFD(AF):
    """Autómata finito determinístico."""

    def add_transition(self, state1: Hashable, state2: Hashable, char: str):
        """Agrega una transición al autómata."""
        if state1 not in self.states:
            raise ValueError(f"El estado {state1} no pertenece al autómata.")
        if state2 not in self.states:
            raise ValueError(f"El estado {state2} no pertenece al autómata.")
        self.transitions[state1][char] = state2
        self.alphabet.add(char)

    def minimize(self):
        """Minimiza el autómata."""
        raise NotImplementedError

    def _rename_state_in_transitions(self, old_name: Hashable, new_name: Hashable):
        """Renombra un estado dentro de las transiciones del autómata."""
        self.transitions[new_name] = self.transitions[old_name]
        del self.transitions[old_name]
        for state in self.transitions:
            for char in self.transitions[state]:
                if self.transitions[state][char] == old_name:
                    self.transitions[state][char] = new_name

    def _get_extended_alphabet(self) -> list[str]:
        """Obtiene el alfabeto extendido del autómata (incluyendo símbolos especiales)."""
        return list(self.alphabet)

    def _transitions_to_str(self, state: Hashable) -> dict[Hashable, str]:
        """Devuelve las transiciones de un estado para cada símbolo como string."""
        transitions = {}
        for char in self._get_extended_alphabet():
            if char in self.transitions[state]:
                transitions[char] = self.transitions[state][char]
            else:
                transitions[char] = "-"
        return transitions
