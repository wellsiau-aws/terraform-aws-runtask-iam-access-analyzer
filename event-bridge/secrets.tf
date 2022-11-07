resource "random_uuid" "runtask_hmac" {}

resource "aws_secretsmanager_secret" "runtask_hmac" {
  name  = "${var.name_prefix}-runtask-hmac"
  #checkov:skip=CKV_AWS_149:use AWS managed key for demo purpose
}

resource "aws_secretsmanager_secret_version" "runtask_hmac" {
  secret_id     = aws_secretsmanager_secret.runtask_hmac.id
  secret_string = random_uuid.runtask_hmac.result
}
