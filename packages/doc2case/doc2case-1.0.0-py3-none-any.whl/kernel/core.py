
from loguru import logger
import requests

from kernel.utils import get_target_value, get_file_path, dump_yaml, dump_json
from kernel import USER_AGENT


class SwaggerParser(object):
    s = requests.session()

    def __init__(self, url):
        self.api_doc_json = self.get_entry_json(url)

    def get_entry_json(self, url):
        response = self.s.get(url).json()
        if response is not None:
            return response

    @staticmethod
    def _make_request_url(testStep_dict, url):
        testStep_dict["name"] = url
        testStep_dict["request"]["url"] = url

    @staticmethod
    def _make_request_method(testStep_dict, entry_json):
        """ parse HAR entry request method, and make testStep method.
        """
        testStep_dict["request"]["method"] = [x for x in entry_json.keys()][0].upper()

    @staticmethod
    def _make_request_headers(testStep_dict, entry_json):
        testStep_headers = {}
        for method, params in entry_json.items():
            testStep_headers["Content-Type"] = params["consumes"][0]
        if testStep_headers:
            testStep_headers["User-Agent"] = USER_AGENT
            testStep_dict["request"]["headers"] = testStep_headers

    @staticmethod
    def _make_request_params(testStep_dict, entry_json):
        for method, params in entry_json.items():
            query_dict = {}
            if params.get("parameters") is None:
                continue
            for param in params.get("parameters"):
                if param is None:
                    continue
                if param.get("in") == "query":
                    queryString = param.get("name")
                    if queryString:
                        query_dict[f"{queryString}"] = f"${queryString}"
                        testStep_dict["request"]["params"] = query_dict

    def _make_request_data(self, testStep_dict, entry_json):
        for method, params in entry_json.items():
            # TODO: make compatible with more mimeType
            request_data_key = "json" if params.get("consumes")[0].startswith("application/json") else "data"
            if method.upper() in ["POST", "PUT", "PATCH"]:
                if params.get("parameters") is None:  #
                    continue
                for param in params.get("parameters"):
                    if param.get("in") == "body":
                        # schema_obj = param.get("name")  # TODO: Strict definitions need to be developed.
                        schema_obj = param.get("schema").get("$ref")
                        if schema_obj is None:
                            continue
                        for obj, properties in self.api_doc_json.get("definitions").items():
                            data_dict = {}
                            if obj in schema_obj:
                                for k, v in properties.get("properties").items():
                                    data_dict[k] = f"${k}"
                            testStep_dict["request"][request_data_key] = data_dict

    @staticmethod
    def _make_validate(testStep_dict):
        testStep_dict["validate"].append({"eq": ["status_code", 200]})

    def _prepare_testStep(self, path, entry_json):
        testStep_dict = {
            "name": "",
            "request": {},
            "validate": []
        }
        self._make_request_url(testStep_dict, path)
        self._make_request_method(testStep_dict, entry_json)
        self._make_request_headers(testStep_dict, entry_json)
        self._make_request_params(testStep_dict, entry_json)
        self._make_request_data(testStep_dict, entry_json)
        self._make_validate(testStep_dict)
        return testStep_dict

    @staticmethod
    def _prepare_config():
        return {
            "base_url": "${ENV(BASE_URL)}",
            "name": "testCase description",
            "variables": {}
        }

    def _prepare_testSteps(self, path, entry_json):
        """ make testStep list.
            testSteps list are parsed from HAR log entries list.

        """
        return [self._prepare_testStep(path, entry_json)]

    def _make_testCase(self, path, entry_json):
        """ Extract info from HAR file and prepare for testCase
        """
        logger.debug("Extract info from HAR file and prepare for testCase.")

        config = self._prepare_config()
        testSteps = self._prepare_testSteps(path, entry_json)
        return {
            "config": config,
            "testSteps": testSteps
        }

    def gen_testCase(self, path=None, file_type="yml"):
        """
        Generate test cases based on the specified path
        """
        if path is not None:
            for test_mapping in get_target_value(path, self.api_doc_json.get("paths")):
                # todo: encapsulation
                logger.info(f"Start to generate testCase.: {path}")
                testCase = self._make_testCase(path, test_mapping)

                file = get_file_path(path, test_mapping) + "." + file_type
                dump_yaml(testCase, file) if file_type == "yml" else dump_json(testCase, file)
                logger.debug("prepared testCase: {}".format(testCase))

        else:  # make compatible with more path swaggerParser
            for path, test_mapping in self.api_doc_json.get("paths").items():
                logger.info(f"Start to generate testCase.: {path}")
                testCase = self._make_testCase(path, test_mapping)

                file = get_file_path(path, test_mapping) + "." + file_type
                logger.debug("spanned file : {}".format(file))
                dump_yaml(testCase, file) if file_type == "yml" else dump_json(testCase, file)
                logger.debug("prepared testCase: {}".format(testCase))

