#!/usr/bin/python
import os
import urllib.request
import re
import html
from jinja2 import Template

model_template_raw = '''{% for entity in entities %}{% for e in entity.names %}
/**
 * The {{ e.name }} html character entity reference model.
 *
 * Name: {{ e.name }}
 * Character: {{ entity.character }}
 * Unicode code point: {{ entity.unicode_string }} ({{ entity.decimal_string }})
 * Description: {{ entity.name }}
 */
static wchar_t* {{ e.name_block }}_HTML_CHARACTER_ENTITY_REFERENCE_MODEL = L"{{ e.name }}";
static int* {{ e.name_block }}_HTML_CHARACTER_ENTITY_REFERENCE_MODEL_COUNT = NUMBER_{{ e.name_length }}_INTEGER_STATE_CYBOI_MODEL_ARRAY;
{% endfor %}{% endfor %}
'''

unicode_template_raw = '''{% for entity in entities %}
static wchar_t {{ entity.name_block }}_UNICODE_CHARACTER_CODE_MODEL_ARRAY[] = { {{ entity.hex_string }} };
static wchar_t* {{ entity.name_block }}_UNICODE_CHARACTER_CODE_MODEL = {{ entity.name_block }}_UNICODE_CHARACTER_CODE_MODEL_ARRAY;
{% endfor %}
'''

executor_template_raw = '''{% for entity in entities %}{% for e in entity.names %}
    if (r == *FALSE_BOOLEAN_STATE_CYBOI_MODEL) {

        check_operation((void*) &r, p1, (void*) {{ e.name_block }}_HTML_CHARACTER_ENTITY_REFERENCE_MODEL, p2, (void*) {{ e.name_block }}_HTML_CHARACTER_ENTITY_REFERENCE_MODEL_COUNT, (void*) EQUAL_COMPARE_LOGIC_CYBOI_FORMAT, (void*) WIDE_CHARACTER_TEXT_STATE_CYBOI_TYPE);

        if (r != *FALSE_BOOLEAN_STATE_CYBOI_MODEL) {

            modify_item(p0, (void*) {{ entity.name_block }}_UNICODE_CHARACTER_CODE_MODEL, (void*) WIDE_CHARACTER_TEXT_STATE_CYBOI_TYPE, (void*) FALSE_BOOLEAN_STATE_CYBOI_MODEL, (void*) PRIMITIVE_STATE_CYBOI_MODEL_COUNT, *NULL_POINTER_STATE_CYBOI_MODEL, (void*) VALUE_PRIMITIVE_STATE_CYBOI_NAME, (void*) TRUE_BOOLEAN_STATE_CYBOI_MODEL, (void*) APPEND_MODIFY_LOGIC_CYBOI_FORMAT);
        }
    }
{% endfor %}{% endfor %}
'''


class EntityName:
    def __init__(self, name: str, post_name_block: str):
        self.name = name.replace(".", "_")
        self.name_length = len(name)
        self.name_block = "{0}_{1}".format(name.upper(), post_name_block).replace(".", "_")


class EntityItem:
    def __init__(self, entity: str, hex_raw: str, name: str):
        normalized_hex = hex_raw.replace('#38;', '', 1)
        self.character = html.unescape(normalized_hex)
        self.name = name.lower()
        self.name_block = name.replace(' ', '_').replace('-', '_').replace("_(LF)", "").replace("/", "_").upper()
        self.decimal_points = []
        self.unicode_points = []
        self.hex_points = []
        self.names = [EntityName(entity, self.name_block)]

        if len(normalized_hex) == 5:
            decimal_value = int(normalized_hex[2:-1])
            self.__add_decimal_to_lists(decimal_value)
        else:
            hex_values = normalized_hex.rstrip(';').split(';')
            for hex_value in hex_values:
                decimal_value = int(hex_value[4:], 16)
                self.__add_decimal_to_lists(decimal_value)
        self.hex_string = ', '.join(self.hex_points)
        self.decimal_string = ";".join(map(str, self.decimal_points))
        self.unicode_string = ';'.join(self.unicode_points)

    def __add_decimal_to_lists(self, decimal_value: int):
        self.decimal_points.append(decimal_value)
        self.unicode_points.append('U+' + format(decimal_value, '04x'))
        self.hex_points.append('0x' + format(decimal_value, '04x'))

    def add_entity_name(self, name: str):
        self.names.append(EntityName(name, self.name_block))


class Parser:
    def __init__(self):
        self.url_entity = 'https://www.w3.org/2003/entities/2007/w3centities-f.ent'
        self.regex = re.compile('<\!ENTITY (?P<entity>[a-zA-Z0-9\.]*) *\"(?P<unicode>.*)\" ><!--(?P<name>.*) -->\s')

    def parse_entities(self):
        with urllib.request.urlopen(self.url_entity) as response:
            html = response.read().decode()
            found_entities = self.regex.findall(html)
            entities = dict({})
            for x in found_entities:
                entity_name = x[0]
                entity_item = EntityItem(entity_name, x[1], x[2])
                existing = entities.get(entity_item.name_block)
                if not existing:
                    entities[entity_item.name_block] = entity_item
                else:
                    if entity_name.lower() not in set(map(lambda e: e.name.lower(), existing.names)):
                        existing.add_entity_name(entity_name)

            return list(sorted(list(entities.values()), key=lambda e: e.decimal_points[0]))


class Writer:
    def __init__(self, entities):
        self.basePath = os.path.dirname(__file__)
        self.model_path = os.path.join(self.basePath, '..', '..', 'src', 'constant', 'model', 'character_entity_reference', 'html_character_entity_reference_model.c')
        self.executor_path = os.path.join(self.basePath, '..', '..', 'src', 'executor', 'representer', 'deserialiser', 'character_reference', 'html_character_reference_deserialiser.c')
        self.unicode_path = os.path.join(self.basePath, '..', '..', 'src', 'constant', 'model', 'character_code', 'unicode', 'unicode_character_code_model.c')
        self.entities = entities

    def write_content(self):
        self.__write_file_content(self.model_path, 46, -3, self.entities, Template(model_template_raw))
        self.__write_file_content(self.executor_path, 56, -4, self.entities, Template(executor_template_raw))
        self.__write_file_content(self.unicode_path, 1199, -159, filter(lambda x: len(x.decimal_points) > 1 or (len(x.decimal_points) == 1 and x.decimal_points[0] > 255), self.entities), Template(unicode_template_raw))

    def __write_file_content(self, file_path, pre, post, entities, template):
        original = open(file_path)
        original_content = original.readlines()
        pre = original_content[0:pre]
        post = original_content[post:]

        with open(file_path, 'w') as outfile:
            outfile.write(''.join(pre))
            outfile.write(template.render(entities=entities))
            outfile.write(''.join(post))


if __name__ == "__main__":
    all_entities = Parser().parse_entities()
    Writer(all_entities).write_content()
