# ==========================================================================
# SETUP TERRAFORM CLOUD
# ==========================================================================

terraform {

  cloud {
    # TODO: Change this to your Terraform Cloud org name.
    organization = "tfc-integration-sandbox"

    workspaces {
      name = "test-aws-runtask"
    }
  }

  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "4.28.0"
    }
    tfe = {
      source = "hashicorp/tfe"
      version = "0.38.0"
    }
  }
}

# TODO: Change this to your Terraform Cloud org name.
data "tfe_organization" "org" {
  name = "tfc-integration-sandbox"
}

data "tfe_workspace" "workspace" {
  name         = "test-aws-runtask"
  organization = data.tfe_organization.org.name
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
# CREATE AN EC2 INSTANCE IN AWS
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

# Uncomment after the first apply (that creates and attaches the run task to this workspace)
# resource "aws_instance" "ec2" {
#   ami           = data.aws_ami.amazon2.id
#   instance_type = "t3.nano"
# }