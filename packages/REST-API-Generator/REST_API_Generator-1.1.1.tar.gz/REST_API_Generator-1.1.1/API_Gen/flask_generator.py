from API_Gen.base_generator import BaseGenerator
from API_Gen.exceptions import InvalidFrameworkException


class FlaskGenerator(BaseGenerator):
    '''
    FlaskGenerator will create end-point handlers for Flask framework applications
    - Child class of BaseGenerator
    ...

    Methods
    -------

    def _write_imports_to_api(self):
        writes import statements to api file

    def _write_methods_to_api(self):
        writes url handlers to api file
    '''
    FRAMEWORK_NAME = 'flask'

    def __init__(self, api_info) -> None:
        super().__init__(api_info)

    def _write_imports_to_api(self):
        self.api_import_placeholder = f"from . import {self.framework_object}\
                                        \nfrom flask import request\
                                        \nfrom . import DUMMY_RESPONSE_JSON\n\n"

        with open(self.project_path_api, 'w') as file:
            file.write(self.api_import_placeholder)

    def _write_methods_to_api(self):
        try:
            for api in self.api_info['api_list']:

                self.api_method_placeholder += f"@{self.framework_object}.route('{api['path']}',methods=['{api['HTTP_method']}'])\
                                                 \ndef {api['method_handler_name']}():\
                                                 \n\treturn DUMMY_RESPONSE_JSON['{api['method_handler_name']}']\n\n"

                self.dummy_response_placeholder[api['method_handler_name']
                                                ] = api['response']

            with open(self.project_path_api, 'a') as fi:
                fi.write(self.api_method_placeholder)

            self._write_to_dummy_response(self.dummy_response_placeholder)

        except KeyError as e:
            raise KeyError(f"Invalid key in Json '{e.args[0]}' ")
