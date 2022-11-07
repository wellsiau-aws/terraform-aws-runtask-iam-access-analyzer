output "runtask_hmac" {
  value     = aws_secretsmanager_secret_version.runtask_hmac.secret_string
  sensitive = true
}

output "runtask_eventbridge_url" {
  value = aws_lambda_function_url.runtask_eventbridge.function_url
}