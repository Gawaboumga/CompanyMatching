from .MatchingType import MatchingType


class MatchingResult:
    def __init__(self, score=0, kind=0):
        self.score = score
        self.kind = kind

    @staticmethod
    def NoMatch():
        return MatchingResult(0, MatchingType.NoMatch)
