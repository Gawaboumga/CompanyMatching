from .MatchingType import MatchingType


class MatcherMixin:

    additional_flag = MatchingType.NoMatch

    def match(self, lhs, rhs, original_lhs, original_rhs, **parameters):
        new_lhs, new_rhs = self.normalize(lhs, rhs, original_lhs, original_rhs, **parameters)
        return self.compare(new_lhs, new_rhs, original_lhs, original_rhs, **parameters), new_lhs, new_rhs

    def compare(self, lhs, rhs, original_lhs, original_rhs, **parameters):
        return None

    def normalize(self, lhs, rhs, original_lhs, original_rhs, **parameters):
        return lhs, rhs


class ComparerMixin(MatcherMixin):

    def compare(self, lhs, rhs, original_lhs, original_rhs, **parameters):
        return self.compare(lhs, rhs, original_lhs, original_rhs, **parameters), lhs, rhs


class NormalizerMixin(MatcherMixin):

    def normalize(self, lhs, rhs, original_lhs, original_rhs, **parameters):
        return self.normalize(lhs, rhs, original_lhs, original_rhs, **parameters)
