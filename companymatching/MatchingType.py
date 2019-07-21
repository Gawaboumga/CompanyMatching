from enum import IntFlag


class MatchingType(IntFlag):
    Abbreviation = 1 << 0
    Additional = 1 << 1
    Exact = 1 << 2
    Initials = 1 << 3
    Shorthand = 1 << 4
    Synonym = 1 << 5
    Translation = 1 << 6
    Transliteration = 1 << 7
    Typography = 1 << 8
    NoMatch = 0
