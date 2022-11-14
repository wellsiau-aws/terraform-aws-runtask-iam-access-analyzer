# ==========================================================================
# ATTACH RUN TASKS
# ==========================================================================

resource "tfe_workspace_run_task" "aws-iam-analyzer-attach" {
  count             = var.flag_attach_runtask ? 1 : 0
  workspace_id      = data.tfe_workspace.workspace.id
  task_id           = var.runtask_id
  enforcement_level = var.runtask_enforcement_level
  stage             = var.runtask_stage
}

# ==========================================================================
# CREATE SIMPLE IAM POLICY
# ==========================================================================

resource "aws_iam_policy" "simple_invalid_iam_policy" {
  # the sample policy below contains invalid iam permissions (syntax-wise)
  count  = var.flag_deploy_invalid_resource ? 1 : 0
  name   = "${var.name_prefix}-simple-invalid-iam-policy"
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroups",
        "logs:CreateLogStreams",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_policy" "simple_valid_iam_policy" {
  name   = "${var.name_prefix}-simple-valid-iam-policy"
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*",
      "Effect": "Allow"
    }
  ]
}
EOF
}