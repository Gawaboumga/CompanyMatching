from ..base import NormalizerMixin


class CharacterNormalizer(NormalizerMixin):

    def __init__(self, meaningless_characters):
        super()
        self.meaningless_characters = meaningless_characters

    def normalize(self, lhs, rhs, original_lhs, original_rhs, **parameters):
        normalized_lhs = self.__normalize(lhs)
        normalized_rhs = self.__normalize(rhs)
        return normalized_lhs, normalized_rhs

    def __normalize(self, input_str, **parameters):
        without_dot = parameters.get("meaningless_characters", self.meaningless_characters)
        return self.__remove(input_str, without_dot)


    def __remove(self, input_str, characters):
        for character in characters:
            input_str = input_str.replace(character, '')

        return input_str
