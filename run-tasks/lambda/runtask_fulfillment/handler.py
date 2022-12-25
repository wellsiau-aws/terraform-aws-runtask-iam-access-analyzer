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
from collections import Counter

session = boto3.Session()
ia2_client = session.client('accessanalyzer')
cwl_client = session.client('logs')
logger = logging.getLogger()

class IA2PolicyType(Enum):
    aws_iam_policy = "IDENTITY_POLICY"
    aws_iam_role_policy = "IDENTITY_POLICY"
    aws_iam_role = "RESOURCE_POLICY"
    aws_organizations_policy = "SERVICE_CONTROL_POLICY"
    aws_kms_key = "RESOURCE_POLICY"

class TFPlanPolicyKey(Enum):
    aws_iam_policy = "policy"
    aws_iam_role_policy = "policy"
    aws_iam_role = "assume_role_policy"
    aws_organizations_policy = "content"
    aws_kms_key = "policy"

if "log_level" in os.environ:
    logger.setLevel(os.environ["log_level"])
    logger.info("Log level set to %s" % logger.getEffectiveLevel())
else:
    logger.setLevel(logging.INFO)

if "SUPPORTED_POLICY_DOCUMENT" in os.environ:
    SUPPORTED_POLICY_DOCUMENT = os.environ["SUPPORTED_POLICY_DOCUMENT"]
else:
    SUPPORTED_POLICY_DOCUMENT = ["aws_iam_policy", "aws_iam_role_policy", "aws_iam_role", "aws_kms_key", "aws_organizations_policy"]

if "CW_LOG_GROUP_NAME" in os.environ:
    LOG_GROUP_NAME = os.environ["CW_LOG_GROUP_NAME"]
    LOG_STREAM_NAME = ""
    SEQUENCE_TOKEN = ""
else: # disable logging if environment variable is not set
    LOG_GROUP_NAME = False

def lambda_handler(event, context):
    logger.info(json.dumps(event))
    try:
        # Get plan output from Terraform Cloud
        endpoint = event["payload"]["detail"]["plan_json_api_url"]
        access_token = event["payload"]["detail"]["access_token"]
        headers = __build_standard_headers(access_token)
        response, response_raw = __get(endpoint, headers)
        json_response = json.loads(response.decode("utf-8"))
        logger.debug("Headers : {}".format(response_raw.headers))
        logger.debug("JSON Response : {}".format(json.dumps(json_response)))

        # Get workspace and run task metadata
        run_id = event["payload"]["detail"]["run_id"]
        workspace_id = event["payload"]["detail"]["workspace_id"]
        
        # Initialize log
        global LOG_STREAM_NAME
        LOG_STREAM_NAME = workspace_id + "_" + run_id
        log_helper(LOG_GROUP_NAME, LOG_STREAM_NAME, 
            "Start IAM Access Analyzer analysis for workspace: {} - run: {}".format(workspace_id, run_id)
        )
        
        if get_plan_changes(json_response): # Check if there are any changes in plan output
            logger.info("Resource changes detected")
            total_ia2_violation_count = ia2_handler(json_response["resource_changes"]) # analyze and calculate number of violations
            fulfillment_response = fulfillment_response_helper(total_ia2_violation_count, skip_log = False) # generate response
        else:
            logger.info("No resource changes detected")
            fulfillment_response = fulfillment_response_helper(total_ia2_violation_count = {}, skip_log = True, override_message = "No resource changes detected", overrise_status = "passed") # override response
        
        return fulfillment_response
  
    except Exception as e: # run-task must return response despite of exception
        logger.exception("Run Task Fulfillment error: {}".format(e))
        fulfillment_response = fulfillment_response_helper(total_ia2_violation_count = {}, skip_log = True, override_message = "Run Task IAM Access Analyzer failed to complete successfully", override_status = "failed") # override response
        return fulfillment_response

def get_plan_changes(plan_payload):
    if "resource_changes" in plan_payload:
        return True
    else:
        return False

def ia2_handler(plan_resource_changes):
    total_ia2_violation_count = {
        "ERROR" : 0,
        "SECURITY_WARNING" : 0,
        "SUGGESTION" : 0,
        "WARNING" : 0
    }

    for resource in plan_resource_changes: # look for resource changes and match the supported policy document
        if resource["type"] in SUPPORTED_POLICY_DOCUMENT:
            logger.info("Resource : {}".format(json.dumps(resource)))
            ia2_violation_count = analyze_resource_policy_changes(resource) # get the policy difference per resource
            if ia2_violation_count: # calculate total violation count 
                total_counter = Counter(total_ia2_violation_count)
                total_counter.update(Counter(ia2_violation_count)) # add new violation to existing counter
                total_ia2_violation_count = dict(total_counter)
        else:
            logger.info("Resource type : {} is not supported".format(resource["type"]))
    
    return total_ia2_violation_count

def analyze_resource_policy_changes(resource):
    if "create" in resource["change"]["actions"]: # skip any deleted resources
        if TFPlanPolicyKey[resource["type"]].value in resource["change"]["after"]: # ensure that the policy is available in plan output
    
            iam_policy = json.loads(resource["change"]["after"][TFPlanPolicyKey[resource["type"]].value]) # take the new changed policy document
            logger.info("Policy : {}".format(json.dumps(iam_policy)))
    
            ia2_response = validate_policy(json.dumps(iam_policy), IA2PolicyType[resource["type"]].value) # run IAM Access analyzer validation
            logger.info("Response : {}".format(ia2_response["findings"]))

            ia2_violation_count = get_iam_policy_violation_count(resource, ia2_response) # calculate any IA2 violations
            return ia2_violation_count
            
        elif TFPlanPolicyKey[resource["type"]].value in resource["change"]["after_unknown"] and resource["change"]["after_unknown"][TFPlanPolicyKey[resource["type"]].value] == True: # missing computed values is not supported
            logger.info("Unsupported policy due to missing computed values")
            log_helper(LOG_GROUP_NAME, LOG_STREAM_NAME, "resource: {} - unsupported policy due to missing computed values" .format(resource["address"]))
            
    elif "delete" in resource["change"]["actions"]:
        logger.info("New policy is null / deleted")
        log_helper(LOG_GROUP_NAME, LOG_STREAM_NAME, "resource: {} - policy is null / deleted" .format(resource["address"]))
    
    else:
        logger.error("Unknown / unsupported action")
        raise
    
def get_iam_policy_violation_count(resource, ia2_response):
    ia2_violation_count = {
        "ERROR" : 0,
        "SECURITY_WARNING" : 0,
        "SUGGESTION" : 0,
        "WARNING" : 0
    }

    if len(ia2_response["findings"]) > 0: # calculate violation if there's any findings
        for finding in ia2_response["findings"]:
            ia2_violation_count[finding["findingType"]] += 1 
            log_helper(LOG_GROUP_NAME, LOG_STREAM_NAME, "resource: {} ".format(resource["address"]) + json.dumps(finding))
    else:
        log_helper(LOG_GROUP_NAME, LOG_STREAM_NAME, "resource: {} - no new findings".format(resource["address"]) )
    
    logger.info("Findings : {}".format(ia2_violation_count))
    return ia2_violation_count

def validate_policy(policy_document, policy_type): # call IAM access analyzer to validate policy
    response = ia2_client.validate_policy(
        policyDocument=policy_document,
        policyType=policy_type
    )
    return response

def log_helper(log_group_name, log_stream_name, log_message): # helper function to write RunTask results to dedicated cloudwatch log group
    if log_group_name: # true if CW log group name is specified
        global SEQUENCE_TOKEN
        try:
            SEQUENCE_TOKEN = log_writer(log_group_name, log_stream_name, log_message, SEQUENCE_TOKEN)["nextSequenceToken"]
        except:
            cwl_client.create_log_stream(logGroupName = log_group_name,logStreamName = log_stream_name)
            SEQUENCE_TOKEN = log_writer(log_group_name, log_stream_name, log_message)["nextSequenceToken"]

def log_writer(log_group_name, log_stream_name, log_message, sequence_token = False): # writer to CloudWatch log stream based on sequence token
    if sequence_token: # if token exist, append to the previous token stream
        response = cwl_client.put_log_events(
            logGroupName = log_group_name,
            logStreamName = log_stream_name,
            logEvents = [{
                'timestamp' : int(round(time.time() * 1000)),
                'message' : time.strftime('%Y-%m-%d %H:%M:%S') + ": " + log_message
            }],
            sequenceToken = sequence_token
        )
    else: # new log stream, no token exist
        response = cwl_client.put_log_events(
            logGroupName = log_group_name,
            logStreamName = log_stream_name,
            logEvents = [{
                'timestamp' : int(round(time.time() * 1000)),
                'message' : time.strftime('%Y-%m-%d %H:%M:%S') + ": " + log_message
            }]
        )
    return response

def fulfillment_response_helper(total_ia2_violation_count, skip_log = False, override_message = False, override_status = False): # helper function to send response to callback step function

    # Return message
    if not override_message:
        fulfillment_output = "{} ERROR, {} SECURITY_WARNING, {} SUGGESTION, {} WARNING".format(
            total_ia2_violation_count["ERROR"], total_ia2_violation_count["SECURITY_WARNING"], total_ia2_violation_count["SUGGESTION"], total_ia2_violation_count["WARNING"])
    else:
        fulfillment_output = override_message
    logger.info("Summary : " + fulfillment_output)

    # Hyperlink to CloudWatch log
    if not skip_log:
        if LOG_GROUP_NAME:
            fulfillment_logs_link = "https://console.aws.amazon.com/cloudwatch/home?region={}#logEventViewer:group={};stream={}".format(os.environ["AWS_REGION"], LOG_GROUP_NAME, LOG_STREAM_NAME)
        else:
            fulfillment_logs_link = "https://console.aws.amazon.com"
        logger.info("Logs : " + fulfillment_logs_link)
    else:
        fulfillment_logs_link = False

    # Run Tasks status
    if not override_status:
        if total_ia2_violation_count["ERROR"] + total_ia2_violation_count["SECURITY_WARNING"] > 0:
            fulfillment_status = "failed"
        else:
            fulfillment_status = "passed"
    else:
        fulfillment_status = override_status
    logger.info("Status : " + fulfillment_status)
    
    return {
        "status": fulfillment_status,
        "message": fulfillment_output,
        "link" : fulfillment_logs_link
    }

def __build_standard_headers(api_token): # TFC API header
    return {
        "Authorization": "Bearer {}".format(api_token),
        "Content-type": "application/vnd.api+json",
    }
    
def __get(endpoint, headers): # HTTP request helper function
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