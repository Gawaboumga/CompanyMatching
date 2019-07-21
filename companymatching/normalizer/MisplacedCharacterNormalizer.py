from ..base import NormalizerMixin


class MisplacedCharacterNormalizer(NormalizerMixin):

    def normalize(self, lhs, rhs, original_lhs, original_rhs, **parameters):
        normalized_lhs = self.__normalize(lhs)
        normalized_rhs = self.__normalize(rhs)
        return normalized_lhs, normalized_rhs

    def __normalize(self, input_str):
        final = []
        tokens = input_str.split()
        for token in tokens:
            if '.' in token:
                parts = token.split('.')
                # If there are more than 2 dots, it's likely to be initials.
                if len(parts) == 2:
                    final.append(parts[0])
                    final.append(parts[1])
                else:
                    final.append(token.replace('.', ''))
            elif '&' in token and token != '&':
                parts = token.split('&')
                # If there are more than 2 parts, I don't know what it can be oO.
                if len(parts) == 2:
                    final.append(parts[0])
                    final.append('&')
                    final.append(parts[1])
                else:
                    final.append(token.replace('&', ''))
            else:
                final.append(token)
        return u' '.join(final)
