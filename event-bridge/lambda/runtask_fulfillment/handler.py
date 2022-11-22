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
import time
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from enum import Enum

class IA2PolicyType(Enum):
    aws_iam_policy = "IDENTITY_POLICY"
    aws_iam_role_policy = "IDENTITY_POLICY"
    aws_iam_role = "RESOURCE_POLICY"
    aws_organizations_policy = "SERVICE_CONTROL_POLICY"

class TFPlanPolicyKey(Enum):
    aws_iam_policy = "policy"
    aws_iam_role_policy = "policy"
    aws_iam_role = "assume_role_policy"
    aws_organizations_policy = "policy"

session = boto3.Session()
ia2_client = session.client('accessanalyzer')
cwl_client = session.client('logs')

logger = logging.getLogger()
if 'log_level' in os.environ:
    logger.setLevel(os.environ["log_level"])
    logger.info("Log level set to %s" % logger.getEffectiveLevel())
else:
    logger.setLevel(logging.INFO)

if 'CW_LOG_GROUP_NAME' in os.environ:
    LOG_GROUP_NAME = os.environ["CW_LOG_GROUP_NAME"]
else:
    # disable logging if environment variable is not set
    LOG_GROUP_NAME = False

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

        run_id = event["payload"]["detail"]["run_id"]
        workspace_id = event["payload"]["detail"]["workspace_id"]

        if get_plan_changes(json_response):
            logger.info("Resource changes detected")
            fulfillment_output, fulfillment_pass, fulfillment_logs_link = get_iam_policy(json_response["resource_changes"], run_id, workspace_id)
        else:
            logger.info("No resource changes detected")
            fulfillment_output = "{} ERROR, {} SECURITY_WARNING, {} SUGGESTION, {} WARNING".format(0, 0, 0, 0)
            fulfillment_pass = "passed"
            fulfillment_logs_link = False
        
        logger.info("Summary : " + fulfillment_output)
        logger.info("Status : " + fulfillment_pass)
        logger.info("Logs : " + fulfillment_logs_link)

        return {
            "status": fulfillment_pass,
            "message": fulfillment_output,
            "link" : fulfillment_logs_link
        }
  
    except Exception as e:
        logger.exception("Run Task Fulfillment error: {}".format(e))
        raise

def get_plan_changes(plan_payload):
    if "resource_changes" in plan_payload:
        return True
    else:
        return False

def get_iam_policy(plan_output, run_id, workspace_id):
    ia2_error = 0
    ia2_security_warning = 0
    ia2_suggestion = 0
    ia2_warning = 0
    ia2_pass = "passed" #Only passed, failed or running are allowed.

    if LOG_GROUP_NAME:
        LOG_STREAM_NAME = workspace_id + "_" + run_id
        cwl_client.create_log_stream(
            logGroupName = LOG_GROUP_NAME,
            logStreamName = LOG_STREAM_NAME
        )
        SEQUENCE_TOKEN = cwl_client.put_log_events(
            logGroupName = LOG_GROUP_NAME,
            logStreamName = LOG_STREAM_NAME,
            logEvents = [ {
                'timestamp' : int(round(time.time() * 1000)),
                'message' : time.strftime('%Y-%m-%d %H:%M:%S') + " Start IAM Access Analyzer analysis for workspace: {} - run: {}".format(workspace_id, run_id,)
            }]
        )["nextSequenceToken"]
                        
    for resource in plan_output:        
        if resource["type"] in ["aws_iam_policy", "aws_iam_role_policy", "aws_iam_role"]:
            logger.info("Resource : {}".format(json.dumps(resource)))
            if resource["change"]["after"] != None:
                iam_policy = json.loads(resource["change"]["after"][TFPlanPolicyKey[resource["type"]].value])
                logger.info("Policy : {}".format(json.dumps(iam_policy)))

                ia2_response = validate_policy(json.dumps(iam_policy), IA2PolicyType[resource["type"]].value)
                logger.info("Response : {}".format(ia2_response["findings"]))

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
                        
                        if LOG_GROUP_NAME:
                            SEQUENCE_TOKEN = cwl_client.put_log_events(
                                logGroupName = LOG_GROUP_NAME,
                                logStreamName = LOG_STREAM_NAME,
                                logEvents = [ {
                                    'timestamp' : int(round(time.time() * 1000)),
                                    'message' : time.strftime('%Y-%m-%d %H:%M:%S') + " resource: {} ".format(resource["address"]) + json.dumps(finding)
                                }],
                                sequenceToken = SEQUENCE_TOKEN
                            )["nextSequenceToken"]
                else:
                    if LOG_GROUP_NAME:
                        SEQUENCE_TOKEN = cwl_client.put_log_events(
                            logGroupName = LOG_GROUP_NAME,
                            logStreamName = LOG_STREAM_NAME,
                            logEvents = [ {
                                'timestamp' : int(round(time.time() * 1000)),
                                'message' : time.strftime('%Y-%m-%d %H:%M:%S') + " resource: {} - no new findings".format(resource["address"]) 
                            }],
                            sequenceToken = SEQUENCE_TOKEN
                        )["nextSequenceToken"]
            else:
                logger.info("New policy is null / deleted")
                if LOG_GROUP_NAME:
                    SEQUENCE_TOKEN = cwl_client.put_log_events(
                        logGroupName = LOG_GROUP_NAME,
                        logStreamName = LOG_STREAM_NAME,
                        logEvents = [ {
                            'timestamp' : int(round(time.time() * 1000)),
                            'message' : time.strftime('%Y-%m-%d %H:%M:%S') + " resource: {} - policy is null / deleted" .format(resource["address"])
                        }],
                        sequenceToken = SEQUENCE_TOKEN
                    )["nextSequenceToken"]

    if LOG_GROUP_NAME:
        ia2_logs_link = "https://console.aws.amazon.com/cloudwatch/home?region={}#logEventViewer:group={};stream={}".format(
            os.environ["AWS_REGION"], LOG_GROUP_NAME, LOG_STREAM_NAME)
    else:
        ia2_logs_link = "https://console.aws.amazon.com"

    ia2_results = "{} ERROR, {} SECURITY_WARNING, {} SUGGESTION, {} WARNING".format(
        ia2_error, ia2_security_warning, ia2_suggestion, ia2_warning)

    if ia2_error + ia2_security_warning > 0:
        ia2_pass = "failed"

    return ia2_results, ia2_pass, ia2_logs_link

def validate_policy(policy_document, policy_type):
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