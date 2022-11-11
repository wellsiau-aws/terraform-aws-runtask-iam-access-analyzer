terraform {

  cloud {
    # TODO: Change this to your Terraform Cloud org name.
    organization = "<enter your org name here>"

    # TODO: Change this to your Terraform Cloud workspace name.
    workspaces {
      name = "aws-event-bridge"
    }
  }

  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "4.38.0"
    }
  }
}

provider "aws" {
  # Configuration options
  region = "us-west-2"
}