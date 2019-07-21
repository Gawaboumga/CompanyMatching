from ..base import ComparerMixin
from ..MatchingResult import MatchingResult, MatchingType


class InitialComparer(ComparerMixin):

    def __init__(self, pipeline):
        super()
        self.__pipeline = pipeline


    def compare(self, lhs, rhs, original_lhs, original_rhs, **parameters):
        shortest, longest = lhs, rhs
        if len(shortest) > len(longest):
            shortest, longest = rhs, lhs

        tokens_shortest = shortest.split()
        tokens_longest = longest.split()

        for short_index, token in enumerate(tokens_shortest):
            if len(token) < parameters.get("maximal_initialism", 5) and len(token) < len(tokens_longest):
                initial_index = 0
                first_initial = token[initial_index]
                for i in range(len(tokens_longest)):
                    if tokens_longest[i][0] == first_initial:
                        j = i + 1
                        initial_index += 1
                        while j != len(tokens_longest) and initial_index != len(token):
                            if tokens_longest[j][0] == token[initial_index]:
                                initial_index += 1
                                j += 1
                            else:
                                break

                        # If we have eventually a match of abbreviations
                        if initial_index == len(token):
                            result, _, _ = self.__pipeline.match(
                                u''.join(tokens_shortest[short_index + 1:]),
                                u''.join(tokens_longest[:i] + tokens_longest[i + initial_index:]),
                                original_lhs,
                                original_rhs,
                                **parameters)
                            if result.kind != MatchingType.NoMatch:
                                result.kind |= MatchingType.Initials
                                return result
