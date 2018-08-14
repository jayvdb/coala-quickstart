import inspect
import itertools
import types
import unittest

from tempfile import NamedTemporaryFile

from tests.test_bears.AllKindsOfSettingsDependentBear import (
    AllKindsOfSettingsDependentBear)
from coala_quickstart.generation.Utilities import (
    contained_in,
    get_default_args, get_all_args,
    search_for_orig, concatenate, peek,
    get_hashbang,
    get_language_from_hashbang)
from coalib.results.SourcePosition import SourcePosition
from coalib.results.SourceRange import SourceRange


def foo():
    pass


def foo_bar(n):
    def bar():
        return n+1
    return bar


class TestAdditionalFunctions(unittest.TestCase):

    def second(func):
        def wrapper():
            return func()
        return wrapper

    def first():
        pass

    third = second(first)
    fourth = second(second(first))

    def test_search_for_orig(self):
        self.assertEqual(types.MethodType(search_for_orig(self.third, 'first'),
                                          self), self.first)
        self.assertEqual(types.MethodType(search_for_orig(self.fourth,
                                                          'first'),
                                          self), self.first)
        self.assertEqual(search_for_orig(self.first, 'first'), None)
        self.assertEqual(search_for_orig(self.first, "bar"), None)
        self.assertEqual(search_for_orig(self.first, "first"), None)
        # function without closure
        self.assertEqual(search_for_orig(foo, "bar"), None)
        self.assertEqual(search_for_orig(foo, "foo"), None)
        func = foo_bar(3)
        x = func()  # function with closure
        self.assertEqual(search_for_orig(func, "bar"), None)

    def test_get_default_args(self):
        self.assertEqual(get_default_args(AllKindsOfSettingsDependentBear.run),
                         {'chars': False,
                          'dependency_results': {},
                          'max_line_lengths': 1000,
                          'no_chars': 79,
                          'use_spaces': None,
                          'use_tabs': False})

    def test_get_all_args(self):
        empty = inspect._empty
        self.assertEqual(get_all_args(AllKindsOfSettingsDependentBear.run),
                         {'self': empty, 'file': empty, 'filename': empty,
                          'configs': empty,
                          'use_bears': empty, 'no_lines': empty,
                          'use_spaces': None,
                          'use_tabs': False, 'max_line_lengths': 1000,
                          'no_chars': 79,
                          'chars': False, 'dependency_results': {}})


class TestHashbag(unittest.TestCase):

    def test_missing_file(self):
        self.assertIsNone(get_hashbang('does_not_exist'))

    def test_with_bash(self):
        with NamedTemporaryFile(mode='w+t', delete=False) as temp_file:
            temp_file.write('#!bin/bash\n')
            temp_file.close()
            self.assertEqual(get_hashbang(temp_file.name), '#!bin/bash')

    def test_no_eol(self):
        with NamedTemporaryFile(mode='w+t', delete=False) as temp_file:
            temp_file.write('#!bin/bash')
            temp_file.close()
            self.assertEqual(get_hashbang(temp_file.name), '#!bin/bash')

    def test_with_slash(self):
        with NamedTemporaryFile(mode='w+t', delete=False) as temp_file:
            temp_file.write('#!/bin/bash\n')
            temp_file.close()
            self.assertEqual(get_hashbang(temp_file.name), '#!/bin/bash')

    def test_with_space(self):
        with NamedTemporaryFile(mode='w+t', delete=False) as temp_file:
            temp_file.write('#!/bin/bash \n')
            temp_file.close()
            self.assertEqual(get_hashbang(temp_file.name), '#!/bin/bash')

    def test_env(self):
        with NamedTemporaryFile(mode='w+t', delete=False) as temp_file:
            temp_file.write('#!/bin/env bash\n')
            temp_file.close()
            self.assertEqual(get_hashbang(temp_file.name), '#!/bin/env bash')

    def test_non_unicode_file(self):
        with NamedTemporaryFile(mode='w+b', delete=False) as temp_file:
            temp_file.write(b'\2000x80')
            temp_file.close()
            self.assertIsNone(get_hashbang(temp_file.name))

    def test_empty_file(self):
        with NamedTemporaryFile(mode='w+t', delete=False) as temp_file:
            temp_file.write('\n')
            temp_file.close()
            self.assertIsNone(get_hashbang(temp_file.name))

    def test_no_bang(self):
        with NamedTemporaryFile(mode='w+t', delete=False) as temp_file:
            temp_file.write('#bin/bash')
            temp_file.close()
            self.assertIsNone(get_hashbang(temp_file.name))

    def test_no_hash(self):
        with NamedTemporaryFile(mode='w+t', delete=False) as temp_file:
            temp_file.write('!bin/bash')
            temp_file.close()
            self.assertIsNone(get_hashbang(temp_file.name))

    def test_get_language_from_hashbang(self):
        self.assertEqual(get_language_from_hashbang('#!/usr/bin/env python'),
                         'python')
        self.assertEqual(get_language_from_hashbang('#!bin/bash'),
                         'bash')


class TestDataStructuresOperationsFunctions(unittest.TestCase):

    def test_concatenate(self):
        dict1 = {'1': {'a', 'b', 'c'},
                 '2': {'d', 'e', 'f'},
                 '3': {'g', 'h', 'i'}}
        dict2 = {'4': {'j', 'k', 'l'},
                 '2': {'m', 'n', 'o'},
                 '5': {'p', 'q', 'r'}}
        result_dict = {'1': {'a', 'b', 'c'},
                       '2': {'d', 'e', 'f', 'm', 'n', 'o'},
                       '3': {'g', 'h', 'i'},
                       '4': {'j', 'k', 'l'},
                       '5': {'p', 'q', 'r'}}
        ret_val = concatenate(dict1, dict2)
        self.assertEqual(ret_val, result_dict)

    def test_peek(self):

        def give_gen():
            for i in range(1, 5):
                yield i

        def give_empty_gen():
            for i in range(1, 1):
                yield i

        obj = give_gen()

        for i in range(1, 5):
            num, new_obj = peek(obj)
            obj, new_obj = itertools.tee(obj)
            self.assertEqual(i, num)

        ret_val = peek(obj)
        obj = give_empty_gen()
        ret_val_1 = peek(obj)

        self.assertEqual(ret_val, None)
        self.assertEqual(ret_val_1, None)


class TestContainedIn(unittest.TestCase):

    def test_contained_in_1(self):
        start = SourcePosition('a.py', line=1, column=5)
        end = SourcePosition('a.py', line=5, column=1)
        smaller = SourceRange(start, end)

        start = SourcePosition('a.py', line=1, column=5)
        end = SourcePosition('a.py', line=5, column=2)
        bigger = SourceRange(start, end)
        self.assertTrue(contained_in(smaller, bigger))

        start = SourcePosition('a.py', line=1, column=4)
        end = SourcePosition('a.py', line=5, column=1)
        bigger = SourceRange(start, end)
        self.assertTrue(contained_in(smaller, bigger))

        start = SourcePosition('a.py', line=1, column=5)
        end = SourcePosition('a.py', line=5, column=1)
        bigger = SourceRange(start, end)
        self.assertTrue(contained_in(smaller, bigger))

    def test_contained_in_2(self):
        start = SourcePosition('a.py', line=1, column=5)
        end = SourcePosition('a.py', line=5, column=1)
        smaller = SourceRange(start, end)

        start = SourcePosition('a.py', line=1, column=9)
        end = SourcePosition('a.py', line=5, column=1)
        bigger = SourceRange(start, end)
        self.assertFalse(contained_in(smaller, bigger))

        start = SourcePosition('a.py', line=1, column=6)
        end = SourcePosition('a.py', line=4, column=2)
        bigger = SourceRange(start, end)
        self.assertFalse(contained_in(smaller, bigger))

        start = SourcePosition('b.py', line=1, column=5)
        end = SourcePosition('b.py', line=5, column=1)
        bigger = SourceRange(start, end)
        self.assertFalse(contained_in(smaller, bigger))

    def test_contained_in_3(self):
        start = SourcePosition('a.py', line=1, column=5)
        end = SourcePosition('a.py', line=5, column=1)
        smaller = SourceRange(start, end)

        start = SourcePosition('a.py', line=2, column=5)
        end = SourcePosition('a.py', line=5, column=1)
        bigger = SourceRange(start, end)
        self.assertFalse(contained_in(smaller, bigger))

    def test_contained_in_4(self):
        start = SourcePosition('a.py', line=3, column=5)
        end = SourcePosition('a.py', line=5, column=1)
        smaller = SourceRange(start, end)

        start = SourcePosition('a.py', line=1, column=5)
        end = SourcePosition('a.py', line=6, column=1)
        bigger = SourceRange(start, end)
        self.assertTrue(contained_in(smaller, bigger))

        start = SourcePosition('a.py', line=3, column=5)
        end = SourcePosition('a.py', line=6, column=1)
        bigger = SourceRange(start, end)
        self.assertTrue(contained_in(smaller, bigger))

    def test_contained_in_5(self):
        start = SourcePosition('a.py', line=3, column=5)
        end = SourcePosition('a.py', line=5, column=1)
        smaller = SourceRange(start, end)

        start = SourcePosition('a.py', line=2, column=5)
        end = SourcePosition('a.py', line=5, column=1)
        bigger = SourceRange(start, end)
        self.assertTrue(contained_in(smaller, bigger))

        start = SourcePosition('a.py', line=3, column=8)
        end = SourcePosition('a.py', line=7, column=1)
        bigger = SourceRange(start, end)
        self.assertFalse(contained_in(smaller, bigger))

    def test_contained_in_6(self):
        start = SourcePosition('a.py', line=3, column=5)
        end = SourcePosition('a.py', line=5, column=7)
        smaller = SourceRange(start, end)

        start = SourcePosition('a.py', line=3, column=5)
        end = SourcePosition('a.py', line=5, column=6)
        bigger = SourceRange(start, end)
        self.assertFalse(contained_in(smaller, bigger))

        start = SourcePosition('a.py', line=2, column=8)
        end = SourcePosition('a.py', line=5, column=1)
        bigger = SourceRange(start, end)
        self.assertFalse(contained_in(smaller, bigger))

        start = SourcePosition('a.py', line=2, column=None)
        end = SourcePosition('a.py', line=5, column=1)
        bigger = SourceRange(start, end)
        self.assertFalse(contained_in(smaller, bigger))
