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
from time import sleep

tfc_org = os.environ['TFC_ORG'];

logger = logging.getLogger()
if 'log_level' in os.environ:
    logger.setLevel(os.environ['log_level'])
    logger.info("Log level set to %s" % logger.getEffectiveLevel())
else:
    logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # todo:
    # validate request: https://www.terraform.io/cloud-docs/integrations/run-tasks#securing-your-run-task
    # send OK
    logger.info(json.dumps(event))
    try:
      if event["payload"]["detail"]["organization_name"] == tfc_org:
        return "verified"
    except Exception as e:
        logger.exception("Run Task Request error: {}".format(e))
        raise
