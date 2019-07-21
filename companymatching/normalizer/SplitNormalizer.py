from ..base import NormalizerMixin


class SplitNormalizer(NormalizerMixin):

    def normalize(self, lhs, rhs, original_lhs, original_rhs, **parameters):
        return lhs.split(), rhs.split()
