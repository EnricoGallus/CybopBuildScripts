from collections import defaultdict


class ApiItem:
    def __init__(self, name: str, brief: str, type: str):
        self.name = name
        if '/' in name:
            split = name.split('/')
            self.group = split[0]
            self.specifier = split[1]
        self.brief = brief
        self.type = type
        self.description = None
        self.examples = None
        self.properties = []
        self.constraints = defaultdict(list)


class ApiProperty:
    def __init__(self, name: str, required: str, format: str, description: str):
        self.name = name
        self.required = 'true' if required == 'required' else 'false'
        self.format = format
        self.description = description
