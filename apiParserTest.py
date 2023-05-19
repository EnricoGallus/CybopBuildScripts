import os
import unittest
from unittest.mock import patch, mock_open
from apiWriter import Writer
from apiParser import Parser

calculate_add_logic = '''/**
 * The calculate/add logic cybol format.
 *
 * Description:
 *
 * Adds the operand to the result.
 *
 * sum = summand + summand
 *
 * Caution! Do not use this operation for adding characters (strings)!
 * They may be concatenated by using the "modify/append" operation.
 *
 * Examples:
 *
 * <node name="add_integer" channel="inline" format="calculate/add" model="">
 *     <node name="result" channel="inline" format="text/cybol-path" model=".result"/>
 *     <node name="operand" channel="inline" format="number/integer" model="2"/>
 * </node>
 *
 * <node name="add_arrays_with_equal_size" channel="inline" format="calculate/add" model="">
 *     <node name="result" channel="inline" format="text/cybol-path" model=".result"/>
 *     <node name="operand" channel="inline" format="number/integer" model="1,2,3"/>
 * </node>
 *
 * <node name="add_summand_to_sum" channel="inline" format="calculate/add" model="">
 *     <node name="result" channel="inline" format="text/cybol-path" model=".sum"/>
 *     <node name="operand" channel="inline" format="text/cybol-path" model=".summand"/>
 * </node>
 *
 * Properties:
 *
 * - result (required) [text/cybol-path]: The sum resulting from the addition. It initially represents the first summand.
 * - operand (required) [text/cybol-path | number/any]: The second summand.
 * - count (optional) [text/cybol-path | number/integer]: The number of elements to be calculated. This is relevant only for arrays with more than one element. If null, the default is the lesser of left and right operand count.
 * - result_index (optional) [text/cybol-path | number/integer]: The result index from where to start calculating. If null, the default is zero.
 * - operand_index (optional) [text/cybol-path | number/integer]: The operand index from where to start calculating. If null, the default is zero.
 */
static wchar_t* ADD_CALCULATE_LOGIC_CYBOL_FORMAT = L"calculate/add";
static int* ADD_CALCULATE_LOGIC_CYBOL_FORMAT_COUNT = NUMBER_13_INTEGER_STATE_CYBOI_MODEL_ARRAY;'''


number_state_logic = '''/**
 * The number/integer state cybol format.
 *
 * Description:
 *
 * An integer is a datum of integral data type, a data type that represents some range of mathematical integers.
 * It is allowed to contain negative values.
 *
 * The standard type used internally is int with 32 Bits.
 * It has a value range from −2,147,483,648 to 2,147,483,647, which is from −(2^31) to 2^31 - 1.
 *
 * Each number can be an element of a vector (array), e.g.:
 * - integer: 1,2,3,4
 *
 * Examples:
 *
 * <node name="decimal_base" channel="inline" format="number/integer" model="24"/>
 * <node name="negative" channel="inline" format="number/integer" model="-24"/>
 * <node name="array" channel="inline" format="number/integer" model="0,1,2,3,4"/>
 * <!-- These numbers will get recognised only if the consider number base prefix flag is set. -->
 * <node name="octal" channel="inline" format="number/integer" model="030"/>
 * <node name="many_zeros" channel="inline" format="number/integer" model="00030"/>
 * <node name="negative_octal" channel="inline" format="number/integer" model="-030"/>
 * <node name="hexadecimal" channel="inline" format="number/integer" model="0x18"/>
 * <node name="negative_hexadecimal" channel="inline" format="number/integer" model="-0x18"/>
 * <node name="hexadecimal_small_letter" channel="inline" format="number/integer" model="0xb"/>
 * <node name="hexadecimal_capital_letter" channel="inline" format="number/integer" model="0x1C"/>
 */
static wchar_t* INTEGER_NUMBER_STATE_CYBOL_FORMAT = L"number/integer";
static int* INTEGER_NUMBER_STATE_CYBOL_FORMAT_COUNT = NUMBER_14_INTEGER_STATE_CYBOI_MODEL_ARRAY;'''


class ApiParserTest(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data=calculate_add_logic)
    def test_parsing_logic(self, file_open_mock):
        parser = Parser()
        result = parser.parse_api_javadoc('calculate_logic_cybol_format.test')
        self.assertEqual(1, len(result))
        calculate_add_logic = next(filter(lambda x: x.name == 'calculate/add', result), None)
        self.assertIsNotNone(calculate_add_logic)
        self.assertEqual('The calculate/add logic cybol format.', calculate_add_logic.brief)
        self.assertEqual('calculate/add', calculate_add_logic.name)
        self.assertEqual('calculate', calculate_add_logic.group)
        self.assertEqual('add', calculate_add_logic.specifier)
        self.assertEqual('logic', calculate_add_logic.type)
        self.assertEqual('''Adds the operand to the result.

sum = summand + summand

Caution! Do not use this operation for adding characters (strings)!
They may be concatenated by using the &#x0022;modify/append&#x0022; operation.''', calculate_add_logic.description)
        self.assertIsNotNone(calculate_add_logic.examples)
        self.assertEqual(5, len(calculate_add_logic.properties))

    @patch('builtins.open', new_callable=mock_open, read_data=number_state_logic)
    def test_parsing_state(self, file_open_mock):
        parser = Parser()
        result = parser.parse_api_javadoc('number_state_cybol_format.test')
        self.assertEqual(1, len(result))
        integer_state = next(filter(lambda x: x.name == 'number/integer', result), None)
        self.maxDiff = None
        self.assertIsNotNone(integer_state)
        self.assertEqual('The number/integer state cybol format.', integer_state.brief)
        self.assertEqual('number/integer', integer_state.name)
        self.assertEqual('number', integer_state.group)
        self.assertEqual('integer', integer_state.specifier)
        self.assertEqual('state', integer_state.type)
        self.assertEqual('''An integer is a datum of integral data type, a data type that represents some range of mathematical integers.
It is allowed to contain negative values.

The standard type used internally is int with 32 Bits.
It has a value range from −2,147,483,648 to 2,147,483,647, which is from −(2^31) to 2^31 - 1.

Each number can be an element of a vector (array), e.g.:
- integer: 1,2,3,4''', integer_state.description)
        self.assertIsNotNone(integer_state.examples)
        self.assertEqual(0, len(integer_state.properties))

    @unittest.skip("should only be executed as integration test")
    def test_parsing_whole_structure(self):
        parser = Parser()
        api_items = parser.parse_structure()

        self.assertEqual(66, len(api_items))

        writer = Writer(api_items)
        writer.update_api_data()


if __name__ == '__main__':
    unittest.main()
