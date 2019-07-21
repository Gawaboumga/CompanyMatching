from ..base import NormalizerMixin
from ..MatchingType import MatchingType


class CommonAbbreviationNormalizer(NormalizerMixin):

    def normalize(self, lhs, rhs, original_lhs, original_rhs, **parameters):
        abbreviations_lhs = lhs[0]
        abbreviations_rhs = rhs[0]

        abbreviations_lhs_to_remove = []
        abbreviations_rhs_to_remove = []
        considered = [False for _ in range(len(rhs))]
        for abbreviation_lhs, elfs_lhs in abbreviations_lhs.items():
            for index, (abbreviation_rhs, elfs_rhs) in enumerate(abbreviations_rhs.items()):
                if not considered[index]:
                    if len(elfs_lhs.intersection(elfs_rhs)) > 0:
                        abbreviations_lhs_to_remove.append(abbreviation_lhs)
                        abbreviations_rhs_to_remove.append(abbreviation_rhs)
                        considered[index] = True
                        break

        for abbreviation_to_remove in abbreviations_lhs_to_remove:
            del abbreviations_lhs[abbreviation_to_remove]
        for abbreviation_to_remove in abbreviations_rhs_to_remove:
            del abbreviations_rhs[abbreviation_to_remove]

        if len(abbreviations_lhs_to_remove) + len(abbreviations_rhs_to_remove) > 0:
            self.additional_flag = MatchingType.Synonym

        return lhs, rhs
