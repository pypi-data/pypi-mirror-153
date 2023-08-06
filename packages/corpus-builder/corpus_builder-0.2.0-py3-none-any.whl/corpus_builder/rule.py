import random

from corpus_builder.exceptions import InvalidRuleException

class Rule:

    def __init__(self, key, derivation):
        """Create e new derivation rule

        Args:
            key (str): a non-terminal element
            derivation (list, set, str): right side of the derivation rule,
            could be a sequence of tokens (list), a set of options to be choosen
            (set) or another token, terminal or non-terminal (str)
        """
        self.key = key
        self.derivation = derivation

    def expand(self):
        """General expansion of a rule in the BNF form

        Raises:
            InvalidRuleException: when rule could not be expandend, if is not str, tuple or list.

        Returns:
            [str]: result of applying this rule
        """
        if isinstance(self.derivation, str):
            return self.derivation
        elif isinstance(self.derivation, tuple):
            return random.choice(self.derivation)
        elif isinstance(self.derivation, list):
            return ' '.join(self.derivation)
        else:
            raise InvalidRuleException('Could not expand rule', self, 'because derivation type is invalid')

    def __str__(self):
        return f'Rule({self.key} -> {self.derivation})'