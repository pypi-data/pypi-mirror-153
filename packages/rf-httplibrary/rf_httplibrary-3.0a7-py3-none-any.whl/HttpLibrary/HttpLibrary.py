# Copyright (C) 2019 Spiralworks Technologies Inc.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN

import requests
import logging
import os
import jsonschema
import urllib3
import traceback
import json
import time

from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse

from concurrent.futures import ThreadPoolExecutor, as_completed
from requests_toolbelt import MultipartEncoder
from requests import Session, Response
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

from jsonpath_rw_ext import parse
from jsonpath_rw import Index, Fields

from HttpLibrary.version import VERSION

LOGGER = logging.getLogger(__name__)
DEFAULT_TAG = 'default'


class HttpLibrary:
    u"""
        A test library for web services and rest ful api.

        == Table of contents ==

        - `Usage`
        - `Examples`
        - `Author`
        - `Developer Manual`
        - `Importing`
        - `Shortcuts`
        - `Keywords`

    = Usage =

    | =Settings= | =Value=         | =Parameter=          |
    | Library    | HttpLibrary     |                      |

    = Examples =

    |  =Setting=  |     =Value=    |
    | Library     | HttpLibrary    |

    | =Test Case= |     =Action=                  | =Argument=                 |    =Argument=            |
    | Example     | ${screenshotfile}             | Capture Page Screenshot    |                          |
    |             | New Http Session              |                            |                          |
    |             | Create Http Multipart Request | <url>                      |                          |
    |             | Add Http Request File         | file                       | ${screenshotfile}        |
    |             | Add Http Request Parameter    | <paramkey1>                | <paramvalue2>            |
    |             | Add Http Request Parameter    | <paramkey2>                | <paramvalue2>            |
    |             | Invoke Http Request           |                            |                          |
    |             | Http Raise For Status         |                            |                          |
    |             | Close Http Session            |                            |                          |


    | =Test Case= |     =Action=                  | =Argument=                 |    =Argument=            |
    | Example     | New Http Session              |                            |                          |
    |             | Create Http Get Request       | <url>                      |                          |
    |             | Add Http Request Parameter    | <paramkey1>                | <paramvalue2>            |
    |             | Add Http Request Parameter    | <paramkey2>                | <paramvalue2>            |
    |             | Invoke Http Request           |                            |                          |
    |             | Http Raise For Status         |                            |                          |
    |             | Close Http Session            |                            |                          |

    | =Test Case= |     =Action=                  | =Argument=                 |    =Argument=            |
    | Example     | New Http Session              |                            |                          |
    |             | Create Http Post Request      | <url>                      |                          |
    |             | Add Http Request Header       | <headerkey1>               | <headervalue1>           |
    |             | Add Http Request Header       | <headerkey1>               | <headervalue1>           |
    |             | Add Http Request Parameter    | <paramkey1>                | <paramvalue2>            |
    |             | Add Http Request Parameter    | <paramkey2>                | <paramvalue2>            |
    |             | Invoke Http Request           |                            |                          |
    |             | Http Raise For Status         |                            |                          |
    |             | Close Http Session            |                            |                          |


    = Author =

    Created: 11/06/2019

    Author: Shiela Buitizon | email:shiela.buitizon@mnltechnology.com

    Company: Spiralworks Technologies Inc.

    = Developer Manual =

        Compiling this pip package:
            - python setup.py bdist_wheel

        Uploading build to pip
            - python -m twine upload dist/*
    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self):
        self.url = None
        self.session: Session = None
        self.params = []
        self.headers = {}
        self.status: int = None
        self.multipart = False
        self.request = None
        self.request_body = None
        self.response: Response = None

    def new_http_session(self):
        """
        Creates a new http session. Also closes previous session.

        Example:
        | New Http Session        |        |
        | Create Http Get Request | <url>  |
        | Invoke Http Request     |        |
        | Close Http Session      |        |
        """
        # make sure previous session is closed
        self.close_http_session()

        self.session = requests.session()
        self.params = []
        self.headers = {}
        self.status = None
        self.multipart = False
        self.request = None
        self.request_body = None
        self.response = None

    def create_new_session(self,
                           url,
                           headers={},
                           params=[],
                           cookies={},
                           files=None,
                           auth=None,
                           hooks=None,
                           timeout=None,
                           proxies=None,
                           verify=False,
                           ):
        """A Requests session.

        Provides cookie persistence, connection-pooling, and configuration.
        """
        if self._has_existing_session():
            self.close_http_session()
        self.session = requests.Session()

    def _has_existing_session(self):
        if self.session:
            return True

    def create_http_get_request(self, url=None):
        """
        Creates an Http Get Request.

        Example:
        | Create Http Get Request | <url> |
        """
        assert self.session, "No session created."
        self.request = getattr(self.session, 'get')
        self.url = url

    def create_http_post_request(self, url=None):
        """
        Creates an Http Post Request.

        Example:
        | Create Http Post Request | <url> |
        """
        assert self.session, "No session created."
        self.request = getattr(self.session, 'post')
        self.url = url

    def create_http_put_request(self, url=None):
        """
        Creates an Http Put Request.

        Example:
        | Create Http Put Request | <url> |
        """
        assert self.session, "No session created."
        self.request = getattr(self.session, 'put')
        self.url = url

    def create_http_delete_request(self, url=None):
        """
        Creates an Http Delete Request.

        Example:
        | Create Http Delete Request | <url> |
        """
        assert self.session, "No session created."
        self.request = getattr(self.session, 'delete')
        self.url = url

    def create_http_multipart_request(self, url=None):
        """
        Creates an Http Multipart Request.

        Example:
        | Create Http Multipart Request | <url> |
        """
        assert self.session, "No session created."
        self.multipart = True
        self.request = getattr(self.session, 'post')
        self.url = url

    def add_http_request_file(self, name, file, content_type='application/octet-stream', file_name=None):
        """
        Adds an HTTP Request File. This keyword is only allowed for multipart request

        Example:

        | ${screenshotfile}             | Capture Page Screenshot |                   |
        | New Http Session              |                         |                   |
        | Create Http Multipart Request | <url>                   |                   |
        | Add Http Request File         | file                    | ${screenshotfile} |
        | Add Http Request Parameter    | <paramkey1>             | <paramvalue2>     |
        | Add Http Request Parameter    | <paramkey2>             | <paramvalue2>     |
        | Invoke Http Request           |                         |                   |
        | Http Raise For Status         |                         |                   |
        | Close Http Session            |                         |                   |
        """
        assert self.multipart, "Only allowed for multipart request."
        assert os.path.isfile(file), "Not a valid file: " + str(file)

        if not file_name:
            path, file_name = os.path.split(file)

        LOGGER.info("filename: " + str(file_name))
        self.params.append((name, (file_name, open(file, 'rb'), content_type)))

    def add_http_request_parameter(self, name, value):
        """
        Adds an HTTP Request Parameter.

        Example:

        | Add HTTP Request Parameter | <paramkey> | <paramvalue> |
        """
        self.params.append((name, value))
        return self.params

    def add_http_request_parameters(self, **req_params):
        """
        Adds HTTP Request Parameters. Accepts dictionary as parameter.

        Example 1:

        | Add HTTP Request Parameters | key=val | foo=bar | a=b |

        Example 2:

        | &{dict} | Create Dictionary | key=val | foo=bar | a=b |
        | Add HTTP Request Parameters | &{dict} |

        """
        for req_param in req_params:
            print(req_param, ":", req_params[req_param])
            self.params.append((req_param, req_params[req_param]))
        return self.params

    def update_request_parameter(self, params):
        """
        """
        self.params = params
        return self.params

    def add_http_request_header(self, name, value):
        """
        Adds HTTP Request Header.

        Example:

        | Add HTTP Request Header | Accept | application/json | # Indicates that json format is the acceptable media type for the response |
        """
        self.headers.update({name: value})
        return self.headers

    def add_http_request_headers(self, **req_headers):
        """
        Adds HTTP Request Headers.  Accepts dictionary as parameter.

        Example1:

        | Add HTTP Request Headers | key=val | foo=bar | a=b |

        Example2:

        | &{dict} | Create Dictionary | key=val | foo=bar | a=b |
        | Add HTTP Request Headers | &{dict} |
        """
        self.headers.update(req_headers)
        return self.headers

    def update_request_header(self, **kwargs):
        """Takes in a dictionary as parameter, then adds it as a request header.
        """
        self.headers.update(kwargs)
        return self.headers

    def set_http_request_body(self, body):
        """
        Sets HTTP request body.

        Example:
        | New Http Session         |                |                  |                                                                            |
        | Create Http Post Request | <url>          |                  |                                                                            |
        | Add HTTP Request Header  | Accept         | application/json | # Indicates that json format is the acceptable media type for the response |
        | Set Http Request Body    | { json body }  |                  | # Accepts string, json, dictionary, etc depending on the Accept header set |
        | Invoke Http Request      |                |                  |                                                                            |
        | Close Http Session       |                |                  |                                                                            |
        """
        self.request_body = body

    def invoke_http_request(self):
        """
        Invokes Http Request

        Example:
        | New Http Session        |       |
        | Create Http Get Request | <url> |
        | Invoke Http Request     |       |
        | Close Http Session      |       |
        """
        assert self.session, "No session created."
        assert self.request, "No request created."

        data = self.params
        if self.multipart:
            m = MultipartEncoder(self.params)
            self.headers.update({'Content-Type': m.content_type})
            data = m
        elif self.request_body:
            data = self.request_body

        self._request_invoke(data)
        self.status = self.response.status_code

    def _request_invoke(self, data):
        LOGGER.info("url: " + self.url)
        LOGGER.info("method: " + self._get_method())
        LOGGER.info("headers: " + str(self.headers))
        LOGGER.info("params: " + str(self.params))

        if self._get_method() == 'get':
            self.response = self.request(self.url, params=data, headers=self.headers)
        else:
            self.response = self.request(self.url, data=data, headers=self.headers)

    def _get_method(self):
        return self.request.__name__

    def _close_file_params(self):
        if not self.params:
            return

        # make sure we close open files
        for param in self.params:
            value = param[1]
            if isinstance(value, tuple):
                value[1].close()

    def http_raise_for_status(self):
        """
        Raises stored :class:`HTTPError`, if one occurred.

        Example:
        | Raise For Status |
        """
        assert self.response is not None, "No request invoked."
        self.response.raise_for_status()

    def http_response_status_code_should_be_equal_to(self, status_code: int):
        """
        Asserts response status code value

        Example:
        | Http Response Status Code Should Be Equal |
        """
        assert self.status, "No request invoked."
        assert self.status == status_code, "Expecting response status code of " + str(status_code)

    def assert_response_status(self, statusCode):
        """
        """
        if self.status:
            assert str(self.response.status_code) == str(statusCode)

    def return_response_status(self):
        return self.response.status_code

    def get_http_response_string(self):
        """
        Returns http response string

        Example:
        | New Http Session        |                          |
        | Create Http Get Request | <url>                    |
        | Invoke Http Request     |                          |
        | ${responsetext}         | Get Http Response String |
        | Close Http Session      |                          |
        """
        assert self.response is not None, "No request invoked."
        return self.response.text

    def get_http_response_headers(self):
        """
        Returns HTTP Response Headers

        Example:
        | `New Http Session`        |                               |
        | `Create Http Get Request` | https://robotframework.org/   |
        | `Invoke Http Request`     |                               |
        | ${responseHeaders}        | `Get Http Response Headers`   |
        | `Close Http Session`      |                               |
        """
        assert self.response is not None, "No request invoked."
        LOGGER.info(self.response.headers)
        return self.response.headers

    def get_http_response_json(self):
        """
        Returns http response json

        Example:
        | New Http Session        |                        |
        | Create Http Get Request | <url>                  |
        | Invoke Http Request     |                        |
        | ${responsejson}         | Get Http Response Json |
        | Close Http Session      |                        |
        """
        assert self.response is not None, "No request invoked."
        return self.response.json()

    def _consume_response(self):
        self._close_file_params()

        if self.response is not None:
            self.response.close()

    def _get_validation_parameters(self, validation, param_name, default_value=None):
        return validation.get('parameters', {}).get(param_name, default_value)

    def _json_path_check(self, json_data, result, validation):
        variables = self._get_validation_parameters(validation, 'variables', {})
        json_paths = self._get_validation_parameters(validation, 'json_paths')
        max_retries = self._get_validation_parameters(validation, 'max_retries', 0)
        retry_delay = self._get_validation_parameters(validation, 'retry_delay', 15)

        result['max_retries'] = max_retries
        result['retry_delay'] = retry_delay

        for json_path in json_paths:
            name = json_path.get('name', None)
            path = json_path.get('path', None)
            json_path_expr = parse(path)
            values = [match.value for match in json_path_expr.find(json_data)]
            if len(values) == 1:
                variables[name] = values[0]
            else:
                variables[name] = values

        conditions = self._get_validation_parameters(validation, 'conditions')
        for condition in conditions:
            assert 'expression' in condition, 'One condition provided in JSON_PATH, has no expression parameter.'
            expression = condition['expression']
            condition_name = condition.get('name', expression)
            formatted_message = condition.get('formatted_message', 'Json path FAIL for condition : {condition_name}')

            vars = dict()
            vars.update(variables)
            eval_value = eval(expression, vars)
            if not isinstance(eval_value, bool):
                result.update(
                    validation_type="JSON_PATH",
                    message=f'expression {expression} does not return bool type.',
                    status="FAIL"
                )
                break

            if not eval_value:
                result.update(
                    validation_type="JSON_PATH",
                    message=formatted_message.format(**variables),
                    status="FAIL"
                )
                break

    def _json_schema_check(self, json_data, result, validation):
        path = self._get_validation_parameters(validation, 'path')
        assert path, 'json schema parameter path not available. / validation[type=JSON_SCHEMA][parameter][path]'
        assert os.path.isfile(path), f'Path {path} not found.'

        try:
            with open(path) as f:
                schema = json.load(f)
        except Exception as e:
            result.update(
                validation_type="JSON_SCHEMA",
                message=f'invalid schema found - {path}.',
                status="FAIL"
            )
            return

        resolver = jsonschema.RefResolver(f'file://{path}', schema)
        try:
            jsonschema.validate(json_data, schema, resolver=resolver)
        except jsonschema.ValidationError as e:
            filename = os.path.basename(path)
            result.update(
                validation_type="JSON_SCHEMA",
                message=f'Validation error for schema "{filename}": {e.message}',
                status="FAIL"
            )

    def _read_json_response(self, r, result):
        try:
            return json.loads(r.data.decode('utf-8'))
        except Exception as e:
            print(traceback.format_exc())
            result.update(
                validation_type="EXCEPTION",
                data=r.data,
                message=f'response data is not JSON type.',
                status="FAIL"
            )

    def _header_check(self, response, result, validation):
        parameters = validation.get('parameters', {})

        for header in parameters:
            valid_values = parameters[header]
            if isinstance(valid_values, str):
                valid_values = [valid_values]

            assert isinstance(valid_values, list), 'headers should be list or str'

            response_header_value = response.headers[header]
            if response_header_value not in valid_values:
                result.update(
                    validation_type="HEADER",
                    message=f'unable to find header {response_header_value} in {valid_values}.',
                    status="FAIL"
                )

    def process_expand(self, result, r, expand_urls):
        url = result['url']
        url_tag = result.get('tag', DEFAULT_TAG)
        expand_variables = expand_urls.get('variables', {})

        if 'status' in result:
            return result

        if 'tags' in expand_urls:
            apply_tags = expand_urls['tags']
        else:
            apply_tags = [expand_urls.get('tag', DEFAULT_TAG)]

        if url_tag not in apply_tags:
            return result

        json_data = self._read_json_response(r, result)

        json_path_value = expand_urls['json_path']
        formatter = expand_urls['formatter']
        destination_tag = expand_urls.get('destination_tag', DEFAULT_TAG)

        json_path_list = json_path_value if isinstance(json_path_value, list) else [json_path_value]
        expand_variable_list = expand_variables if isinstance(expand_variables, list) else [expand_variables]

        for json_path in json_path_list:
            json_path_expr = parse(json_path)
            values = [match.value for match in json_path_expr.find(json_data)]
            parent_path = url[0:url.rindex('/')]
            o = urlparse(url)
            root_path = f'{o.scheme}://{o.netloc}{o.port if o.port else ""}'
            for expand_variable in expand_variable_list:
                variables = dict(parent_path=parent_path, root_path=root_path)
                urls = result['expanded_urls']
                for value in values:
                    variables.update(json_value=value)
                    # Support double formatting
                    url = formatter.format(**variables)

                    try:
                        url = url.format(**expand_variable)
                    except ValueError:
                        print(traceback.format_exc())

                    url_item = dict(url=url, tag=destination_tag)
                    if url_item not in urls:
                        urls.append(url_item)

    def process_expands(self, result, r, expand_urls):
        result['expanded_urls'] = list()
        if isinstance(expand_urls, list):
            for expand_url in expand_urls:
                self.process_expand(result, r, expand_url)
            LOGGER.info(f">result['expanded_urls'] - {len(result['expanded_urls'])} / {result['expanded_urls']}")

    def _invoke_get(self, http, headers, result, validations, expand_urls=None):
        url = result['url']
        url_tag = result.get('tag', DEFAULT_TAG)

        http_headers = {}
        if url_tag in headers:
            http_headers = headers[url_tag]

        if 'started_time' not in result:
            result['started_time'] = datetime.now()

        retry = result.get('retry', -1)

        try:
            result['execution_time'] = datetime.now()
            retry += 1
            result['retry'] = retry

            LOGGER.info(f"GET {url}, with headers={http_headers}, with retry {retry}")
            r = http.request('GET', url, headers=http_headers)
            json_data = None

            if expand_urls:
                self.process_expands(result, r, expand_urls)

            for validation in validations:
                assert 'type' in validation, 'A validation has no type.'

                if 'tags' in validation:
                    validation_tags = validation['tags']
                else:
                    validation_tags = [validation.get('tag', DEFAULT_TAG)]

                if url_tag not in validation_tags:
                    # don't process validation tag if not included
                    continue

                if validation['type'] == 'STATUS_CODE':
                    LOGGER.info(f">>>> Status Code Validation, url = {url}")
                    valid_response_codes = self._get_validation_parameters(validation, 'response_codes', [200, 201])
                    if r.status not in valid_response_codes:
                        result.update(
                            validation_type="STATUS_CODE",
                            status_code=r.status,
                            message=f'Expected {valid_response_codes} but was {r.status}.',
                            valid_response_codes=valid_response_codes,
                            status="FAIL"
                        )

                if validation['type'] in ['JSON_PATH', 'JSON_SCHEMA'] and json_data is None:
                    json_data = self._read_json_response(r, result)

                if validation['type'] == 'JSON_PATH':
                    LOGGER.info(f">>>> Json Path Validation, url = {url}")
                    self._json_path_check(json_data, result, validation)

                if validation['type'] == 'HEADER':
                    LOGGER.info(f">>>> Header Validation, url = {url}")
                    self._header_check(r, result, validation)

                if validation['type'] == 'JSON_SCHEMA':
                    LOGGER.info(f">>>> Json Schema Validation, url = {url}")
                    self._json_schema_check(json_data, result, validation)

                if 'status' in result:
                    break

        except Exception as exc:
            print(traceback.format_exc())
            result.update(
                validation_type="EXCEPTION",
                message='%r generated an exception: %s' % (url, exc),
                status="FAIL"
            )

        if 'status' not in result:
            result.update(status='PASS')

        return result

    def _process_urls(self, executor, url_dicts, http, headers, validations, expand_urls=None):
        if not url_dicts:
            return []

        results = []
        future_to_url = {
            executor.submit(self._invoke_get,
                            http,
                            headers,
                            url_dict,
                            validations,
                            expand_urls): url_dict['url']
            for url_dict in url_dicts
        }

        for future in as_completed(future_to_url):
            url = future_to_url[future]

            try:
                results.append(future.result())
            except Exception as exc:
                print(traceback.format_exc())
                results.append(dict(
                    url=url,
                    validation_type="EXCEPTION",
                    message='%r generated an exception: %s' % (url, exc),
                    status="FAIL"
                ))

        return results

    def _get_expanded_uls(self, results):
        expanded_urls = []
        for result in results:
            new_urls = result.get('expanded_urls', None)
            if new_urls:
                for new_url in new_urls:
                    if new_url not in expanded_urls:
                        LOGGER.info(f'expand url -> {new_url}')
                        expanded_urls.append(new_url)

        LOGGER.info(f"Expanded URL Count: {len(expanded_urls)}")
        return expanded_urls

    def _is_not_done(self, results):
        """
        Returns True if all results are PASS or max_retries has been reached.
        :param results: the url results to check
        :return: True if all results are PASS or max_retries has been reached.
        """
        for result in results:
            if result.get('status', 'PASS') == 'FAIL':
                retry = result['retry']
                max_retries = result['max_retries']

                if retry < max_retries:
                    return True

        return False

    def _get_for_retry_now(self, for_retry_results):
        """
        Returns the url results that is candidate for retry now.
        This will compute based on the retry delay.

        :param for_retry_results: the url result candidate for retry
        :return: the url results that should be retried now
        """
        results = []
        now = datetime.now()
        for result in for_retry_results:
            if result.get('status', 'PASS') == 'FAIL':
                execution_time = result['execution_time']
                retry_delay = result['retry_delay']
                retry = result['retry']
                max_retries = result['max_retries']

                if (now - execution_time) >= timedelta(seconds=retry_delay) and retry < max_retries:
                    result.pop('status', None)
                    result.pop('validation_type', None)
                    result.pop('message', None)

                    results.append(result)

        return results

    def append_urls(self, urls, url_value, tags):
        for tag in tags:
            urls.append(dict(url=url_value, tag=tag))

    def bulk_http_validate(self, config: dict):
        """
            Bulk validation for urls using HTTP GET method.

            Supports validation for the following :

            * STATUS_CODE - for response code checking

            * JSON_PATH - for response body expression checks using json path value

            * JSON_SCHEMA - for response schema checks

            * HEADER - for response header key and value checks

            Example:
            | Bulk Http Validate | ${config_payload} | # contains bulk http test payload configuration |

            Sample Payload:
            | {
            |   "parallel": "true",
            |   "thread_size": "10",
            |   "retry_timeout: 600,
            |   "retries": {
            |       "retries": 3,
            |       "redirect": 3
            |   },
            |   "timeout": {
            |       "connect": 1.0,
            |       "read": 3.0
            |   },
            |   "validations": [
            |   {
            |       "parameters": {
            |           "response_codes": [200, 201]
            |       }
            |       "type": "STATUS_CODE",
            |       "tags": [
            |           "default",
            |           "<destination tag name>"
            |       ]
            |   },
            |   {
            |       "parameters": {
            |           "max_retries": 20,
            |           "retry_delay": 15,
            |           "variables": {
            |               "expected_version": 123
            |           },
            |           "json_paths": [
            |               {"name": "actual_version", "path": "$.//"}
            |           ],
            |           "conditions": [
            |              {
            |                   "name": "version check",
            |                   "expression": "int(actual_version) >= expected_version",
            |                   "formatted_message":
            |                       "Version should be {expected_version}. Found: {actual_version}"
            |               }
            |           ]
            |       },
            |       "type": "JSON_PATH"
            |   },
            |   {
            |       "parameters": {
            |           "path": "<path to json schema file>"
            |       },
            |       "type": "JSON_SCHEMA"
            |   },
            |   {
            |       "parameters": {
            |           "content-type": ["json", "image/png", "image/jpg", "image/jpeg"]
            |       },
            |       "type": "HEADER",
            |       "tags": [
            |           "<destination tag name>"
            |       ]
            |   }],
            |   "urls": [
            |       "url1",
            |       "url2",
            |       "url3",
            |       "url4",
            |       "url5"
            |   ],
            |   "headers": [
            |       {   "Authorization": "Bearer <token>",
            |           "<header key>": "header value>"
            |       }
            |   ],
            |   "expand_urls": {
            |       "destination_tag": "<destination tag name>"
            |       "json_path": "$.uri",
            |       "formatter": "{parent_path}/{json_value}"
            |   },
            |   "aggregate": false,
            |   "return_type": "ALL|PASS|FAIL",
            | }

            Workers:

            * ``parallel`` (default is True) flag for processing strategy

            * ``thread_size`` (default is 5) specifies the number of workers to use

            * ``retry_timeout`` (default to 10 mins) general wait time for retry.
              Will overrider ``max_retries`` and ``retry_delay`` rule in JSON_PATH

            * connection ``retries`` defaults : retries = 2 and redirect = 2.

            * connection ``timeout`` defaults : connect = 2.0 and read = 3.0.

            Validations:

            * validation with type ``STATUS_CODE`` defines expected ``response_codes``

            * validation with type ``JSON_PATH`` defines expression checks via
            the following parameters:
            | > max_retries - retry count for failed conditions
            | > retry_delay - retry delay for failed conditions
            | > variables - variable values are substituted in condition expression
            | > json_paths - save value in specied path to name variable defined
            | > conditions - defines condition ``expression`` for assertion checks.
            |   Returns the ``formatted_message`` when asssertions failS.

            * validation with type ``JSON_SCHEMA`` defines json schema file path that will
            be used for response schema validation.

            * validation with type ``HEADER`` defines expected response header key and value pair

            Expanded Urls:

            The list of url can also be expanded using ``expands_urls`` where values are taken
            from ``json_path`` specified, substituted in ``formatter`` and added to original url list
            under "default" or "<destination>" tag specified.

            Headers:

            Request header configuration containing list of key value pair.

            Result Aggregates:

            * ``aggregate`` when set to False will group results by url

            * ``aggregate`` when set to True will group results by :
            tag name (value is default if not set), status and message

            * ``return_type`` accepts ``ALL|PASS|FAIL``. ``ALL`` will return passed
            and failed test result, ``PASS`` and ``FAIL`` will only return passed
            and failed test, respectively.

            * Aside from specied validation types (``STATUS_CODE``, ``JSON_PATH``, ``JSON_SCHEMA``
              and ``HEADER``) result will return validation_type equal to ``EXCEPTION`` if
              - response data is not in proper JSON format
              - invoking url generated an exception

            Samplet output: (aggregate=False)
            | output = [
            | {
            |   "url": "url1",
            |   "tag": "default",
            |   "started_time": datetime.datetime(2021, 9, 15, 2, 51, 10, 866370),
            |   "execution_time": datetime.datetime(2021, 9, 15, 2, 51, 10, 866379),
            |   "retry": 0,
            |   "expanded_urls": [
            |   {
            |       "url": "url1-imageurl1",
            |       "tag": "imagepath",
            |       "started_time": datetime.datetime(2021, 9, 15, 2, 51, 12, 335243),
            |       "execution_time": datetime.datetime(2021, 9, 15, 2, 51, 12, 335251),
            |       "retry": 0,
            |       "status": "PASS",
            |   },
            |   {
            |       "url": "url1-imageurl2",
            |       "tag": "imagepath",
            |       "started_time": datetime.datetime(2021, 9, 15, 2, 51, 12, 335295),
            |       "execution_time": datetime.datetime(2021, 9, 15, 2, 51, 12, 335298),
            |       "retry": 0,
            |       "status": "PASS",
            |   }
            | },
            | {
            |   "url": "url2",
            |   "tag": "default",
            |   "started_time": datetime.datetime(2021, 9, 15, 2, 51, 10, 866370),
            |   "execution_time": datetime.datetime(2021, 9, 15, 2, 51, 10, 866379),
            |   "retry": 0,
            |   "expanded_urls": [
            |   {
            |       "url": "url2-imageurl1",
            |       "tag": "imagepath",
            |       "started_time": datetime.datetime(2021, 9, 15, 2, 51, 12, 335243),
            |       "execution_time": datetime.datetime(2021, 9, 15, 2, 51, 12, 335251),
            |       "retry": 0,
            |       "status": "FAIL",
            |       "validation_type": "STATUS_CODE",
            |       "status_code": 404,
            |       "message": "Expected [200, 201] but was 404.",
            |       "valid_response_codes": [200, 201]
            |   },
            |   {
            |       "url": "url2-imageurl2",
            |       "tag": "imagepath",
            |       "started_time": datetime.datetime(2021, 9, 15, 2, 51, 12, 335295),
            |       "execution_time": datetime.datetime(2021, 9, 15, 2, 51, 12, 335298),
            |       "retry": 0,
            |       "status": "FAIL",
            |       "validation_type": "HEADER",
            |       "message": "unable to find header text/html in ['json', 'image/png', 'image/jpg', 'image/jpeg']"
            |   }
            | },
            | {
            |   "url": "url3",
            |   "tag": "default",
            |   "started_time": datetime.datetime(2021, 9, 15, 2, 51, 12, 335243),
            |   "execution_time": datetime.datetime(2021, 9, 15, 2, 51, 12, 335251),
            |   "retry": 0,
            |   "status": "FAIL",
            |   "validation_type": "STATUS_CODE",
            |   "status_code": 404,
            |   "message": "Expected [200, 201] but was 404.",
            |   "valid_response_codes": [200, 201]
            | },
            | {
            |   "url": "url4",
            |   "tag": "default",
            |   "started_time": datetime.datetime(2021, 9, 15, 2, 51, 12, 335243),
            |   "execution_time": datetime.datetime(2021, 9, 15, 2, 51, 12, 335251),
            |   "retry": 0,
            |   "status": "FAIL",
            |   "validation_type": "JSON_PATH",
            |   "message": "Json path failed for condition 'schema_version'.",
            | },
            | {
            |   "url": "url5",
            |   "tag": "default",
            |   "started_time": datetime.datetime(2021, 4, 19, 18, 32, 44, 864982),
            |   "execution_time": datetime.datetime(2021, 4, 19, 18, 32, 54, 861017),
            |   "retry": 3,
            |   "max_retries": 20,
            |   "retry_delay": 15,
            |   "validation_type": "JSON_SCHEMA",
            |   "message": "Validation error for schema 'schema.file.json': [] is too short",
            |   "status": "FAIL"
            | }]

            Sample output: (aggregate=True)
            | output = [
            | {
            |   "tag": "default",
            |   "status": "PASS",
            |   "urls": [
            |       "url1",
            |       "url2"
            |   ]
            | },
            | {
            |   "tag": "default",
            |   "status": "FAIL",
            |   "message": "Expected [200, 201] but was 404.",
            |   "urls": [
            |       "url3"
            |   ]
            | },
            | {
            |   "tag": "default",
            |   "status": "FAIL",
            |   "message": "Json path failed for condition 'schema_version'.",
            |   "urls": [
            |       "url4"
            |   ]
            | },
            | {
            |   "tag": "default",
            |   "status": "FAIL",
            |   "message": "Validation error for schema 'schema.file.json': [] is too short",
            |   "urls": [
            |       "url5"
            |   ]
            | },
            | {
            |   "tag": "imagepath",
            |   "status": "PASS",
            |   "urls": [
            |       "url1-imageurl1",
            |       "url1-imageurl2"
            |   ]
            | },
            | {
            |   "tag": "imagepath",
            |   "status": "FAIL",
            |   "urls": [
            |       "url2-imageurl1"
            |   ],
            |   "message": "Expected [200, 201] but was 404.",
            | },
            | {
            |   "tag": "imagepath",
            |   "status": "FAIL",
            |   "urls": [
            |       "url2-imageurl2"
            |   ],
            |   "message": "unable to find header text/html in ['json', 'image/png', 'image/jpg', 'image/jpeg']"
            | }

            Tag Support:

            Validations, Urls, Expand Url and Headers all have tag support to help group aggregate results.
            Default tag value is ``default``. Tag name can be set in ``validations``, ``urls`` and
            ``headers`` using ``tags`` and in Expand URL using ``destination_tag``

            ​New in HttpLibrary 2.0.0b3
        """
        assert 'urls' in config, 'No urls found'
        assert 'validations' in config, 'No validations found'
        assert len(config['urls']) > 0, 'urls cannot be empty'
        assert len(config['validations']) > 0, 'validations cannot be empty'

        for validation in config['validations']:
            assert validation.get('type', '') in ["STATUS_CODE", "JSON_PATH", "JSON_SCHEMA", "HEADER"]

        retries = 2
        redirect = 2
        connection_timeout = 2.0
        read_timeout = 3.0
        thread_size = 5
        aggregate = config.get('aggregate', False)
        return_type = config.get('return_type', 'FAIL')
        retry_timeout = config.get('retry_timeout', 600)  # 10 minutes

        assert return_type in ('PASS', 'FAIL', 'ALL'), 'return_type can only be "PASS", "FAIL" or "ALL"'
        return_types = ['PASS', 'FAIL'] if return_type == 'ALL' else [return_type]

        expand_urls = config.get("expand_urls", None)

        if expand_urls and isinstance(expand_urls, dict):
            assert 'json_path' in expand_urls, 'json_path key not in expand_urls'
            assert 'formatter' in expand_urls, 'formatter key not in expand_urls'
        if expand_urls and isinstance(expand_urls, list):
            i = 0
            for expand_url in expand_urls:
                assert 'json_path' in expand_url, f'json_path key not in expand_url[{i}]'
                assert 'formatter' in expand_url, f'formatter key not in expand_url[{i}]'
                i += 1

        # update retries based from config
        if 'retries' in config:
            if 'retries' in config['retries']:
                retries = config['retries']['retries']
            if 'redirect' in config['retries']:
                redirect = config['retries']['redirect']

        # update timeouts based from config
        if 'timeout' in config:
            if 'connect' in config['timeout']:
                connection_timeout = config['timeout']['connect']
            if 'read' in config['timeout']:
                read_timeout = config['timeout']['read']

        cofig_headers = config.get('headers', {})
        headers = {}
        if cofig_headers and isinstance(cofig_headers, list):
            for header in cofig_headers:
                tag = header.get('tag', DEFAULT_TAG)
                headers[tag] = header
        if cofig_headers and isinstance(cofig_headers, dict):
            headers[DEFAULT_TAG] = cofig_headers

        # update thread_size
        parallel = config.get('parellel', True)
        if parallel and 'thread_size' in config:
            thread_size = config['thread_size']
        if not parallel:
            thread_size = 1

        urllib3.disable_warnings()
        cert_reqs = config.get('cert_reqs', 'NONE')

        urls = []
        for url in config['urls']:
            if isinstance(url, str):
                urls.append(dict(url=url, tag=DEFAULT_TAG))
            elif isinstance(url, dict):
                tags = [url['tag']] if 'tag' in url else url['tags']
                if 'urls' in url:
                    for inner_url in url['urls']:
                        self.append_urls(urls, inner_url, tags)
                else:
                    url_value = url['url']
                    self.append_urls(urls, url_value, tags)
            else:
                raise AssertionError(f'urls item can only be of type dict or str. url={url}, type={type(url)}')

        results = []
        with urllib3.PoolManager(
                retries=urllib3.Retry(retries, redirect=redirect),
                timeout=urllib3.Timeout(connect=connection_timeout, read=read_timeout),
                cert_reqs=cert_reqs) as http:
            with ThreadPoolExecutor(max_workers=thread_size) as executor:
                results.extend(self._process_urls(executor, urls, http, headers, config['validations'], expand_urls))

                # get all expanded urls and process
                results.extend(self._process_urls(executor, self._get_expanded_uls(results), http, headers, config['validations']))

                # lets process retries
                start_time = datetime.now()
                for_retry_results = []
                for result in results:
                    if result['status'] == 'FAIL' and result.get('retry', 0) < result.get('max_retries', 0):
                        for_retry_results.append(result)

                LOGGER.info(f"for retries {len(for_retry_results)}")
                while self._is_not_done(for_retry_results) and (datetime.now() - start_time) < timedelta(seconds=retry_timeout):
                    for_retry_now = self._get_for_retry_now(for_retry_results)
                    if for_retry_now:
                        self._process_urls(executor, for_retry_now, http, headers, config['validations'])

                    LOGGER.info("sleeping for the next batch of retry...")
                    time.sleep(1)

                if self._is_not_done(for_retry_results) and (datetime.now() - start_time) >= timedelta(seconds=retry_timeout):
                    LOGGER.warning(f"Retry timeout reached. timeout={retry_timeout}")

        # lets filter the results based from acceptable return types
        filtered_results = []
        for result in results:
            if result.get('status', "FAIL") in return_types:
                filtered_results.append(result)

        if aggregate:
            aggregation = dict()
            for result in filtered_results:
                status = result['status']
                tag = result.get('tag', '')
                message = result.get('message', '')
                key = f'{tag}/{status}/{message}'

                item = aggregation.get(key)
                if not item:
                    item = dict(tag=tag, status=status, urls=[result['url']])
                    aggregation[key] = item

                    if message:
                        item.update(message=message)
                else:
                    item['urls'].append(result['url'])

            return aggregation.values()

        return filtered_results

    def close_http_session(self):
        """
        Closes http session

        Example:
        | New Http Session        |       |
        | Create Http Get Request | <url> |
        | Invoke Http Request     |       |
        | Close Http Session      |       |
        """
        self._consume_response()

        if self.session:
            self.session.close()
