import unittest

from entityGenerator import EntityItem


class EntityGeneratorCase(unittest.TestCase):
    def test_parseNormalEntity(self):
        result = EntityItem('AElig', '&#x000C6;', 'LATIN CAPITAL LETTER AE')

        self.assertEqual('AElig', result.entity)
        self.assertEqual('Æ', result.character)
        self.assertEqual(5, result.character_length)
        self.assertEqual('latin capital letter ae', result.name)
        self.assertEqual('LATIN_CAPITAL_LETTER_AE', result.name_block)
        self.assertEqual([198], result.decimal_points)
        self.assertEqual(['U+00c6'], result.unicode_points)
        self.assertEqual(['0x00c6'], result.hex_points)

    def test_parseAmpersand(self):
        result = EntityItem('AMP', '&#38;#38;', 'AMPERSAND')

        self.assertEqual('AMP', result.entity)
        self.assertEqual('&', result.character)
        self.assertEqual(3, result.character_length)
        self.assertEqual('ampersand', result.name)
        self.assertEqual('AMPERSAND', result.name_block)
        self.assertEqual([38], result.decimal_points)
        self.assertEqual(['U+0026'], result.unicode_points)
        self.assertEqual(['0x0026'], result.hex_points)

    def test_parseStrangeCombination(self):
        result = EntityItem('nvlt', '&#38;#x0003C;&#x020D2;', 'LESS-THAN SIGN with vertical line')

        self.assertEqual('nvlt', result.entity)
        self.assertEqual('<⃒', result.character)
        self.assertEqual(4, result.character_length)
        self.assertEqual('less-than sign with vertical line', result.name)
        self.assertEqual('LESS_THAN_SIGN_WITH_VERTICAL_LINE', result.name_block)
        self.assertEqual([60, 8402], result.decimal_points)
        self.assertEqual(['U+003c', 'U+20d2'], result.unicode_points)
        self.assertEqual(['0x003c', '0x20d2'], result.hex_points)


if __name__ == '__main__':
    unittest.main()
