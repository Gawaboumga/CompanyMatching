from ..base import NormalizerMixin
from ..MatchingType import MatchingType


class OtherWordsAbbreviationNormalizer(NormalizerMixin):

    def __init__(self, abbreviations):
        self.abbreviations = abbreviations

    def normalize(self, lhs, rhs, original_lhs, original_rhs, **parameters):
        original_length = len(lhs)
        lhs_to_remove = set()
        rhs_to_remove = set()

        considered_lhs = [False for _ in range(len(lhs))]
        considered_rhs = [False for _ in range(len(rhs))]
        for index, l in enumerate(lhs):
            other = self.abbreviations.get(l, None)
            if other is not None and other in rhs:
                pos = rhs.index(other)
                if pos != -1 and considered_rhs[pos] == False:
                    considered_lhs[index] = True
                    considered_rhs[pos] = True
                    lhs_to_remove.add(l)
                    rhs_to_remove.add(other)

        for index, l in enumerate(rhs):
            if not considered_rhs[index]:
                other = self.abbreviations.get(l, None)
                if other is not None and other in lhs:
                    pos = lhs.index(other)
                    if pos != -1 and considered_lhs[pos] == False:
                        considered_lhs[index] = True
                        considered_rhs[pos] = True
                        lhs_to_remove.add(l)
                        rhs_to_remove.add(other)

        for to_remove in lhs_to_remove:
            lhs.remove(to_remove)
        for to_remove in rhs_to_remove:
            rhs.remove(to_remove)

        if original_length != len(lhs):
            self.additional_flag |= MatchingType.Abbreviation

        return lhs, rhs
