import os
from subprocess import run, TimeoutExpired


class IntegrationTestResult:
    def __init__(self, name: str, success: bool):
        self.name = name
        self.success = success

    def encode(self):
        return self.__dict__


class IntegrationTester:
    def __init__(self):
        base_path = os.path.join(os.path.dirname(__file__), '..', '..')
        self.path_to_cyboi = os.path.join('..', 'src', 'controller', 'cyboi')
        self.path_to_examples = os.path.join(base_path, 'examples')
        self.results = []

    def __test_execution(self, relative_path_to_test_file: str):
        print("Execute 'run.cybol' in " + relative_path_to_test_file)
        try:
            result = run(
                [self.path_to_cyboi, relative_path_to_test_file],
                timeout=1,
                cwd=self.path_to_examples,
                capture_output=True)
            print(result.stdout)
            return IntegrationTestResult(relative_path_to_test_file, result.returncode == 0)
        except TimeoutExpired as e:
            print('Execution of ' + relative_path_to_test_file + ' failed')
            return IntegrationTestResult(relative_path_to_test_file, False)

    def __find_all_programs(self):
        for path, dirs, files in os.walk(self.path_to_examples):
            if 'run.cybol' in files:
                dirs[:] = []  # found run.cybol stop processing further
                self.results.append(self.__test_execution(os.path.join(path.replace(self.path_to_examples + os.sep, ''), 'run.cybol')))
            else:
                print('No test found in: ' + path)

    def execute(self):
        self.__find_all_programs()
        success = len(list(filter(lambda x: x.success is True, self.results)))
        total = len(self.results)
        with open('result.txt', 'w') as outfile:
            outfile.write(f'From {total} are {success} succeeded and {total - success} failed' + os.linesep)
            for result in self.results:
                outfile.write(f'name: {result.name}, success: {result.success}' + os.linesep)


if __name__ == "__main__":
    IntegrationTester().execute()
