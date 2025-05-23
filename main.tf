terraform {
  backend "s3" {
    bucket       = "cloneugc-terraform-state"
    key          = "terraform.tfstate"
    region       = "us-east-1"
    use_lockfile = true
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "media_bucket" {
  bucket_prefix = "cloneugc-media-"

  tags = {
    Name = "cloneugc-media"
  }
}

output "media_bucket_name" {
  value       = aws_s3_bucket.media_bucket.bucket
  description = "The name of the media S3 bucket."
}
