import Levenshtein
import unicodedata
from .MatchingParameters import MatchingParameters
from .MatchingResult import MatchingResult
from .MatchingType import MatchingType
from .elf.Elf import Elf, ElfType


class DefaultMatching:   

    def __init__(self, default_parameters=None):
        if default_parameters is None:
            self.default_parameters = MatchingParameters.default()
        else:
            self.default_parameters = default_parameters

        from .Pipeline import make_pipeline
        from .normalizer import UnicodeNormalizer
        from .normalizer import CharacterNormalizer
        from .normalizer import MisplacedCharacterNormalizer
        from .comparer import LevenshteinComparer
        from .comparer import InitialComparer
        from .normalizer import SplitNormalizer
        from .normalizer import TokenCategoryNormalizer
        from .normalizer import AbbreviationLegalFormNormalizer
        from .normalizer import CommonAbbreviationNormalizer
        from .comparer import TokenCategoryComparer
        from .normalizer import KeepOtherWordsNormalizer
        from .normalizer import AndNormalizer
        from .normalizer import OtherWordsAbbreviationNormalizer
        from .comparer import OtherWordsComparer

        handle_company_words = make_pipeline(
            SplitNormalizer(),
            TokenCategoryNormalizer(),
            AbbreviationLegalFormNormalizer(), CommonAbbreviationNormalizer(),
            TokenCategoryComparer(),
            KeepOtherWordsNormalizer(), AndNormalizer(self.default_parameters.and_words),
            OtherWordsAbbreviationNormalizer(self.default_parameters.abbreviations),
            OtherWordsComparer()
        )

        self.__pipeline = make_pipeline(
            UnicodeNormalizer(), CharacterNormalizer(self.default_parameters.meaningless_characters_without_dot), MisplacedCharacterNormalizer(),
            LevenshteinComparer(),
            InitialComparer(handle_company_words),
            handle_company_words
        )

    def match(self, lhs, rhs, **parameters):
        default_parameters = vars(self.default_parameters)
        default_parameters.update(parameters)
        return self.__pipeline.match(lhs, rhs, lhs, rhs, **default_parameters)[0]
