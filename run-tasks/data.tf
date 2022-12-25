data "aws_region" "current_region" {}

data "aws_caller_identity" "current_account" {}

data "aws_partition" "current_partition" {}

data "aws_iam_policy" "AWSLambdaBasicExecutionRole" {
  name = "AWSLambdaBasicExecutionRole"
}

data "archive_file" "runtask_eventbridge" {
  type        = "zip"
  source_dir  = "${path.module}/lambda/runtask_eventbridge/build/site-packages/"
  output_path = "${path.module}/lambda/runtask_eventbridge.zip"
}

data "archive_file" "runtask_request" {
  type        = "zip"
  source_dir  = "${path.module}/lambda/runtask_request/build/site-packages/"
  output_path = "${path.module}/lambda/runtask_request.zip"
}

data "archive_file" "runtask_fulfillment" {
  type        = "zip"
  source_dir  = "${path.module}/lambda/runtask_fulfillment/build/site-packages/"
  output_path = "${path.module}/lambda/runtask_fulfillment.zip"
}

data "archive_file" "runtask_callback" {
  type        = "zip"
  source_dir  = "${path.module}/lambda/runtask_callback/build/site-packages/"
  output_path = "${path.module}/lambda/runtask_callback.zip"
}