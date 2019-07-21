from .elf import Elf


class MatchingParameters:
    __MEANINGLESS_CHARACTERS = ['.', ',', '/', '\\', '\'', '(', ')', '’', '-']

    def __init__(self, typographies_in_raw=1, typographies_in_word=1, entity_words_unmatched=1, common_words_unmatched=1, maximal_initialism=5, \
        remove_common_abbreviations=True, meaningless_characters=__MEANINGLESS_CHARACTERS):
        self.ELF = Elf.Elf()
        self.maximal_typographies_in_raw = typographies_in_raw
        self.maximal_typographies_in_word = typographies_in_word
        self.maximal_entity_words_unmatched = entity_words_unmatched
        self.maximal_common_words_unmatched = common_words_unmatched
        self.maximal_initialism = maximal_initialism
        self.remove_common_abbreviations = remove_common_abbreviations
        self.meaningless_characters = meaningless_characters
        if '.' in meaningless_characters:
            copy = meaningless_characters[:]
            copy.remove('.')
            self.meaningless_characters_without_dot = copy
        else:
            self.meaningless_characters_without_dot = meaningless_characters
        self.transliterate = None
        self.and_words = ['and', 'und', 'et']
        self.abbreviations = { 'bros': 'brothers', 'dept': 'department', 'ets': 'establishments' }

    @staticmethod
    def default():
        return MatchingParameters()
