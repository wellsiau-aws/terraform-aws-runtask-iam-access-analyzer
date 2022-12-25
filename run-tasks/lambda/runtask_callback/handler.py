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
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode

logger = logging.getLogger()
if 'log_level' in os.environ:
    logger.setLevel(os.environ['log_level'])
    logger.info("Log level set to %s" % logger.getEffectiveLevel())
else:
    logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(json.dumps(event))
    try:
        endpoint = event["payload"]["detail"]["task_result_callback_url"]
        access_token = event["payload"]["detail"]["access_token"]
        headers = __build_standard_headers(access_token)
        payload = {
            "data": {
                "attributes": {
                    "status": event["payload"]["result"]["fulfillment"]["status"],
                    "message": event["payload"]["result"]["fulfillment"]["message"],
                    "url": event["payload"]["result"]["fulfillment"]["link"],
                },
                "type": "task-results",
            }
        }
        logger.info("Payload : {}".format(json.dumps(payload)))
        response = __patch(endpoint, headers, bytes(json.dumps(payload), encoding="utf-8"))
        logger.info("TFC response: {}".format(response))
        return "completed"
  
    except Exception as e:
        logger.exception("Run Task Callback error: {}".format(e))
        raise

def __build_standard_headers(api_token):
    return {
        "Authorization": "Bearer {}".format(api_token),
        "Content-type": "application/vnd.api+json",
    }
    
def __patch(endpoint, headers, payload):
    request = Request(endpoint, headers=headers or {}, data=payload, method = "PATCH")
    try:
        with urlopen(request, timeout=10) as response:
            return response.read(), response
    except HTTPError as error:
        logger.error(error.status, error.reason)
    except URLError as error:
        logger.error(error.reason)
    except TimeoutError:
        logger.error("Request timed out")
    