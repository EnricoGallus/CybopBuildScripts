import unittest

from entityGenerator import EntityItem


class EntityGeneratorCase(unittest.TestCase):
    def test_parseNormalEntity(self):
        result = EntityItem('AElig', '&#x000C6;', 'LATIN CAPITAL LETTER AE')

        self.assertEqual('Æ', result.character)
        self.assertEqual('latin capital letter ae', result.name)
        self.assertEqual('LATIN_CAPITAL_LETTER_AE', result.name_block)
        self.assertEqual([198], result.decimal_points)
        self.assertEqual(['U+00c6'], result.unicode_points)
        self.assertEqual(['0x00c6'], result.hex_points)

        self.assertEqual(1, len(result.names))
        entity_name = result.names[0]
        self.assertEqual('AElig', entity_name.name)
        self.assertEqual(5, entity_name.name_length)
        self.assertEqual('AELIG_LATIN_CAPITAL_LETTER_AE', entity_name.name_block)

    def test_parseAmpersand(self):
        result = EntityItem('AMP', '&#38;#38;', 'AMPERSAND')

        self.assertEqual('&', result.character)
        self.assertEqual('ampersand', result.name)
        self.assertEqual('AMPERSAND', result.name_block)
        self.assertEqual([38], result.decimal_points)
        self.assertEqual(['U+0026'], result.unicode_points)
        self.assertEqual(['0x0026'], result.hex_points)

        self.assertEqual(1, len(result.names))
        entity_name = result.names[0]
        self.assertEqual('AMP', entity_name.name)
        self.assertEqual(3, entity_name.name_length)
        self.assertEqual('AMP_AMPERSAND', entity_name.name_block)

    def test_parseStrangeCombination(self):
        result = EntityItem('nvlt', '&#38;#x0003C;&#x020D2;', 'LESS-THAN SIGN with vertical line')

        self.assertEqual('<⃒', result.character)
        self.assertEqual('less-than sign with vertical line', result.name)
        self.assertEqual('LESS_THAN_SIGN_WITH_VERTICAL_LINE', result.name_block)
        self.assertEqual([60, 8402], result.decimal_points)
        self.assertEqual(['U+003c', 'U+20d2'], result.unicode_points)
        self.assertEqual(['0x003c', '0x20d2'], result.hex_points)

        self.assertEqual(1, len(result.names))
        entity_name = result.names[0]
        self.assertEqual('nvlt', entity_name.name)
        self.assertEqual(4, entity_name.name_length)
        self.assertEqual('NVLT_LESS_THAN_SIGN_WITH_VERTICAL_LINE', entity_name.name_block)


if __name__ == '__main__':
    unittest.main()
