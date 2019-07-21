from ..base import NormalizerMixin
from ..MatchingType import MatchingType


class AbbreviationLegalFormNormalizer(NormalizerMixin):

    def normalize(self, lhs, rhs, original_lhs, original_rhs, **parameters):
        abbreviations_lhs = lhs[0]
        company_words_lhs = lhs[1]
        abbreviations_rhs = rhs[0]
        company_words_rhs = rhs[1]

        original_length = len(abbreviations_lhs) + len(company_words_rhs) + len(abbreviations_rhs) + len(company_words_lhs)
        self.__remove_abbreviations_of_company_words(abbreviations_lhs, company_words_rhs)
        self.__remove_abbreviations_of_company_words(abbreviations_rhs, company_words_lhs)

        remaining_length = len(abbreviations_lhs) + len(company_words_rhs) + len(abbreviations_rhs) + len(company_words_lhs)
        if original_length != remaining_length:
            self.additional_flag = MatchingType.Shorthand

        return lhs, rhs

    def __remove_abbreviations_of_company_words(self, abbreviations, company_words):
        abbreviations_to_remove = set()
        company_words_to_remove = set()
        considered = [False for _ in range(len(company_words))]
        for abbreviation, abbreviation_elfs in abbreviations.items():
            for index, (company_word, company_elfs) in enumerate(company_words.items()):
                if not considered[index]:
                    if len(abbreviation_elfs.intersection(company_elfs)) > 0:
                        abbreviations_to_remove.add(abbreviation)
                        company_words_to_remove.add(company_word)
                        considered[index] = True

        for abbreviation_to_remove in abbreviations_to_remove:
            del abbreviations[abbreviation_to_remove]
        for company_word_to_remove in company_words_to_remove:
            del company_words[company_word_to_remove]

        return abbreviations, company_words
