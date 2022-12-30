terraform {

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