from ..base import ComparerMixin
from ..MatchingResult import MatchingResult, MatchingType
from .LevenshteinComparer import LevenshteinComparer


class OtherWordsComparer(ComparerMixin):

    def compare(self, lhs, rhs, original_lhs, original_rhs, **parameters):
        
        levenshteinComparer = LevenshteinComparer()
        return levenshteinComparer.compare(u''.join(lhs), u''.join(rhs), original_lhs, original_rhs)
