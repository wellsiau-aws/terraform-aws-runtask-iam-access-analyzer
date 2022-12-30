data "aws_region" "current" {
}

module "runtask_iam_access_analyzer" {
  source           = "../../" # set your Terraform Cloud workspace with Local execution mode to allow module reference like this
  tfc_org          = "wellsiau-org"
  aws_region       = "us-west-2"
  workspace_prefix = "aws"
  deploy_waf       = false
}
