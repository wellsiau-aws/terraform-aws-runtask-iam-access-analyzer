locals {
  lambda_managed_policies     = [data.aws_iam_policy.AWSLambdaBasicExecutionRole.arn]
  lambda_reserved_concurrency = 100
  lambda_default_timeout      = 30
  lambda_python_runtime       = "python3.8"
  cloudwatch_log_group_name   = "/hashicorp/terraform/runtask/iam-access-analyzer/"
}