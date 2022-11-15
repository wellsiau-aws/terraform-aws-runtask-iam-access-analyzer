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

# ==========================================================================
# CREATE SIMPLE IAM ROLE AND ATTACH POLICY
# ==========================================================================

resource "aws_iam_role" "simple_invalid_iam_role" {
  count              = var.flag_deploy_invalid_resource ? 1 : 0
  name               = "${var.name_prefix}-simple-invalid-iam-role"
  assume_role_policy = templatefile("${path.module}/iam/trust-policies/lambda.tpl", { none = "none" })
}

resource "aws_iam_role_policy" "simple_invalid_iam_role_policy" {
  count = var.flag_deploy_invalid_resource ? 1 : 0
  name  = "${var.name_prefix}-simple-invalid-iam-role-policy"
  role  = aws_iam_role.simple_invalid_iam_role[count.index].id
  policy = templatefile("${path.module}/iam/role-policies/simple-invalid-iam-role-policy.tpl", {
    data_aws_region     = data.aws_region.current_region.name
    data_aws_account_id = data.aws_caller_identity.current_account.account_id
    data_aws_partition  = data.aws_partition.current_partition.partition
    var_name_prefix     = var.name_prefix
  })
}