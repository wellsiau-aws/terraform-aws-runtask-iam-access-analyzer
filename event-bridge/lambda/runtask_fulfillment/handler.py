'''
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
import json
import logging
import os
import boto3
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode

session = boto3.Session()
ia2_client = session.client('accessanalyzer')

logger = logging.getLogger()
if 'log_level' in os.environ:
    logger.setLevel(os.environ['log_level'])
    logger.info("Log level set to %s" % logger.getEffectiveLevel())
else:
    logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(json.dumps(event))
    try:
        endpoint = event["payload"]["detail"]["plan_json_api_url"]
        access_token = event["payload"]["detail"]["access_token"]
        headers = __build_standard_headers(access_token)
        response, response_raw = __get(endpoint, headers)
        json_response = json.loads(response.decode("utf-8"))
        logger.info("Headers : {}".format(response_raw.headers))
        logger.info("JSON Response : {}".format(json.dumps(json_response)))

        fulfillment_output, fulfillment_pass = get_iam_policy(json_response["resource_changes"])
        return {
            "status": fulfillment_pass,
            "message": fulfillment_output
        }
  
    except Exception as e:
        logger.exception("Run Task Fulfillment error: {}".format(e))
        raise

def get_iam_policy(plan_output):
    ia2_error = 0
    ia2_security_warning = 0
    ia2_suggestion = 0
    ia2_warning = 0
    ia2_pass = "passed" #Only passed, failed or running are allowed.
    for resource in plan_output:
        logger.info(resource)
        if resource["type"] == "aws_iam_policy":
            if resource["change"]["after"] != None:
                iam_policy = json.loads(resource["change"]["after"]["policy"])
                logger.info(json.dumps(iam_policy))
                ia2_response = validate_policy(json.dumps(iam_policy), "IDENTITY_POLICY")
                logger.info(ia2_response)
                if len(ia2_response["findings"]) > 0:
                    for finding in ia2_response["findings"]:
                        if finding["findingType"] == "ERROR":
                            ia2_error += 1
                        elif finding["findingType"] == "SECURITY_WARNING":
                            ia2_security_warning += 1
                        elif finding["findingType"] == "SUGGESTION":
                            ia2_suggestion += 1
                        elif finding["findingType"] == "WARNING":
                            ia2_warning += 1
            else:
                logger.info("New policy is null / deleted")
    ia2_results = "{} ERROR, {} SECURITY_WARNING, {} SUGGESTION, {} WARNING".format(
        ia2_error, ia2_security_warning, ia2_suggestion, ia2_warning)
    if ia2_error + ia2_security_warning > 0:
        ia2_pass = "failed"
    return ia2_results, ia2_pass

def validate_policy(policy_document, policy_type):
    logger.info("Inspecting policy via IAM Access Analyzer")
    response = ia2_client.validate_policy(
        policyDocument=policy_document,
        policyType=policy_type
    )
    return response

def __build_standard_headers(api_token):
    return {
        "Authorization": "Bearer {}".format(api_token),
        "Content-type": "application/vnd.api+json",
    }
    
def __get(endpoint, headers):
    request = Request(endpoint, headers=headers or {}, method = "GET")
    try:
        with urlopen(request, timeout=10) as response:
            return response.read(), response
    except HTTPError as error:
        logger.error(error.status, error.reason)
    except URLError as error:
        logger.error(error.reason)
    except TimeoutError:
        logger.error("Request timed out")