# ==========================================================================
# SETUP TERRAFORM CLOUD
# ==========================================================================

terraform {

  cloud {
    # TODO: Change this to your Terraform Cloud org name.
    organization = "tfc-integration-sandbox"

    workspaces {
      name = "aws-iam-runtask-test"
    }
  }
}

# TODO: Change this to your Terraform Cloud org name.
data "tfe_organization" "org" {
  name = "tfc-integration-sandbox"
}

data "tfe_workspace" "workspace" {
  name         = "aws-iam-runtask-test"
  organization = data.tfe_organization.org.name
}

provider tfe {
}

# ==========================================================================
# CREATE RUN TASKS
# ==========================================================================

resource "tfe_organization_run_task" "aws-iam-analyzer" {
  organization = data.tfe_organization.org.name
  url          = var.runtask_eventbridge_url
  name         = var.runtask_name
  enabled      = true
  hmac_key     = var.runtask_hmac
  description  = var.runtask_description
}

# ==========================================================================
# ATTACH RUN TASKS
# ==========================================================================

resource "tfe_workspace_run_task" "aws-iam-analyzer-attach" {
  workspace_id      = data.tfe_workspace.workspace.id
  task_id           = tfe_organization_run_task.aws-iam-analyzer.id
  enforcement_level = var.runtask_enforcement_level
  stage             = var.runtask_stage
}

# ==========================================================================
# CREATE AN EC2 INSTANCE IN AWS (uncomment after first apply)
# ==========================================================================

# provider "aws" {
#   # TODO: Specify the region you like to use.
#   region = "us-east-2"
# }

# data "aws_ami" "amazon2" {
#   most_recent = true

#   filter {
#     name   = "name"
#     values = ["amzn2-ami-hvm-*-x86_64-ebs"]
#   }

#   owners = ["amazon"]
# }

# resource "aws_instance" "ec2" {
#   ami           = data.aws_ami.amazon2.id
#   instance_type = "t3.nano"
# }