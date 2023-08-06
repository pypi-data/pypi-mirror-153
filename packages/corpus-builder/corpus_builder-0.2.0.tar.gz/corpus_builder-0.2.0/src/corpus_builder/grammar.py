from corpus_builder.exceptions import RuleNotFoundException

class Grammar:
    """BNF Grammar that defines the domain corpus
    """

    def __init__(self, rules, root):
        """Defines the grammar with its derivation rules and root

        Args:
            rules ([Rule]): Collection of derivation rules of the grammar
            root (str): Non terminal element that defines the starting point of 
                the generation process. Should match the key of one of the rules,
                which will be the first one to be expanded.
        """
        self._rules = {rule.key: rule for rule in rules}
        self.root = root

    def is_non_terminal(self, token):
        """Check if token is a terminal of this grammar

        Args:
            token (str): grammar element to be verified

        Returns:
            bool: True if token in considered a non terminal
        """
        return token.startswith('<')

    def get_rule(self, key):
        if key not in self._rules:
            raise RuleNotFoundException('Could not find rule with key', key)
        else:
            return self._rules[key]
