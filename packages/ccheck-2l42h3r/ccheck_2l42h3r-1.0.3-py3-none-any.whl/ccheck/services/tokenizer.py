"""TokenizerService class module"""

from typing import List, Optional
import re
from functools import reduce

from ccheck.domain.rule import Rule
from ccheck.domain.token.token import Token
from ccheck.config import Config


class TokenizerService:
    """TokenizerService class"""

    __rules: List[Rule] = []

    def __init__(self, config: Config) -> None:
        self.__rules = config.rule_config

    @staticmethod
    def __rule_matches_text_predicate_factory(text: str, rule: Rule) -> bool:
        return re.search(rule.regex, text) is not None

    def __get_matching_rule(self, text: str) -> Optional[Rule]:
        val = next(
            (
                rule
                for rule in self.__rules
                if TokenizerService.__rule_matches_text_predicate_factory(text, rule)
            ),
            None,
        )
        return val

    def __get_max_text_index(self, text: str) -> int:
        i = 0

        while i < len(text):
            match = self.__get_matching_rule(text[0 : (i + 1)])
            if match is None:
                return i
            i += 1

        return i

    def __partial_tokenize(self, text: str) -> List[Token]:
        length = len(text)
        if length == 0:
            return []

        max_index = self.__get_max_text_index(text)

        if max_index == 0:
            return []

        match = text[0:max_index]
        rule = self.__get_matching_rule(match)

        if rule is None:
            return []

        tokens = [Token(rule.type, match)]

        tokens.extend(self.__partial_tokenize(text[max_index:length]))

        return tokens

    def tokenize(self, text: str) -> List[Token]:
        """Returns list of tokens found in given text"""
        tokens = list(filter(lambda t: len(t) > 0, re.split(r"(\s+)", text)))
        return reduce(lambda a, b: a + b, list(map(self.__partial_tokenize, tokens)))

    def add_rule(self, rule: Rule) -> None:
        """Adds a new token to instance's rule list"""
        self.__rules.append(rule)
