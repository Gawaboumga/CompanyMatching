from ..base import NormalizerMixin


class AndNormalizer(NormalizerMixin):

    def __init__(self, and_words):
        self.and_words = and_words

    def normalize(self, lhs, rhs, original_lhs, original_rhs, **parameters):
        return self.__remove_ands(lhs, rhs)

    def __remove_ands(self, lhs, rhs):
        if not ('&' in lhs or '&' in rhs):
            return lhs, rhs

        if '&' in lhs:
            rhs = list(filter(lambda x: x not in self.and_words, rhs))
            lhs = filter(lambda x: x != '&', lhs)
        if '&' in rhs:
            lhs = filter(lambda x: x not in self.and_words, lhs)
            rhs = filter(lambda x: x != '&', rhs)
        return list(lhs), list(rhs)