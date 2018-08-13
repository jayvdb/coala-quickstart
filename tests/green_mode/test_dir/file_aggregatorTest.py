import os
import unittest

from copy import deepcopy
from os.path import join
from unittest.mock import patch

from coala_quickstart.green_mode.file_aggregator import (
    aggregate_files)


class Test_file_aggregators(unittest.TestCase):
    def test_aggregate_files(self):
        files = [
            'main.py', 'another_main.py',
            join('src', 'a.py'), join('src', 'b.py'),
            join('src', 'a', 'c.py'), join('src', 'a', 'd.py'),
            join('src', 'b', 'x.py'),
            join('test', 'y.py'), join('test', 'p', 'z.py'),
        ]
        return_val = (
            'main.py', 'another_main.py',
            join('src', 'a.py'), join('src', 'b.py'),
            join('src', 'a', 'c.py'), join('src', 'a', 'd.py'),
            join('src', 'b', 'x.py'), join('src', 'b', 't.py'),
            join('test', 'y.py'), join('test', 'p', 'z.py'),
        )
        project_dir_ = os.sep + 'some_dir' + os.sep
        new_files = []
        for i in files:
            new_files.append(project_dir_ + i)
        files = new_files

        new_return_val = ()
        for i in return_val:
            new_return_val += (project_dir_ + i,)
        return_val = new_return_val

        with patch('os.walk') as mockwalk:
            mockwalk.return_value = [
                ('', (), return_val), ]
            files_ret, ignore = aggregate_files(deepcopy(files), 'some_dir')
            self.assertEqual(files_ret, [os.sep + 'some_dir' + os.sep + '**'])
            self.assertEqual(
                ignore, [os.sep + join('some_dir', 'src', 'b', 't.py')])

        return_val = (
            'main.py', 'another_main.py', 'some.c',
            join('src', 'a.py'), join('src', 'b.py'), join(
                'src', 'omg.c'), join('src', 'gsoc.c'),
            join('src', 'a', 'c.py'), join('src', 'a', 'd.py'),
            join('src', 'b', 'x.py'), join('src', 'b', 't.py'), join(
                'src', 'b', 'x.c'), join('src', 'b', 'y.c'),
            join('test', 'y.py'), join('test', 's.c'),
            join('test', 'badass.c'),
            join('test', 'p', 'z.py'), join(
                'test', 'p', 'zx.c'), join('test', 'p', 'xz.c'),
        )

        new_return_val = ()
        for i in return_val:
            new_return_val += (project_dir_ + i,)
        return_val = new_return_val

        with patch('os.walk') as mockwalk:
            mockwalk.return_value = [
                ('', (), return_val), ]
            files_ret, ignore = aggregate_files(deepcopy(files), 'some_dir')
            self.assertEqual(files_ret, [os.sep + 'some_dir' + os.sep +
                                         '**.py'])
            self.assertEqual(ignore, [os.sep + os.path.join(
                'some_dir', 'src', 'b', 't.py')])

        return_val = (
            'main.py', 'another_main.py', 'some.c', 'README.md',
            join('src', 'a.py'), join('src', 'b.py'), join(
                'src', 'omg.c'), join('src', 'gsoc.c'),
            join('src', 'a', 'c.py'), join('src', 'a', 'd.py'),
            join('src', 'b', 'x.py'), join('src', 'b', 't.py'), join(
                'src', 'b', 'x.c'), join('src', 'b', 'y.c'),
            join('test', 'y.py'), join('test', 's.c'),
            join('test', 'badass.c'),
            join('test', 'p', 'z.py'), join(
                'test', 'p', 'zx.c'), join('test', 'p', 'xz.c'),
        )

        new_return_val = ()
        for i in return_val:
            new_return_val += (project_dir_ + i,)
        return_val = new_return_val

        with patch('os.walk') as mockwalk:
            mockwalk.return_value = [
                ('', (), return_val), ]
            files_ret, ignore = aggregate_files(deepcopy(files), 'some_dir')
            self.assertEqual(files_ret, [os.sep + os.path.join(
                'some_dir', '**.py')])
            self.assertEqual(ignore, [os.sep + os.path.join(
                'some_dir', 'src', 'b', 't.py')])

        return_val = (
            'main.py', 'another_main.py', 'some.c', 'README.md',
            join('src', 'a.py'), join('src', 'b.py'), join(
                'src', 'omg.c'), join('src', 'gsoc.c'),
            join('src', 'x.py'), join('src', 'y.py'), join(
                'src', 'temp.py'), join('src', 'h.py'), join('src', 'u.py'),
            join('src', 'a', 'c.py'), join('src', 'a', 'd.py'), join(
                'src', 'a', 'l.py'), join('src', 'a', 'v.py'),
            join('src', 'b', 'x.py'), join('src', 'b', 't.py'), join(
                'src', 'b', 'x.c'), join('src', 'b', 'y.c'),
            join('test', 'y.py'), join('test', 's.c'),
            join('test', 'badass.c'),
            join('test', 'p', 'z.py'), join(
                'test', 'p', 'zx.c'), join('test', 'p', 'xz.c'),
        )

        new_return_val = ()
        for i in return_val:
            new_return_val += (project_dir_ + i,)
        return_val = new_return_val

        with patch('os.walk') as mockwalk:
            mockwalk.side_effect = [
                [('', (), return_val), ],
                [('', (), (
                    os.sep + join('', 'some_dir', 'main.py'), os.sep +
                    join('', 'some_dir', 'another_main.py'),
                    os.sep + join('', 'some_dir', 'some.c'),
                    os.sep + join('', 'some_dir', 'README.md'))), ],
                [(os.sep + join('', 'some_dir', 'src', ''),
                  (),
                  (os.sep + join('', 'some_dir', 'src', 'a.py'),
                   os.sep + join('', 'some_dir', 'src', 'b.py'),
                   os.sep + join('', 'some_dir', 'src', 'omg.c'),
                   os.sep + join('', 'some_dir', 'src', 'gsoc.c'),
                   os.sep + join('', 'some_dir', 'src', 'x.py'),
                   os.sep + join('', 'some_dir', 'src', 'y.py'),
                   os.sep + join('', 'some_dir', 'src', 'temp.py'),
                   os.sep + join('', 'some_dir', 'src', 'h.py'),
                   os.sep + join('', 'some_dir', 'src', 'u.py'),
                   os.sep + join('', 'some_dir', 'src', 'a', 'c.py'),
                   os.sep + join('', 'some_dir', 'src', 'a', 'd.py'),
                   os.sep + join('', 'some_dir', 'src', 'a', 'l.py'),
                   os.sep + join('', 'some_dir', 'src', 'a', 'v.py'),
                   os.sep + join('', 'some_dir', 'src', 'b', 'x.py'),
                   os.sep + join('', 'some_dir', 'src', 'b', 't.py'),
                   os.sep + join('', 'some_dir', 'src', 'b', 'x.c'),
                   os.sep + join('', 'some_dir', 'src', 'b', 'y.c',)
                   )),
                 ],
                [(os.sep + join('', 'some_dir', 'src', ''),
                  (),
                  (os.sep + join('', 'some_dir', 'src', 'a.py'),
                   os.sep + join('', 'some_dir', 'src', 'b.py'),
                   os.sep + join('', 'some_dir', 'src', 'omg.c'),
                   os.sep + join('', 'some_dir', 'src', 'gsoc.c'),
                   os.sep + join('', 'some_dir', 'src', 'x.py'),
                   os.sep + join('', 'some_dir', 'src', 'y.py'),
                   os.sep + join('', 'some_dir', 'src', 'temp.py'),
                   os.sep + join('', 'some_dir', 'src', 'h.py'),
                   os.sep + join('', 'some_dir', 'src', 'u.py')
                   )),
                 ],
                [(os.sep + join('', 'some_dir', 'src', 'a', ''),
                  (),
                  (os.sep + join('', 'some_dir', 'src', 'a', 'c.py'),
                   os.sep + join('', 'some_dir', 'src', 'a', 'd.py'),
                   os.sep + join('', 'some_dir', 'src', 'a', 'l.py'),
                   os.sep + join('', 'some_dir', 'src', 'a', 'v.py')
                   )),
                 ],
                [(os.sep + join('', 'some_dir', 'test', ''),
                  (),
                  (os.sep + join('', 'some_dir', 'test', 'y.py'),
                   os.sep + join('', 'some_dir', 'test', 's.c'),
                   os.sep + join('', 'some_dir', 'test', 'badass.c'),
                   os.sep + join('', 'some_dir', 'test', 'p', 'z.py'),
                   os.sep + join('', 'some_dir', 'test', 'p', 'zx.c'),
                   os.sep + join('', 'some_dir', 'test', 'p', 'xz.c',)
                   ))
                 ], ]
            files_ret, ignore = aggregate_files(deepcopy(files), 'some_dir')
            self.assertEqual(
                files_ret,
                [os.sep + os.path.join('some_dir', '*'),
                 os.sep + os.path.join('some_dir', 'src', '*'),
                 os.sep + os.path.join('some_dir', 'src', 'a', '**'),
                 os.sep + os.path.join('some_dir', 'test', '**')]
            )
            self.assertCountEqual(
                list(set(ignore)),
                [os.sep + os.path.join('some_dir', 'some.c'),
                 os.sep + os.path.join('some_dir', 'README.md'),
                 os.sep + os.path.join('some_dir', 'src', 'omg.c'),
                 os.sep + os.path.join('some_dir', 'src', 'gsoc.c'),
                 os.sep + os.path.join('some_dir', 'src', 'x.py'),
                 os.sep + os.path.join('some_dir', 'src', 'y.py'),
                 os.sep + os.path.join('some_dir', 'src', 'temp.py'),
                 os.sep + os.path.join('some_dir', 'src', 'h.py'),
                 os.sep + os.path.join('some_dir', 'src', 'u.py'),
                 os.sep + os.path.join('some_dir', 'src', 'a', 'l.py'),
                 os.sep + os.path.join('some_dir', 'src', 'a', 'v.py'),
                 os.sep + os.path.join('some_dir', 'test', 's.c'),
                 os.sep + os.path.join('some_dir', 'test', 'badass.c'),
                 os.sep + os.path.join('some_dir', 'test', 'p', 'zx.c'),
                 os.sep + os.path.join('some_dir', 'test', 'p', 'xz.c')]
            )
