import json
import os
from API_Gen.exceptions import InvalidFrameworkException


class BaseGenerator():
    '''
    BaseGenerator class is a parent class to generate files and intializations

    ...

    Attributes
    ----------
    api_info : dict
        input json configuration
    init_file : str
        the name of the init file
    main_file : str
        the name of the init file
    api_file : str
        the number of legs the animal has (default 4)

    Methods
    -------
    says(sound=None)
        Prints the anima
    '''
    VALID_FRAMEWORKS = ['sanic']

    def __init__(self, api_info) -> None:
        self.api_info = api_info
        self.init_file = '__init__.py'
        self.main_file = '__main__.py'
        if not api_info.get('api_module_name'):
            self.api_info['api_module_name'] = 'webapp'
        self.api_file = f"{self.api_info['api_module_name']}.py"
        self.framework_object = self.api_info.get('framework_object', 'app')
        self.dummy_response_file = 'dummy_response.json'
        self.api_method_placeholder = ''
        self.dummy_response_placeholder = {}

    # Function that generates the file structure for the new API
    def _generate_file_paths(self):
        try:
            os.chdir(self.api_info['project_dir'])
            self.project_path = os.path.join(
                self.api_info['project_dir'], self.api_info['project_name'])
            self.project_path_init = os.path.join(
                self.project_path, self.init_file)
            self.project_path_main = os.path.join(
                self.project_path, self.main_file)
            self.project_path_api = os.path.join(
                self.project_path, self.api_file)
            self.project_path_dummy_response = os.path.join(
                self.project_path, self.dummy_response_file)

            if not os.path.isdir(self.project_path):
                os.mkdir(self.project_path)

        except FileNotFoundError as e:
            print(f'ERROR:- {e.strerror} "{e.filename}"')
        except KeyError as e:
            print(f"Missing key in Json '{e.args[0]}'")

    # Function that intializes the main and init files of the project
    def _write_to_init(self):
        try:
            # intializing the __init__.py file
            self.init_placeholder = f"from {self.api_info['framekwork'].lower()} import {self.api_info['framekwork'].capitalize()}\
                                        \n######\
                                        \n# Remove these line of code when you no longer require a dummy response\
                                        \nimport json\
                                        \nimport os\
                                        \nDUMMY_RESPONSE_FILE = os.path.join(\'{self.api_info['project_name']}\','dummy_response.json')\
                                        \nwith open(DUMMY_RESPONSE_FILE, 'r') as fi:\
                                        \n    DUMMY_RESPONSE_JSON = json.load(fi)\
                                        \n######\
                                        \n\n{self.framework_object} = {self.api_info['framekwork'].capitalize()}('structure_flask')\n"

            # intializing the __init__ file
            with open(self.project_path_init, 'w') as file:
                file.write(self.init_placeholder)

        except KeyError as e:
            print(f"Missing key in Json '{e.args[0]}'")

    def _write_to_main(self):
        # intializing the __main__.py file
        self.main_placeholder = f"from . import {self.framework_object}\
                                  \nfrom . import {self.api_info['api_module_name']}\
                                  \n\n{self.framework_object}.run(host='{self.api_info['host']}', port={self.api_info['port']})\n"

        # intializing the __main__ file
        with open(self.project_path_main, 'w') as file:
            file.write(self.main_placeholder)

    def _write_to_dummy_response(self, dummy_response_data, read_file=True):
        try:
            if read_file:
                with open(self.project_path_dummy_response, 'r') as file:
                    dummy_response_data.update(json.load(file))
            with open(self.project_path_dummy_response, 'w') as file:
                file.write(json.dumps(dummy_response_data))
        except FileNotFoundError as e:
            self._write_to_dummy_response(
                dummy_response_data=dummy_response_data, read_file=False)

    def create_apis(self):
        if self.api_info['framekwork'].lower() not in BaseGenerator.VALID_FRAMEWORKS:
            raise InvalidFrameworkException(
                f"'{self.api_info['framekwork']}' is not an acceptable Framework")
        self._generate_file_paths()
        self._write_to_init()
        self._write_to_main()
        self._write_imports_to_api()
        self._write_methods_to_api()

    def add_apis(self):
        if self.api_info['framekwork'].lower() not in BaseGenerator.VALID_FRAMEWORKS:
            raise InvalidFrameworkException(
                f"'{self.api_info['framekwork']}' is not an acceptable Framework")
        self._generate_file_paths()
        self._write_methods_to_api()
