#!/usr/bin/python
import os
import urllib.request
import re
from jinja2 import Template

# todo implement sort
# todo implement conversion of unicodes
# todo implement generation of unicode_character_code_model file

model_template_raw = '''{% for entity in entities %}
/**
 * The {{ entity.name }} html character entity reference model.
 *
 * Name: {{ entity.entity }}
 * Character: {{ entity.character }}
 * Unicode code point: {{ entity.unicode }} ({{ entity.hex }})
 * Description: {{ entity.name }}
 */
static wchar_t* {{ entity.name_block }}_HTML_CHARACTER_ENTITY_REFERENCE_MODEL = L"{{ entity.entity }}";
static int* {{ entity.name_block }}_HTML_CHARACTER_ENTITY_REFERENCE_MODEL_COUNT = NUMBER_{{ entity.character_length }}_INTEGER_STATE_CYBOI_MODEL_ARRAY;
{% endfor %}	
'''

executor_template_raw = '''{% for entity in entities %}
    if (r == *FALSE_BOOLEAN_STATE_CYBOI_MODEL) {

        check_operation((void*) &r, p1, (void*) {{ entity.name_block }}_HTML_CHARACTER_ENTITY_REFERENCE_MODEL, p2, (void*) {{ entity.name_block }}_HTML_CHARACTER_ENTITY_REFERENCE_MODEL_COUNT, (void*) EQUAL_COMPARE_LOGIC_CYBOI_FORMAT, (void*) WIDE_CHARACTER_TEXT_STATE_CYBOI_TYPE);

        if (r != *FALSE_BOOLEAN_STATE_CYBOI_MODEL) {

            modify_item(p0, (void*) {{ entity.name_block }}_UNICODE_CHARACTER_CODE_MODEL, (void*) WIDE_CHARACTER_TEXT_STATE_CYBOI_TYPE, (void*) FALSE_BOOLEAN_STATE_CYBOI_MODEL, (void*) PRIMITIVE_STATE_CYBOI_MODEL_COUNT, *NULL_POINTER_STATE_CYBOI_MODEL, (void*) VALUE_PRIMITIVE_STATE_CYBOI_NAME, (void*) TRUE_BOOLEAN_STATE_CYBOI_MODEL, (void*) APPEND_MODIFY_LOGIC_CYBOI_FORMAT);
        }
    }
    {% endfor %}
'''

class EntityItem:
    def __init__(self, entity: str, hex: str, name: str):
        self.entity = entity
        self.character_length = len(entity)
        self.name = name.lower()
        self.name_block = name.replace(' ', '_')
        self.hex = hex # todo remove later
        self.hex_values = hex.replace('38;', '') if hex.startswith("38;") else hex.replace('x', '').split(';')
        # self.unicode_pos = int(self.hex, 16)
        self.unicode = 'unicode' # self.unicode = chr(self.unicode_pos)


class Parser:
    def __init__(self):
        self.url_entity = 'https://www.w3.org/2003/entities/2007/w3centities-f.ent'
        self.regex = re.compile('<\!ENTITY (?P<entity>[a-zA-Z0-9\.]*) *\"(&| &)#(?P<unicode>.*);\" ><!--(?P<name>.*) -->\s')

    def parse_entities(self):
        with urllib.request.urlopen(self.url_entity) as response:
            html = response.read().decode()
            all_entities = self.regex.findall(html)
            return list(map(lambda x: EntityItem(x[0], x[2], x[3]), all_entities))


class Writer:
    def __init__(self, entities):
        self.basePath = os.path.dirname(__file__)
        self.model_path = os.path.join(self.basePath, '..', '..', 'src', 'constant', 'model', 'character_entity_reference', 'html_character_entity_reference_model.c')
        self.executor_path = os.path.join(self.basePath, '..', '..', 'src', 'executor', 'representer', 'deserialiser', 'character_reference', 'html_character_reference_deserialiser.c')
        self.entities = entities

    def write_content(self):
        self.__write_file_content(self.model_path, 46, -3, Template(model_template_raw))
        self.__write_file_content(self.executor_path, 56, -4, Template(executor_template_raw))

    def __write_file_content(self, file_path, pre, post, template):
        original = open(file_path)
        original_content = original.readlines()
        pre = original_content[0:pre]
        post = original_content[post:]

        with open(file_path, 'w') as outfile:
            outfile.write(''.join(pre))
            outfile.write(template.render(entities=self.entities))
            outfile.write(''.join(post))


if __name__ == "__main__":
    entities = Parser().parse_entities()
    Writer(entities).write_content()