terraform {

  cloud {
    # TODO: Change this to your Terraform Cloud org name.
    organization = "<your tfc organization>"
    workspaces {
      tags = ["app:aws-event-bridge"]
    }
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.38.0"
    }

    tfe = {
      version = "~>0.38.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

provider "tfe" {
}