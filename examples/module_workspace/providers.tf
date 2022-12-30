terraform {

  cloud {
    # TODO: Change this to your Terraform Cloud org name.
    organization = "wellsiau-org"
    workspaces {
      tags = ["app:aws-access-analyzer"]
    }
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 3.73.0"
    }

    tfe = {
      version = "~>0.38.0"
    }
  }
}

provider "aws" {
  region = "us-west-2"
}