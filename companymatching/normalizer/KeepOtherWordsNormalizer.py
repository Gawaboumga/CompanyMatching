from ..base import NormalizerMixin


class KeepOtherWordsNormalizer(NormalizerMixin):

    def normalize(self, lhs, rhs, original_lhs, original_rhs, **parameters):
        normalized_lhs = lhs[2]
        normalized_rhs = rhs[2]
        return normalized_lhs, normalized_rhs
