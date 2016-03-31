#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_porter2stemmer
----------------------------------

Tests for `porter2stemmer` module.
"""
import unittest
from porter2stemmer import Porter2Stemmer


class TestPorter2stemmer(unittest.TestCase):

    def setUp(self):
        pass

    def test_stem(self):
        stemmer = Porter2Stemmer()

        with open('tests/porter2_stemmed.csv') as test_cases:
            for line in test_cases:
                orig, stemmed = line.strip().split(',')
                self.assertEqual(stemmer.stem(orig), stemmed)

        test_cases.close()

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
