from ..base import ComparerMixin
from ..MatchingResult import MatchingResult, MatchingType
import Levenshtein


class LevenshteinComparer(ComparerMixin):

    def compare(self, lhs, rhs, original_lhs, original_rhs, **parameters):

        edit = Levenshtein.distance(lhs, rhs)

        if edit <= parameters.get("maximal_typographies_in_raw", 1):
            ratio = self.__ratio_distance(edit, lhs, rhs)
            if edit == 0 and len(lhs) == len(rhs):
                return MatchingResult(ratio, MatchingType.Exact)
            else:
                return MatchingResult(ratio, MatchingType.Typography)

    def __ratio_distance(self, edit_score, lhs, rhs):
        if edit_score == 0:
            return 100
        else:
            len_sum = len(lhs) + len(rhs)
            return int(((len_sum - edit_score) / len_sum) * 100)
