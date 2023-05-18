import os
import unittest
from apiWriter import Writer
from apiParser import Parser


def path_to_test_file(file_name):
    return os.path.join(os.path.dirname(__file__), 'test', file_name)


class ApiParserTest(unittest.TestCase):
    def test_parsing_logic(self):
        parser = Parser()
        result = parser.parse_api_javadoc(path_to_test_file('calculate_logic_cybol_format.test'))
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

    def test_parsing_state(self):
        parser = Parser()
        result = parser.parse_api_javadoc(path_to_test_file('number_state_cybol_format.test'))
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
