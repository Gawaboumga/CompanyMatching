from ..base import ComparerMixin
from ..MatchingResult import MatchingResult, MatchingType
import Levenshtein


class TokenCategoryComparer(ComparerMixin):

    def compare(self, lhs, rhs, original_lhs, original_rhs, **parameters):
        abbreviations_lhs = lhs[0]
        company_words_lhs = lhs[1]
        abbreviations_rhs = rhs[0]
        company_words_rhs = rhs[1]

        number_of_entity_words = len(abbreviations_lhs) + len(company_words_lhs) + len(abbreviations_rhs) + len(company_words_rhs)
        if number_of_entity_words > parameters.get("maximal_entity_words_unmatched", 1):
            return MatchingResult.NoMatch()

        if number_of_entity_words > 0:
            self.additional_flag = MatchingType.Additional
