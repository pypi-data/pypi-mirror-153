from API_Gen.base_generator import BaseGenerator


class SanicGenerator(BaseGenerator):

    def __init__(self, api_info) -> None:
        super().__init__(api_info)

    # Intitlaizes the wepapp.py file
    def _write_imports_to_api(self):
        self.api_import_placeholder = f"from . import {self.framework_object}\
                                      \nfrom sanic import json\
                                      \nfrom . import DUMMY_RESPONSE_JSON\n\n"

        with open(self.project_path_api, 'w') as fi:
            fi.write(self.api_import_placeholder)

    def _write_methods_to_api(self):
        try:
            for api in self.api_info['api_list']:

                self.api_method_placeholder += f"@{self.framework_object}.{api['HTTP_method'].lower()}('{api['path']}')\
                                                 \nasync def {api['method_handler_name']}(request):\
                                                 \n\treturn json(DUMMY_RESPONSE_JSON['{api['method_handler_name']}'])\n\n"

                self.dummy_response_placeholder[api['method_handler_name']
                                                ] = api['response']

            with open(self.project_path_api, 'a') as fi:
                fi.write(self.api_method_placeholder)

            self._write_to_dummy_response(self.dummy_response_placeholder)

        except KeyError as e:
            print(e)
