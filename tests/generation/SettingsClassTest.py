import unittest

from pyprint.ConsolePrinter import ConsolePrinter
from coala_quickstart.generation.SettingsClass import (
    collect_bear_settings, SettingTypes)
from tests.test_bears.AllKindsOfSettingsDependentBear import (
    AllKindsOfSettingsDependentBear)
from tests.test_bears.AllKindsOfSettingsDependentDecoratedBear import (
    AllKindsOfSettingsDependentDecoratedBear)
from tests.test_bears.AllKindsOfSettingsBaseBear import (
    AllKindsOfSettingsBaseBear)
from tests.test_bears.LinterBearWithCreateArguments import (
    LinterBearWithCreateArguments)
from tests.test_bears.SomeLinterBear import SomeLinterBear
from tests.test_bears.LinterBearWithParameters import LinterBearWithParameters
from tests.test_bears.BearA import BearA


class TestSettingsClass(unittest.TestCase):

    def setUp(self):
        self.printer = ConsolePrinter()
        self.log_printer = None

    def test_collect_bear_settings(self):
        relevant_bears = {'test':
                          {AllKindsOfSettingsDependentBear,
                           AllKindsOfSettingsDependentDecoratedBear,
                           AllKindsOfSettingsBaseBear,
                           BearA, SomeLinterBear, LinterBearWithCreateArguments,
                           LinterBearWithParameters}}

        bear_settings_obj = collect_bear_settings(relevant_bears)

        # The following test is for testing out the sorting of settings
        # into Type bool and other Types using the test bear
        # AllKindsOfSettingsDependentBear. This bear has all kinds of
        # possible setting types and is dependent on another similar
        # kind of bear so that the non-optional settings from the
        # base bear also show up here.

        k = 0
        for index, i in enumerate(bear_settings_obj):
            if i.bear == AllKindsOfSettingsDependentBear:
                k = index
                break
        obj = bear_settings_obj[k].non_optional_settings
        self.assertCountEqual(obj.settings_bool, ['use_bear', 'use_bears'])
        self.assertCountEqual(obj.settings_others, ['config',
                                                    'max_line_lengths',
                                                    'no_line', 'configs',
                                                    'no_lines'])
        obj = bear_settings_obj[k].optional_settings
        self.assertCountEqual(obj.settings_bool, ['use_spaces', 'use_tabs',
                                                  'chars', 'use_space',
                                                  'use_tab'])
        self.assertCountEqual(obj.settings_others, ['max_line_lengths',
                                                    'no_chars',
                                                    'dependency_results',
                                                    'dependency_result',
                                                    'no_char',
                                                    'max_line_length'])

        # The following test is for testing out the sorting of settings
        # into Type bool and other Types using the test bear
        # AllKindsOfSettingsDependentDecoratedBear. This bear has all kinds of
        # possible setting types and is dependent on another similar
        # kind of bear so that the non-optional settings from the
        # base bear also show up here. Moreover the run methods of both these
        # bears are decorated to test out whether the code is able to extract
        # out the original function from the decorated methods and provide
        # us with the correct bear settings.

        for index, i in enumerate(bear_settings_obj):
            if i.bear == AllKindsOfSettingsDependentDecoratedBear:
                k = index
                break
        obj = bear_settings_obj[k].non_optional_settings
        self.assertCountEqual(obj.settings_bool, ['use_bear', 'use_bears'])
        self.assertCountEqual(obj.settings_others, ['config',
                                                    'max_line_lengths',
                                                    'no_line',
                                                    'configs',
                                                    'no_lines'])
        obj = bear_settings_obj[k].optional_settings
        self.assertCountEqual(obj.settings_bool, ['use_spaces', 'use_tabs',
                                                  'chars', 'use_space',
                                                  'use_tab'])
        self.assertCountEqual(obj.settings_others, ['max_line_lengths',
                                                    'no_chars',
                                                    'dependency_results',
                                                    'dependency_result',
                                                    'no_char',
                                                    'max_line_length'])

        # The following test is for testing out the sorting of settings
        # into Type bool and other Types using the test bear
        # AllKindsOfSettingsBaseBear. This bear has all kinds of
        # possible setting types.

        for index, i in enumerate(bear_settings_obj):
            if i.bear == AllKindsOfSettingsBaseBear:
                k = index
                break
        obj = bear_settings_obj[k].non_optional_settings
        self.assertCountEqual(obj.settings_bool, ['use_bear'])
        self.assertCountEqual(obj.settings_others, ['config',
                                                    'max_line_lengths',
                                                    'no_line'])
        obj = bear_settings_obj[k].optional_settings
        self.assertCountEqual(obj.settings_bool, ['use_space', 'use_tab'])
        self.assertCountEqual(obj.settings_others, ['max_line_length',
                                                    'no_char',
                                                    'dependency_result'])

        # The following test is for testing out the sorting of settings
        # into Type bool and other Types using the test bear
        # BearA. This bear is dependent on BearB which is further dependent
        # on BearC to test out that settings from BearC
        # are appearing over here and the parsing of the bear dependency
        # tree is done right.

        for index, i in enumerate(bear_settings_obj):
            if i.bear == BearA:
                k = index
                break
        obj = bear_settings_obj[k].non_optional_settings
        self.assertCountEqual(obj.settings_bool, ['use_spaces'])
        self.assertCountEqual(obj.settings_others, [])
        obj = bear_settings_obj[k].optional_settings
        self.assertCountEqual(obj.settings_bool, [])
        self.assertCountEqual(obj.settings_others, ['a'])

        # The following tests are for testing out the sorting of settings
        # into Type bool and other Types using the test bears
        # SomeLinterBear and LinterBearWithParameters. These tests ensure that
        # the method create_arguments() is parsed correctly for its settings
        # for linter bears.

        for index, i in enumerate(bear_settings_obj):
            if i.bear == SomeLinterBear:
                k = index
                break
        obj = bear_settings_obj[k].non_optional_settings
        self.assertCountEqual(obj.settings_bool, [])
        self.assertCountEqual(obj.settings_others, [])
        obj = bear_settings_obj[k].optional_settings
        self.assertCountEqual(obj.settings_bool, [])
        self.assertCountEqual(obj.settings_others, [])

        # LinterBearWithParameters is also added because SomeLinterBear did not
        # have any valid output to test against.

        for index, i in enumerate(bear_settings_obj):
            if i.bear == LinterBearWithParameters:
                k = index
                break
        obj = bear_settings_obj[k].non_optional_settings
        self.assertCountEqual(obj.settings_bool, [])
        self.assertCountEqual(obj.settings_others, ['nonopsetting'])
        obj = bear_settings_obj[k].optional_settings
        self.assertCountEqual(obj.settings_bool, ['someoptionalsetting'])
        self.assertCountEqual(obj.settings_others, [])

        # The following test is for testing out the sorting of settings
        # into Type bool and other Types using the test bear
        # LinterBearWithCreateArguments. This test is added primarily to
        # check that the settings from create_arguments() as well as
        # generate_config() are populated inside the classes
        # (to store metadata) for which
        # the test is being written, for linter bears.

        for index, i in enumerate(bear_settings_obj):
            if i.bear == LinterBearWithCreateArguments:
                k = index
                break
        obj = bear_settings_obj[k].non_optional_settings
        self.assertCountEqual(obj.settings_bool, ['yes'])
        self.assertCountEqual(obj.settings_others, ['nonopsetting', 'rick'])
        obj = bear_settings_obj[k].optional_settings
        self.assertCountEqual(obj.settings_bool, ['someoptionalsetting'])
        self.assertCountEqual(obj.settings_others, ['makman2'])

    def test_invalid_trigger(self):
        with self.assertRaises(ValueError, msg='Invalid trigger Type'):
            SettingTypes({'a': bool}, None, None, 'wubalubadubdub')
