import sys
sys.path.append(r"C:/Users/YHUBAUT/Documents/GitHub/CompanyMatching")

from companymatching.DefaultMatching import DefaultMatching
from companymatching.MatchingType import MatchingType
from companymatching.MatchingParameters import MatchingParameters
import unittest


class TestElf(unittest.TestCase):

    def test_exact_match(self):
        name_matching = DefaultMatching()
        result = name_matching.match("exact", "exact")
        self.assertEqual(result.score, 100)
        self.assertEqual(result.kind, MatchingType.Exact)

    def test_typography(self):
        name_matching = DefaultMatching()
        result = name_matching.match("exact", "exbct")
        self.assertEqual(result.score, 90)
        self.assertEqual(result.kind, MatchingType.Typography)

    def test_unicode(self):
        name_matching = DefaultMatching()
        result = name_matching.match("ß", "ss")
        self.assertEqual(result.score, 100)
        self.assertEqual(result.kind, MatchingType.Exact)

        result = name_matching.match("elcua", "élçùà")
        self.assertEqual(result.score, 100)
        self.assertEqual(result.kind, MatchingType.Exact)
    
    def test_shorthand(self):
        name_matching = DefaultMatching()
        result = name_matching.match("polop", "polop SA")
        self.assertEqual(result.score, 100)
        self.assertEqual(result.kind, MatchingType.Additional | MatchingType.Exact)

    def test_initials_with_dots(self):
        name_matching = DefaultMatching()
        result = name_matching.match("T.E.S.T.", "TEST")
        self.assertEqual(result.score, 100)
        self.assertEqual(result.kind, MatchingType.Exact)

    def test_entity_abbreviations(self):
        name_matching = DefaultMatching()
        result = name_matching.match("test co. ltd.", "test corporation limited")
        self.assertEqual(result.score, 100)
        self.assertEqual(result.kind, MatchingType.Exact | MatchingType.Shorthand)

    def test_no_match_abbreviation(self):
        name_matching = DefaultMatching()
        result = name_matching.match("polop coop", "polop SA")
        self.assertEqual(result.score, 0)
        self.assertEqual(result.kind, MatchingType.NoMatch)

    def test_specifity_national(self):
        name_matching = DefaultMatching()
        result = name_matching.match("polop NV", "polop SA")
        self.assertEqual(result.score, 100)
        self.assertEqual(result.kind, MatchingType.Exact | MatchingType.Synonym)

    def test_abbreviation(self):
        name_matching = DefaultMatching()
        result = name_matching.match("TMC", "Test Matching Company SA")
        self.assertEqual(result.score, 100)
        self.assertEqual(result.kind, MatchingType.Additional | MatchingType.Exact | MatchingType.Initials)

        result = name_matching.match("TMC group", "Test Matching Company -Group")
        self.assertEqual(result.score, 100)
        self.assertEqual(result.kind, MatchingType.Exact | MatchingType.Initials)

    def test_ampersand(self):
        name_matching = DefaultMatching()
        result = name_matching.match("Test & Matching", "test and matching")
        self.assertEqual(result.score, 100)
        self.assertEqual(result.kind, MatchingType.Exact)

    def test_entity_abbreviations_without_spaces(self):
        name_matching = DefaultMatching()
        result = name_matching.match("test co.ltd", "test corporation limited")
        self.assertEqual(result.score, 100)
        self.assertEqual(result.kind, MatchingType.Exact | MatchingType.Shorthand)

    def test_no_match_with_two_different_company_word(self):
        name_matching = DefaultMatching()
        result = name_matching.match("Test Europe Group", "Test Europe Corporation")
        self.assertEqual(result.score, 0)
        self.assertEqual(result.kind, MatchingType.NoMatch)

    def test_handle_private_equity_and_numbers(self):
        name_matching = DefaultMatching()
        result = name_matching.match("Test V Group", "Test IV Group")
        self.assertEqual(result.score, 96)
        self.assertEqual(result.kind, MatchingType.Typography)

        result = name_matching.match("Test 3 Group", "Test 5 Group")
        self.assertEqual(result.score, 95)
        self.assertEqual(result.kind, MatchingType.Typography)

    def test_transcription(self):
        parameters = MatchingParameters.default()
        parameters.transliterate = fake_transliterate
        name_matching = DefaultMatching(parameters)
        result = name_matching.match("Еднолично акционерно дружество седмица", "sedmitsa EAD")
        self.assertEqual(result.score, 100)
        self.assertEqual(result.kind, MatchingType.Exact | MatchingType.Shorthand | MatchingType.Transliteration)

    def test_specify_parameters(self):
        name_matching = DefaultMatching()
        result = name_matching.match("test", "tast")
        self.assertEqual(result.score, 87)
        self.assertEqual(result.kind, MatchingType.Typography)

        result = name_matching.match("test", "pard", maximal_typographies_in_raw=4)
        self.assertEqual(result.score, 50)
        self.assertEqual(result.kind, MatchingType.Typography)

    def test_handle_misplaced_and(self):
        name_matching = DefaultMatching()
        result = name_matching.match("T&M", "T & M")
        self.assertEqual(result.score, 100)
        self.assertEqual(result.kind, MatchingType.Exact)

    def test_handle_common_word_abbreviation(self):
        name_matching = DefaultMatching()
        result = name_matching.match("ets.", "establishments")
        self.assertEqual(result.score, 100)
        self.assertEqual(result.kind, MatchingType.Exact | MatchingType.Abbreviation)


def fake_transliterate(token):
    if token == "седмица":
        return "sedmitsa"
    elif token == "ead":
        return "ead"
    elif token == "sedmitsa":
        return "sedmitsa"
    
    assert False

if __name__ == '__main__':
    unittest.main()
