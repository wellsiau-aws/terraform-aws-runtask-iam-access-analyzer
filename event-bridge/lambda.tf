################# RunTask EventBridge ##################
resource "aws_lambda_function" "runtask_eventbridge" {
  function_name    = "${var.name_prefix}-runtask-eventbridge"
  description      = "Terraform Cloud Run Task - EventBridge handler"
  role             = aws_iam_role.runtask_eventbridge.arn
  source_code_hash = data.archive_file.runtask_eventbridge.output_base64sha256
  filename         = data.archive_file.runtask_eventbridge.output_path
  handler          = "handler.lambda_handler"
  runtime          = local.lambda_python_runtime
  timeout          = local.lambda_default_timeout
  environment {
    variables = {
      TFC_HMAC_SECRET_ARN = aws_secretsmanager_secret.runtask_hmac.arn
      EVENT_BUS_NAME      = var.event_bus_name
    }
  }
  tracing_config {
    mode = "Active"
  }
  reserved_concurrent_executions = local.lambda_reserved_concurrency
  #checkov:skip=CKV_AWS_116:not using DLQ
  #checkov:skip=CKV_AWS_117:VPC is not required
  #checkov:skip=CKV_AWS_173:no sensitive info inside environment variable
  #checkov:skip=CKV_AWS_272:skip code-signing
}

resource "aws_lambda_function_url" "runtask_eventbridge" {
  function_name      = aws_lambda_function.runtask_eventbridge.function_name
  authorization_type = "NONE"
  #checkov:skip=CKV_AWS_258:auth set to none, validation hmac inside the lambda code
}

resource "aws_cloudwatch_log_group" "runtask_eventbridge" {
  name              = "/aws/lambda/${aws_lambda_function.runtask_eventbridge.function_name}"
  retention_in_days = var.cloudwatch_log_group_retention
}



################# RunTask Request ##################
resource "aws_lambda_function" "runtask_request" {
  function_name    = "${var.name_prefix}-runtask-request"
  description      = "Terraform Cloud Run Task - Request handler"
  role             = aws_iam_role.runtask_request.arn
  source_code_hash = data.archive_file.runtask_request.output_base64sha256
  filename         = data.archive_file.runtask_request.output_path
  handler          = "handler.lambda_handler"
  runtime          = local.lambda_python_runtime
  timeout          = local.lambda_default_timeout
  tracing_config {
    mode = "Active"
  }
  reserved_concurrent_executions = local.lambda_reserved_concurrency
  environment {
    variables = {
      TFC_ORG = "${var.tfc_org}"
    }
  }
  #checkov:skip=CKV_AWS_116:not using DLQ
  #checkov:skip=CKV_AWS_117:VPC is not required
  #checkov:skip=CKV_AWS_173:no sensitive info inside environment variable
  #checkov:skip=CKV_AWS_272:skip code-signing
}

resource "aws_cloudwatch_log_group" "runtask_request" {
  name              = "/aws/lambda/${aws_lambda_function.runtask_request.function_name}"
  retention_in_days = var.cloudwatch_log_group_retention
}



################# RunTask Callback ##################
resource "aws_lambda_function" "runtask_callback" {
  function_name    = "${var.name_prefix}-runtask-callback"
  description      = "Terraform Cloud Run Task - Callback handler"
  role             = aws_iam_role.runtask_callback.arn
  source_code_hash = data.archive_file.runtask_callback.output_base64sha256
  filename         = data.archive_file.runtask_callback.output_path
  handler          = "handler.lambda_handler"
  runtime          = local.lambda_python_runtime
  timeout          = local.lambda_default_timeout
  tracing_config {
    mode = "Active"
  }
  reserved_concurrent_executions = local.lambda_reserved_concurrency
  #checkov:skip=CKV_AWS_116:not using DLQ
  #checkov:skip=CKV_AWS_117:VPC is not required
  #checkov:skip=CKV_AWS_272:skip code-signing
}

resource "aws_cloudwatch_log_group" "runtask_callback" {
  name              = "/aws/lambda/${aws_lambda_function.runtask_callback.function_name}"
  retention_in_days = var.cloudwatch_log_group_retention
}



################# RunTask Fulfillment ##################
resource "aws_lambda_function" "runtask_fulfillment" {
  function_name    = "${var.name_prefix}-runtask-fulfillment"
  description      = "Terraform Cloud Run Task - Fulfillment handler"
  role             = aws_iam_role.runtask_fulfillment.arn
  source_code_hash = data.archive_file.runtask_fulfillment.output_base64sha256
  filename         = data.archive_file.runtask_fulfillment.output_path
  handler          = "handler.lambda_handler"
  runtime          = local.lambda_python_runtime
  timeout          = local.lambda_default_timeout
  tracing_config {
    mode = "Active"
  }
  reserved_concurrent_executions = local.lambda_reserved_concurrency
  #checkov:skip=CKV_AWS_116:not using DLQ
  #checkov:skip=CKV_AWS_117:VPC is not required
  #checkov:skip=CKV_AWS_272:skip code-signing
}

resource "aws_cloudwatch_log_group" "runtask_fulfillment" {
  name              = "/aws/lambda/${aws_lambda_function.runtask_fulfillment.function_name}"
  retention_in_days = var.cloudwatch_log_group_retention
}