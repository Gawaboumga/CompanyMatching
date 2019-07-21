from .MatchingType import MatchingType
from .MatchingResult import MatchingResult

__all__ = ['Pipeline', 'make_pipeline']


class Pipeline:

    def __init__(self, steps):
        self.steps = steps

    def match(self, lhs, rhs, original_lhs, original_rhs, **parameters):
        for step in self.steps:
            step.additional_flag = MatchingType.NoMatch

        for i in range(len(self.steps)):
            result, lhs, rhs = self.steps[i].match(lhs, rhs, original_lhs, original_rhs, **parameters)
            if result is not None:
                for j in range(i):
                    result.kind |= self.steps[j].additional_flag
                return result, lhs, rhs
        return MatchingResult.NoMatch(), lhs, rhs

    def __len__(self):
        return len(self.steps)

def make_pipeline(*steps):
    return Pipeline(steps)
