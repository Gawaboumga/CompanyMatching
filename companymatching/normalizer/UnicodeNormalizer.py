from ..base import NormalizerMixin
import unicodedata


class UnicodeNormalizer(NormalizerMixin):

    def normalize(self, lhs, rhs, original_lhs, original_rhs, **parameters):
        normalized_lhs = self.__normalize(lhs)
        normalized_rhs = self.__normalize(rhs)
        return normalized_lhs, normalized_rhs

    def __normalize(self, input_str):
        nfkd_form = unicodedata.normalize('NFKD', input_str.casefold())
        return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
