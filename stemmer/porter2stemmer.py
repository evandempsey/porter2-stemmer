#######################################################
# porter2stemmer.py: a Python implementation of the   #
# revised English stemming algorithm by Martin Porter #
#                                                     #
# Author: Evan Dempsey                                #
# Email: evandempsey@gmail.com                        #
# Last modified: 16/Jul/2012                          #
#                                                     #
# Usage:                                              #
# Import it, instantiate it, and pass                 #
# words as arguments to the stem method.              #
#                                                     #
# Example:                                            #
# from Porter2Stemmer import Porter2Stemmer           #
# stemmer = Porter2Stemmer()                          #
# print stemmer.stem('conspicuous')                   #
#######################################################

import sys
import re


class Porter2Stemmer(object):
    """Stem words according to the Porter2 stemming algorithm.
    A description of the algorithm can be found at
    http://snowball.tartarus.org/algorithms/english/stemmer.html"""

    vowels = ['a', 'e', 'i', 'o', 'u', 'y']
    doubles = ['bb', 'dd', 'ff', 'gg', 'mm', 'nn', 'pp', 'rr', 'tt']
    liEndings = ['c', 'd', 'e', 'g', 'h', 'k', 'm', 'n', 'r', 't']

    def stem(self, word):
        """Stem the word if it has more than two characters,
        otherwise return it as is"""

        if len(word) <= 2:
            return word
        else:
            word = self.removeInitialApostrophe(word)
            word = self.setYs(word)
            self.getRegions(word)

            word = self.zerothStep(word)
            word = self.firstStepA(word)
            word = self.firstStepB(word)
            word = self.firstStepC(word)
            word = self.secondStep(word)
            word = self.thirdStep(word)
            word = self.fourthStep(word)
            word = self.fifthStep(word)

            return word

    def removeInitialApostrophe(self, word):
        """Remove initial apostrophes from words"""
        if word[0] == "'":
            word = word[1:]

        return word

    def setYs(self, word):
        """Identify Ys that are to be treated
        as consonants and make them uppercase"""

        if word[0] == 'y':
            word = 'Y' + word[1:]

        for match in re.finditer("[aeiou]y", word):
            yIndex = match.end() - 1
            charList = [x for x in word]
            charList[yIndex] = 'Y'
            word = ''.join(charList)

        return word

    def getRegions(self, word):
        """Find regions R1 and R2"""
        self.r1 = sys.maxint
        self.r2 = sys.maxint

        length = len(word)

        for index, match in enumerate(re.finditer("[aeiouy][^aeiouy]", word)):
            if index == 0:
                if match.end() < length:
                    self.r1 = match.end()
            if index == 1:
                if match.end() < length:
                    self.r2 = match.end()
                break

    def isShort(self, word):
        """Determine if the word is short. Short words
        are ones that end in a short syllable and
        have an empty R1 region."""

        short = False
        length = len(word)

        if self.r1 >= length:
            if length > 2:
                ending = word[length - 3:]
                if re.match("[^aeiouy][aeiouy][^aeiouwxY]", ending):
                    short = True
            else:
                if re.match("[aeiouy][^aeiouy]", word):
                    short = True

        return short

    def zerothStep(self, word):
        """Get rid of apostrophes indicating possession"""

        if word.endswith("'s'"):
            return word[:-3]
        elif word.endswith("'s"):
            return word[:-2]
        elif word.endswith("'"):
            return word[:-1]
        else:
            return word

    def firstStepA(self, word):
        length = len(word)

        if word.endswith("sses"):
            return word[:-2]

        elif word.endswith("ied") or word.endswith("ies"):
            word = word[:-3]
            if len(word) == 1:
                word += 'ie'
            else:
                word += 'i'
            return word

        # This ensures that words like conspicous stem properly
        elif word.endswith('us') or word.endswith('ss'):
            return word

        # From spec: 'delete if the preceding word part contains a vowel
        # not immediately before the s (so gas and this retain the s,
        # gaps and kiwis lose it)
        elif word[length - 1] == 's':
            for letter in word[:-2]:
                if letter in self.vowels:
                    return word[:-1]

        return word

    def firstStepB(self, word):
        hasVowel = False

        if word.endswith('eed'):
            if len(word) >= self.r1:
                word = word[:-3] + 'ee'
            return word

        elif word.endswith('eedly'):
            if len(word) >= self.r1:
                word = word[:-5] + 'ee'
            return word

        elif word.endswith('ed'):
            for vowel in self.vowels:
                if vowel in word[:-2]:
                    hasVowel = True
                    word = word[:-2]
                    break

        elif word.endswith('edly'):
            for vowel in self.vowels:
                if vowel in word[:-4]:
                    hasVowel = True
                    word = word[:-4]
                    break

        elif word.endswith('ing'):
            for vowel in self.vowels:
                if vowel in word[:-3]:
                    hasVowel = True
                    word = word[:-3]
                    break

        elif word.endswith('ingly'):
            for vowel in self.vowels:
                if vowel in word[:-5]:
                    hasVowel = True
                    word = word[:-5]
                    break

        # Be sure to only perform one of these.
        if hasVowel:
            length = len(word)
            if word[length - 2:] in ['at', 'bl', 'iz']:
                word += 'e'
            elif word[length - 2:] in self.doubles:
                word = word[:-1]
            elif self.isShort(word):
                word += 'e'

        return word

    def firstStepC(self, word):
        """Replace y or Y with i if preceded by a non-vowel
        which is not the first letter of the word"""
        length = len(word)

        if word[length - 1] in 'Yy':
            if length > 2:
                if word[length - 2] not in self.vowels:
                    word = word[:-1] + 'i'

        return word

    def secondStep(self, word):
        """Perform replacements on common suffixes"""
        length = len(word)

        replacements = {'tional': 'tion', 'enci': 'ence', 'anci': 'ance',
                        'abli': 'able', 'entli': 'ent', 'ization': 'ize',
                        'izer': 'ize', 'ation': 'ate', 'ator': 'ate', 'alism': 'al',
                        'aliti': 'al', 'alli': 'al', 'fulness': 'ful',
                        'ousness': 'ous', 'ousli': 'ous', 'iveness': 'ive',
                        'iviti': 'ive', 'biliti': 'ble', 'bli': 'ble',
                        'fulli': 'ful', 'lessli': 'less'}

        for suffix in replacements.keys():
            if word.endswith(suffix):
                suffixLength = len(suffix)
                if self.r1 <= (length - suffixLength):
                    word = word[:-suffixLength] + replacements[suffix]

        if word.endswith('ogi'):
            if self.r1 <= (length - 3):
                if (length - 3) > 0:
                    if word[length - 4] == 'l':
                        word = word[:-3]

        if word.endswith('li'):
            if self.r1 <= (length - 2):
                if word[length - 3] in self.liEndings:
                    word = word[:-2]

        return word

    def thirdStep(self, word):
        """Perform replacements on common suffixes, part deux"""

        length = len(word)
        replacements = {'ational': 'ate', 'tional': 'tion', 'alize': 'al',
                        'icate': 'ic', 'iciti': 'ic', 'ical': 'ic',
                        'ful': '', 'ness': ''}

        for suffix in replacements.keys():
            if word.endswith(suffix):
                suffixLength = len(suffix)
                if self.r1 <= (length - suffixLength):
                    word = word[:-suffixLength] + replacements[suffix]

        if word.endswith('ative'):
            if self.r1 <= (length - 5) and self.r2 <= (length - 5):
                word = word[:-5]

        return word

    def fourthStep(self, word):
        """Delete some very common suffixes"""

        length = len(word)
        suffixes = ['al', 'ance', 'ence', 'er', 'ic', 'able', 'ible',
                    'ant', 'ement', 'ment', 'ent', 'ism', 'ate',
                    'iti', 'ous', 'ive', 'ize']

        for suffix in suffixes:
            if word.endswith(suffix) and self.r2 <= (length - len(suffix)):
                word = word[:-len(suffix)]
                return word

        if word.endswith('ion') and self.r2 <= (length - 3):
            if word[length - 4] in 'st':
                word = word[:-3]

        return word

    def fifthStep(self, word):
        """Deal with terminal Es and Ls and
        convert any uppercase Ys back to lowercase"""

        length = len(word)

        if word[length - 1] == 'e':
            if self.r2 <= (length - 1):
                word = word[:-1]

            elif self.r1 <= (length - 1):
                if not self.isShort(word[:-1]):
                    word = word[:-1]

        elif word[length - 1] == 'l':
            if self.r2 <= (length - 1) and word[length - 2] == 'l':
                word = word[:-1]

        charList = [x if x != 'Y' else 'y' for x in word]
        word = ''.join(charList)

        return word


def main():
    """If stemmer is being invoked from command line,
    perform tests based on the list of words and their stemmed
    counterparts in the porter2_stemmed.csv file provided"""

    print '*** Porter2Stemmer.py Tests ***'
    stemmer = Porter2Stemmer()

    try:
        testCases = open('porter2_stemmed.csv', 'r')
    except IOError:
        print 'Testing file could not be found. Exiting...'
        return

    for line in testCases:
        line = line.split(',')
        print line[0] + ' => ' + line[1].strip()
        assert stemmer.stem(line[0]) == line[1].strip()

    testCases.close()
    print 'All tests passed.'


if __name__ == '__main__':
    main()
