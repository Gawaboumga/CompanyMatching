from ..base import NormalizerMixin
from ..elf.Elf import ElfType
from ..MatchingType import MatchingType


class TokenCategoryNormalizer(NormalizerMixin):

    def normalize(self, lhs, rhs, original_lhs, original_rhs, **parameters):
        new_lhs = self.__categorize_tokens(lhs, **parameters)
        new_rhs = self.__categorize_tokens(rhs, **parameters)
        return new_lhs, new_rhs

    def __categorize_tokens(self, tokens, **parameters):
        abbreviations = {}
        company_words = {}
        others = []

        elf = parameters["ELF"]
        transliterate_function = parameters.get("transliterate", None)

        for token in tokens:
            category, elfs = self.__categorize_token(token, parameters)
            if category == ElfType.Abbreviation or category == ElfType.TransliteratedAbbreviation:
                abbreviations[token] = elfs
            elif category == ElfType.LocalName or category == ElfType.TransliteratedLocalName:
                company_words[token] = elfs
            else:
                if transliterate_function is not None:
                    transliteration = transliterate_function(token)
                    if transliteration is None:
                        others.append(token)
                    else:
                        self.additional_flag = MatchingType.Transliteration
                        others.append(transliteration)
                else:
                    others.append(token)
        return abbreviations, company_words, others

    def __categorize_token(self, token, parameters):

        elf = parameters["ELF"]
        transliterate_function = parameters.get("transliterate", None)

        abbreviations_elfs = elf.get(ElfType.Abbreviation, token)
        local_names_elfs = elf.get(ElfType.LocalName, token)

        if abbreviations_elfs is None and local_names_elfs is None:
            if transliterate_function is None:
                return ElfType.Unknown, None
            
            transliterated_token = transliterate_function(token)
            transliterated_abbreviations_elfs = elf.get(ElfType.TransliteratedAbbreviation, transliterated_token)
            transliterated_local_names_elfs = elf.get(ElfType.TransliteratedLocalName, transliterated_token)
            if transliterated_abbreviations_elfs is None and transliterated_local_names_elfs is None:
                return ElfType.Unknown, None
            elif transliterated_abbreviations_elfs is None and transliterated_local_names_elfs is not None:
                return ElfType.LocalName, transliterated_local_names_elfs
            elif transliterated_abbreviations_elfs is not None and transliterated_local_names_elfs is None:
                return ElfType.Abbreviation, transliterated_abbreviations_elfs
            else:
                if len(transliterated_abbreviations_elfs) > len(transliterated_local_names_elfs):
                    return ElfType.Abbreviation, transliterated_abbreviations_elfs
                else:
                    return ElfType.LocalName, transliterated_local_names_elfs
            
        elif abbreviations_elfs is None and local_names_elfs is not None:
            return ElfType.LocalName, local_names_elfs
        elif abbreviations_elfs is not None and local_names_elfs is None:
            return ElfType.Abbreviation, abbreviations_elfs
        else:
            if len(abbreviations_elfs) > len(local_names_elfs):
                return ElfType.Abbreviation, abbreviations_elfs
            else:
                return ElfType.LocalName, local_names_elfs
