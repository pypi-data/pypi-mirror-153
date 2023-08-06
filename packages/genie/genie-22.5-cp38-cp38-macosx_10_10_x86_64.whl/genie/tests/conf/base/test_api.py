import os
import sys
import importlib
import unittest
import weakref
from unittest import mock

from genie.libs.clean import BaseStage
from genie.conf.base.device import Device
from genie.conf.base.api import ExtendApis, CleanAPI
from genie.tests.conf.base.mock_errored_api_data import data_loader
from genie.json.exceptions import ApiImportError

from pyats.aetest.steps import Steps


class TestApi(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice', os='iosxe',
                             custom={'abstraction': {'order':['os']}})

    def test_api_success(self):
        api = self.device.api.get_api('shut_interface', self.device)
        self.assertEqual(callable(api), True)
        self.assertEqual(api.__name__, 'shut_interface')

    def test_api_exception(self):
        with self.assertRaises(AttributeError):
            self.device.api.get_api('DontExists', self.device)

    @mock.patch('genie.conf.base.api._load_function_json', return_value=data_loader())
    def test_api_recall_error(self, mock_data):

        with self.assertRaises(NameError):
            importlib.reload(genie.libs.sdk.apis)
            self.device.api.get_api('clear_interface_counters', self.device)


class TestExtendApi(unittest.TestCase):

    def setUp(self):
        sys.path.append(os.path.dirname(__file__))

    def test_extend_api(self):
        ext = ExtendApis('dummy_api')
        ext.extend()
        summary = ext.output['extend_info']

        self.assertEqual(len(summary), 2)
        self.assertIn("api name: 'dummy_iosxe', tokens ['iosxe'], "
                      "module name: utils",
                      summary)
        self.assertIn("api name: 'dummy_common', tokens ['com'], "
                      "module name: utils",
                      summary)

    def test_extend_api_module_error(self):
        ext = ExtendApis('dummy_api_error')
        with self.assertRaises(ApiImportError):
            ext.extend()


class TestCleanAPI(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice', os='iosxe',
            custom={'abstraction': {'order': ['os']}})

    def test_attributes(self):
        self.assertIsInstance(self.device.api.clean, CleanAPI)
        self.assertEqual(self.device.api.clean.device, weakref.ref(self.device))
        self.assertTrue(isinstance(self.device.api.clean.history, dict))

    @mock.patch('genie.libs.clean.utils.load_clean_json')
    def test_retrieve_existing_stage(self, clean_json):
        clean_json.return_value = {
            "ExistsStage": {
                "iosxe": {
                      "package": "genie.libs.clean",
                      "module_name": "stages.stages",
                      "uid": "ExistsStage",
                }
            }
        }

        class ExistsStage(BaseStage):
            pass

        with mock.patch('genie.libs.clean.stages.stages.ExistsStage', ExistsStage, create=True):

            # Make sure the returned class is instantiated and its the expected class
            self.assertIsInstance(self.device.api.clean.ExistsStage, ExistsStage)
            self.assertEqual(self.device.api.clean.ExistsStage, ExistsStage())

            # Make sure the stage has mandatory parameters setup
            self.assertEqual(self.device.api.clean.ExistsStage.parameters['device'], self.device)
            self.assertIsInstance(self.device.api.clean.ExistsStage.parameters['steps'], Steps)

    @mock.patch('genie.libs.clean.utils.load_clean_json')
    def test_retrieve_non_existent_stage(self, clean_json):
        clean_json.return_value = {
            "DoesntExistStage": {
                "iosxe": {
                      "package": "genie.libs.clean",
                      "module_name": "stages.stages",
                      "uid": "DoesntExistStage",
                }
            }
        }

        with self.assertRaises(Exception) as cm:
            self.device.api.clean.DefinitelyDoesntExistStage

        self.assertIn(
            "The clean stage 'DefinitelyDoesntExistStage' does not exist in the json file",
            str(cm.exception)
        )

        with self.assertRaises(Exception) as cm:
            self.device.api.clean.DoesntExistStage

        self.assertIn(
            "The clean stage 'DoesntExistStage' does not exist under the following abstraction tokens",
            str(cm.exception)
        )

    @mock.patch('genie.libs.clean.utils.load_clean_json')
    def test_dir(self, clean_json):
        before = dir(self.device.api.clean)

        clean_json.return_value = {
            "ExistsStage": {
                "iosxe": {
                      "package": "genie.libs.clean",
                      "module_name": "stages.stages",
                      "uid": "ExistsStage",
                }
            },
            "SomeOtherOs": {
                "nxos": {
                      "package": "genie.libs.clean",
                      "module_name": "stages.stages",
                      "uid": "SomeOtherOs",
                }
            },
        }

        after = dir(self.device.api.clean)

        # nxos stages should not appear on an iosxe device
        self.assertEqual(self.device.os, 'iosxe')
        self.assertEqual(['ExistsStage'] + before, after)



if __name__ == '__main__':
    unittest.main()

