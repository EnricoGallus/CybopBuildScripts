import os
from itertools import groupby
from jinja2 import Template
from apiData import ApiItem

variable_template_raw = '''<node>{% for element in elements %}
    <node name="{{ element.name }}" channel="inline" format="text/plain" model="{{ element.name }}"/>{% endfor %}
</node>
'''

type_template_raw = '''<node>{% for group in group_names %}
    <node name="{{ group }}" channel="file" format="element/part" model="api-generator/spec/{{ type }}/{{ group }}.cybol"/>{% endfor %}
</node>
'''

group_template_raw = '''<node>{% for element in elements %}
    <node name="{{ element.specifier }}" channel="file" format="element/part" model="api-generator/spec/{{ type }}/{{ element.group }}/{{ element.specifier }}.cybol"/>{% endfor %}
</node>
'''

specifier_template_raw = '''<node>
    <node name="description" channel="inline" format="text/plain" model="{{ element.description}}"/>{% if element.examples is not none %}
    <node name="examples" channel="file" format="text/plain" model="api-generator/spec/{{ element.type }}/{{ element.group }}/{{ element.specifier }}/examples.txt"/>{% endif %}{% if element.properties|length > 0 %}
    <node name="properties" channel="file" format="element/part" model="api-generator/spec/{{ element.type }}/{{ element.group }}/{{ element.specifier }}/properties.cybol"/>{% endif %}{% if element.constraints|length > 0 %}{% for constraint in element.constraints %}
    <node name="{{ constraint }}_constraints" channel="file" format="element/part" model="api-generator/spec/{{ element.type }}/{{ element.group }}/{{ element.specifier }}/{{ constraint }}_constraints.cybol"/>{% endfor %}{% endif %}
</node>

'''
properties_template_raw = '''<node>{% for property in properties %}
    <node name="{{ property.name }}" channel="inline" format="text/plain" model="">
        <node name="required" channel="inline" format="logicvalue/boolean" model="{{ property.required }}"/>
        <node name="format" channel="inline" format="text/plain" model="{{ property.format }}"/>
        <node name="description" channel="inline" format="text/plain" model="{{ property.description }}"/>
    </node>{% endfor %}
</node>

'''


class Writer:
    def __init__(self, api_items: []):
        self.api_items = api_items
        self.basePath = os.path.join(os.path.dirname(__file__), '..', '..')
        self.path_to_format = os.path.join(self.basePath, 'include', 'constant', 'format', 'cybol')
        self.spec_output_path = os.path.join(self.basePath, 'tools', 'api-generator', 'spec')
        self.api_output_path = os.path.join(self.basePath, 'doc', 'cybol', 'api')
        self.variable_types = {'encoding', 'channel'}

    def update_api_data(self):
        for type_group_key, grouped_by_types_list in groupby(self.api_items, key=lambda element: element.type):
            type_group = list(sorted(grouped_by_types_list, key=lambda x: x.name))
            self.__write_api_specification(type_group, type_group_key)
            if type_group_key in self.variable_types:
                self.__write_variable_groups(type_group, type_group_key)
            else:
                self.__write_type_groups(type_group, type_group_key)
                for group_key, grouped_by_group_list in groupby(type_group, key=lambda element: element.group):
                    group = list(sorted(grouped_by_group_list, key=lambda x: x.name))
                    self.__write_groups(group, type_group_key, group_key)
                    # skipping type_group template at the moment
                    for element in group:
                        self.__write_specifier(element)
                        if element.examples is not None:
                            self.__write_examples(element)
                        self.__write_properties(element)
                        self.__write_constraints(element)

    def __write_api_specification(self, elements, type):
        file_path = os.path.join(self.api_output_path, type + '.txt')
        names = os.linesep.join(list(sorted(map(lambda x: x.name, elements))))
        self.__write_content(file_path, names)

    def __write_variable_groups(self, elements, type):
        file_path = os.path.join(self.spec_output_path, type + '.cybol')
        self.__write_content(file_path, Template(variable_template_raw).render(elements=elements))

    def __write_type_groups(self, elements, type):
        file_path = os.path.join(self.spec_output_path, type + '.cybol')
        group_names = sorted(set(map(lambda x: x.group, elements)))
        self.__write_content(file_path, Template(type_template_raw).render(group_names=group_names, type=type))

    def __write_groups(self, elements, type, group):
        file_path = os.path.join(self.spec_output_path, type, group + '.cybol')
        self.__write_content(file_path, Template(group_template_raw).render(elements=elements, type=type))

    def __write_specifier(self, element: ApiItem):
        file_path = os.path.join(self.spec_output_path, element.type, element.group, element.specifier + '.cybol')
        self.__write_content(file_path, Template(specifier_template_raw).render(element=element))

    def __write_examples(self, element: ApiItem):
        file_path = os.path.join(self.spec_output_path, element.type, element.group, element.specifier, 'examples.txt')
        self.__write_content(file_path, element.examples)

    def __write_properties(self, element: ApiItem):
        if len(element.properties) > 0:
            file_path = os.path.join(self.spec_output_path, element.type, element.group, element.specifier, 'properties.cybol')
            self.__write_content(file_path, Template(properties_template_raw).render(properties=element.properties))

    def __write_constraints(self, element: ApiItem):
        if len(element.constraints) > 0:
            for constraint in element.constraints:
                file_path = os.path.join(self.spec_output_path, element.type, element.group, element.specifier, constraint + '_constraints.cybol')
                self.__write_content(file_path, Template(properties_template_raw).render(properties=element.constraints.get(constraint)))

    def __write_content(self, path_to_file: str, content: str):
        os.makedirs(os.path.dirname(path_to_file), exist_ok=True)
        with open(path_to_file, 'w') as outfile:
            outfile.write(content)
