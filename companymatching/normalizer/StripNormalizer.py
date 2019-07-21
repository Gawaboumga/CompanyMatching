from ..base import NormalizerMixin


class StripNormalizer(NormalizerMixin):

    def normalize(self, lhs, rhs, original_lhs, original_rhs, **parameters):
        return lhs.strip(), rhs.strip()
