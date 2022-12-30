locals {
  lambda_managed_policies     = [data.aws_iam_policy.AWSLambdaBasicExecutionRole.arn]
  lambda_reserved_concurrency = 100
  lambda_default_timeout      = 30
  lambda_python_runtime       = "python3.9"
  cloudwatch_log_group_name   = var.cloudwatch_log_group_name
  waf_deployment              = var.deploy_waf ? 1 : 0
  waf_rate_limit              = 100
}