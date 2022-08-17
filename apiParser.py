import os
import re
from re import Pattern
from apiData import ApiItem, ApiProperty
from apiWriter import Writer


class Parser:
    def __init__(self):
        self.api_regex = re.compile(
            "\/\*\*\s(?P<brief>.*)([\*\s]*?)(?=Description:)([\W\w\s]*?)static wchar_t\* .*(?P<type>LOGIC|STATE).* = L\"(?P<name>.*)\";")
        self.description_regex = re.compile("Description:\s(?P<description>[\W\w\s]*?)(Examples:|Properties:|(\*\/))")
        self.example_regex = re.compile("Examples:\s \*\s(?P<examples>[\W\w]*?)(Properties:|(\*\/))")
        self.properties_regex = re.compile("Properties:(?P<content>[\w\W]*?)(Constraints|\*/)")
        self.constraints_regex = re.compile("Constraints for Property (?P<property>.*):\s(?P<content>[\w\W]*?(Constraints|\*/))")
        self.property_regex = re.compile(" - (?P<name>.*) \((?P<required>.*)\) \[(?P<format>.*)\]: (?P<description>.*)")
        self.variable_regex = re.compile("static wchar_t\* .*?(?P<type>(CHANNEL|ENCODING)) = L\"(?P<value>.+)\";")

        self.basePath = os.path.join(os.path.dirname(__file__), '..', '..')
        self.path_to_format = os.path.join(self.basePath, 'src', 'constant', 'format', 'cybol')
        self.path_to_channel = os.path.join(self.basePath, 'src', 'constant', 'channel', 'cybol')
        self.path_to_encoding = os.path.join(self.basePath, 'src', 'constant', 'encoding', 'cybol')

    def parse_structure(self):
        api_items = []
        for path, dirs, files in os.walk(self.path_to_format):
            for file in files:
                api_items.extend(self.parse_api_javadoc(os.path.join(path, file)))
        for path in [self.path_to_channel, self.path_to_encoding]:
            for cybol_path, dirs, files in os.walk(path):
                for file in files:
                    api_items.extend(self.__parse_variables(os.path.join(cybol_path, file)))

        return api_items

    def parse_api_javadoc(self, path_to_file: str):
        with open(path_to_file) as file_content:
            all_matched = re.findall(self.api_regex, file_content.read())
            return list(map(lambda x: self.__parse_javadoc_content(x), all_matched))

    def __parse_javadoc_content(self, api_element: Pattern[str]):
        api_item = ApiItem(api_element[4], api_element[0].lstrip(' *'), api_element[3].lower())
        content = api_element[2]
        api_item.description = ' '.join(
            list(filter(None,
                        map(lambda x: x.lstrip('*').lstrip(' *'),
                            self.description_regex.match(content).group("description").split(os.linesep)))))
        examples = self.example_regex.search(content)
        if examples:
            api_item.examples = os.linesep.join(list(map(lambda x: x[3:], examples.group("examples").rstrip(' *\n').split(os.linesep))))

        property_content = self.properties_regex.search(content)
        if property_content:
            properties = self.property_regex.findall(property_content[0])
            for x in properties:
                api_item.properties.append(ApiProperty(x[0], x[1], x[2], x[3]))

        constraint_content = self.constraints_regex.findall(content)
        for constraint in constraint_content:
            constrains = self.property_regex.findall(constraint[1])
            for x in constrains:
                api_item.constraints[constraint[0].lower()].append(ApiProperty(x[0], x[1], x[2], x[3]))

        return api_item

    def __parse_variables(self, path_to_file):
        with open(path_to_file) as file_content:
            all_matched = re.findall(self.variable_regex, file_content.read())
            return list(map(lambda x: ApiItem(x[2], '', x[0].lower()), all_matched))


if __name__ == "__main__":
    api_items = Parser().parse_structure()
    writer = Writer(api_items)
    writer.update_api_data()

