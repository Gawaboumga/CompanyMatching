from enum import IntEnum
import csv
import os


class ElfType(IntEnum):
    Abbreviation = 0,
    LocalName = 1,
    TransliteratedAbbreviation = 2,
    TransliteratedLocalName = 3,
    Unknown = 5,


class Elf:
    def __init__(self):
        file_path = os.path.join(os.path.dirname(__file__), 'elf_company.csv')
        self.__elf_database = self.__read_from_csv(file_path)

    def get(self, elf_type, token, country='AA'):
        country_mapping = self.__elf_database[country]
        if country_mapping[elf_type] is None:
            return None
        else:
            return country_mapping[elf_type].get(token)

    def __read_from_csv(self, file_path):
        elf_database = {}
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"', strict=True)
            for tokens in spamreader:

                country = tokens[0]
                elf_type = ElfType(int(tokens[1]))
                word = tokens[2]
                elfs = set(tokens[3].split(';'))

                country_mapping = elf_database.get(country, None)
                if country_mapping is None:
                    word_mapping = {}
                    word_mapping[word] = elfs
                    country_mapping = [None for _ in range(4)]
                    country_mapping[elf_type] = word_mapping
                else:
                    word_mapping = country_mapping[elf_type]
                    if word_mapping is not None:
                        word_mapping[word] = elfs
                    else:
                        word_mapping = { word: elfs }
                    country_mapping[elf_type] = word_mapping

                elf_database[country] = country_mapping
        return elf_database
