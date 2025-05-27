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

resource "aws_security_group" "server_sg" {
  name_prefix = "cloneugc-server-sg-"
  description = "Allow SSH, HTTP, and HTTPS"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "server" {
  ami                         = "ami-084568db4383264d4"
  instance_type               = "t3.medium"
  vpc_security_group_ids      = [aws_security_group.server_sg.id]
  associate_public_ip_address = true
  key_name                    = "zlpkhr@Azamats-MacBook-Pro"

  root_block_device {
    volume_type = "gp3"
    volume_size = 40
  }
}

output "server_public_ip" {
  value       = aws_instance.server.public_ip
  description = "The public IP of the server."
}
