terraform {

  cloud {
    # TODO: Change this to your Terraform Cloud org name.
    organization = "wellsiau-org"
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

provider "aws" { # for Cloudfront WAF only
  region = "us-east-1"
  alias  = "cloudfront_waf"
}

provider "tfe" {
}