terraform {
  required_version = ">= 1.2.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  backend "s3" {
    region       = "us-east-1"
    bucket       = "cloneugc-terraform-state"
    key          = "terraform.tfstate"
    use_lockfile = true
  }
}

provider "aws" {
  alias  = "eu-west-3"
  region = "eu-west-3"
}

resource "aws_s3_bucket" "dev_bucket" {
  provider      = aws.eu-west-3
  bucket_prefix = "cloneugc-dev-"
}

output "dev_bucket_name" {
  value = aws_s3_bucket.dev_bucket.bucket
}
