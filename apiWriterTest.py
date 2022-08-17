import unittest
from unittest import mock
from unittest.mock import call, mock_open

from apiWriter import Writer
from apiData import ApiItem


class ApiWriterTest(unittest.TestCase):

    @mock.patch('builtins.open', new_callable=mock_open())
    @mock.patch('apiWriter.os.makedirs')
    def test_update_api_data_channel(self, make_dir_mock, file_open_mock):
        api_items = [
            ApiItem('display', '', 'channel')
        ]

        Writer(api_items).update_api_data()

        make_dir_calls = [
            call('/Users/enrico/cybop/build/scripts/../../tools/api-generator/spec', exist_ok=True)
        ]
        make_dir_mock.assert_has_calls(make_dir_calls)

        file_open_mock.assert_any_call('/Users/enrico/cybop/build/scripts/../../doc/cybol/api/channel.txt', 'w')
        file_open_mock.assert_any_call('/Users/enrico/cybop/build/scripts/../../tools/api-generator/spec/channel.cybol', 'w')

        write_calls = [
            call('display'),
            call('<node>\n    <node name="display" channel="inline" format="text/plain" model="display"/>\n</node>')
        ]
        file_open_mock.return_value.__enter__().write.assert_has_calls(write_calls)

    @mock.patch('builtins.open', new_callable=mock_open())
    @mock.patch('apiWriter.os.makedirs')
    def test_update_api_data_encoding(self, make_dir_mock, file_open_mock):
        api_items = [
            ApiItem('utf-8', '', 'encoding')
        ]

        Writer(api_items).update_api_data()

        make_dir_calls = [
            call('/Users/enrico/cybop/build/scripts/../../tools/api-generator/spec', exist_ok=True)
        ]
        make_dir_mock.assert_has_calls(make_dir_calls)

        file_open_mock.assert_any_call('/Users/enrico/cybop/build/scripts/../../doc/cybol/api/encoding.txt', 'w')
        file_open_mock.assert_any_call('/Users/enrico/cybop/build/scripts/../../tools/api-generator/spec/encoding.cybol', 'w')

        write_calls = [
            call('utf-8'),
            call('<node>\n    <node name="utf-8" channel="inline" format="text/plain" model="utf-8"/>\n</node>')
        ]
        file_open_mock.return_value.__enter__().write.assert_has_calls(write_calls)

    @mock.patch('builtins.open', new_callable=mock_open())
    @mock.patch('apiWriter.os.makedirs')
    def test_update_api_data_encoding(self, make_dir_mock, file_open_mock):
        api_items = [
            ApiItem('utf-8', '', 'encoding')
        ]

        Writer(api_items).update_api_data()

        make_dir_calls = [
            call('/Users/enrico/cybop/build/scripts/../../tools/api-generator/spec', exist_ok=True)
        ]
        make_dir_mock.assert_has_calls(make_dir_calls)

        file_open_mock.assert_any_call('/Users/enrico/cybop/build/scripts/../../doc/cybol/api/encoding.txt', 'w')
        file_open_mock.assert_any_call('/Users/enrico/cybop/build/scripts/../../tools/api-generator/spec/encoding.cybol', 'w')

        write_calls = [
            call('calculate/add'),
            call('<node>\n    <node name="utf-8" channel="inline" format="text/plain" model="utf-8"/>\n</node>')
        ]
        file_open_mock.return_value.__enter__().write.assert_has_calls(write_calls)

    @mock.patch('builtins.open', new_callable=mock_open())
    @mock.patch('apiWriter.os.makedirs')
    def test_update_api_data_logic_without_anything(self, make_dir_mock, file_open_mock):
        api_items = [
            ApiItem('calculate/add', 'This is the add method', 'logic')
        ]

        Writer(api_items).update_api_data()

        make_dir_calls = [
            call('/Users/enrico/cybop/build/scripts/../../tools/api-generator/spec', exist_ok=True)
        ]
        make_dir_mock.assert_has_calls(make_dir_calls)

        file_open_mock.assert_any_call('/Users/enrico/cybop/build/scripts/../../doc/cybol/api/logic.txt', 'w')
        file_open_mock.assert_any_call('/Users/enrico/cybop/build/scripts/../../tools/api-generator/spec/logic.cybol', 'w')

        write_calls = [
            call('calculate/add'),
            call('<node>\n    <node name="calculate" channel="file" format="element/part" model="api-generator/spec/logic/calculate.cybol"/>\n</node>'),
            call('<node>\n    <node name="add" channel="file" format="element/part" model="api-generator/spec/logic/calculate/add.cybol"/>\n</node>'),
            call('<node>\n    <node name="description" channel="inline" format="text/plain" model="None"/>\n</node>\n')
        ]
        file_open_mock.return_value.__enter__().write.assert_has_calls(write_calls)

    @mock.patch('builtins.open', new_callable=mock_open())
    @mock.patch('apiWriter.os.makedirs')
    def test_update_api_data_two_logig_same_group(self, make_dir_mock, file_open_mock):
        api_items = [
            ApiItem('calculate/add', 'This is the add method', 'logic'),
            ApiItem('calculate/divide', 'This is the divide method', 'logic')
        ]

        Writer(api_items).update_api_data()

        make_dir_calls = [
            call('/Users/enrico/cybop/build/scripts/../../tools/api-generator/spec', exist_ok=True)
        ]
        make_dir_mock.assert_has_calls(make_dir_calls)

        self.assertEqual(5, file_open_mock.call_count)
        file_open_mock.assert_any_call('/Users/enrico/cybop/build/scripts/../../doc/cybol/api/logic.txt', 'w'),
        file_open_mock.assert_any_call('/Users/enrico/cybop/build/scripts/../../tools/api-generator/spec/logic.cybol', 'w'),
        file_open_mock.assert_any_call('/Users/enrico/cybop/build/scripts/../../tools/api-generator/spec/logic/calculate.cybol', 'w'),
        file_open_mock.assert_any_call('/Users/enrico/cybop/build/scripts/../../tools/api-generator/spec/logic/calculate/add.cybol', 'w'),
        file_open_mock.assert_any_call('/Users/enrico/cybop/build/scripts/../../tools/api-generator/spec/logic/calculate/divide.cybol', 'w'),

        write_calls = [
            call('calculate/add\ncalculate/divide'),
            call('<node>\n    <node name="calculate" channel="file" format="element/part" model="api-generator/spec/logic/calculate.cybol"/>\n</node>'),
            call('<node>\n    <node name="add" channel="file" format="element/part" model="api-generator/spec/logic/calculate/add.cybol"/>\n    <node name="divide" channel="file" format="element/part" model="api-generator/spec/logic/calculate/divide.cybol"/>\n</node>'),
            call('<node>\n    <node name="description" channel="inline" format="text/plain" model="None"/>\n</node>\n'),
            call('<node>\n    <node name="description" channel="inline" format="text/plain" model="None"/>\n</node>\n')
        ]
        file_open_mock.return_value.__enter__().write.assert_has_calls(write_calls)
        self.assertEqual(5, file_open_mock.return_value.__enter__().write.call_count)


if __name__ == '__main__':
    unittest.main()
