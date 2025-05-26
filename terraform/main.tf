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
  region = "us-east-1"
}

resource "aws_s3_bucket" "media_bucket" {
  bucket_prefix = "cloneugc-media-"
  force_destroy = true
}

output "media_bucket_name" {
  value       = aws_s3_bucket.media_bucket.bucket
  description = "The name of the media S3 bucket."
}

resource "aws_sqs_queue" "celery_queue" {
  name_prefix                = "cloneugc-celery-"
  visibility_timeout_seconds = 3600
}

output "celery_queue_url" {
  value       = aws_sqs_queue.celery_queue.url
  description = "The URL of the created SQS queue for Celery."
}
