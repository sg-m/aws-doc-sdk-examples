# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Stub functions that are used by the AWS Lambda unit tests.

When tests are run against an actual AWS account, the stubber class does not
set up stubs and passes all calls through to the Boto 3 client.
"""

from botocore.stub import ANY

from test_tools.example_stubber import ExampleStubber


class LambdaStubber(ExampleStubber):
    """
    A class that implements a variety of stub functions that are used by the
    AWS Lambda unit tests.

    The stubbed functions all expect certain parameters to be passed to them as
    part of the tests, and will raise errors when the actual parameters differ from
    the expected.
    """
    def __init__(self, client, use_stubs=True):
        """
        Initializes the object with a specific client and configures it for
        stubbing or AWS passthrough.

        :param client: A Boto 3 Lambda client.
        :param use_stubs: When True, use stubs to intercept requests. Otherwise,
                          pass requests through to AWS.
        """
        super().__init__(client, use_stubs)

    def stub_create_function(self, function_name, function_arn, role_arn,
                             handler, zip_contents=ANY, error_code=None):
        expected_params = {
            'FunctionName': function_name,
            'Runtime': ANY,
            'Role': role_arn,
            'Handler': handler,
            'Code': {'ZipFile': zip_contents},
            'Description': ANY,
            'Publish': True
        }
        if not error_code:
            self.add_response(
                'create_function',
                expected_params=expected_params,
                service_response={
                    'FunctionArn': function_arn
                }
            )
        else:
            self.add_client_error(
                'create_function',
                expected_params=expected_params,
                service_error_code=error_code
            )

    def stub_delete_function(self, function_name, error_code=None):
        self._stub_bifurcator(
            'delete_function',
            expected_params={'FunctionName': function_name},
            error_code=error_code)
