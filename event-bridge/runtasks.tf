resource "tfe_organization_run_task" "aws_iam_analyzer" {
  organization = var.tfc_org
  url          = trim(aws_lambda_function_url.runtask_eventbridge.function_url, "/")
  name         = "${var.name_prefix}-runtask"
  enabled      = true
  hmac_key     = aws_secretsmanager_secret_version.runtask_hmac.secret_string
  description  = "Demo runtask integration with AWS IAM Access Analyzer"
}
