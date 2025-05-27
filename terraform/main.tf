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

resource "aws_route53_zone" "cloneugc_zone" {
  name = "cloneugc.com."
}

resource "aws_route53_record" "cloneugc_com" {
  zone_id = aws_route53_zone.cloneugc_zone.zone_id
  name    = "cloneugc.com"
  type    = "A"
  ttl     = 300
  records = [aws_instance.server.public_ip]
}

resource "aws_route53_record" "www_cloneugc_com" {
  zone_id = aws_route53_zone.cloneugc_zone.zone_id
  name    = "www.cloneugc.com"
  type    = "CNAME"
  ttl     = 300
  records = ["cloneugc.com"]
}

resource "random_password" "db_password" {
  length  = 32
  special = false
}

resource "aws_secretsmanager_secret" "db_password" {
  name = "cloneugc-db-password"
}

resource "aws_secretsmanager_secret_version" "db_password_version" {
  secret_id     = aws_secretsmanager_secret.db_password.id
  secret_string = random_password.db_password.result
}

resource "aws_security_group" "rds_sg" {
  name_prefix = "cloneugc-rds-sg-"
  description = "Allow PostgreSQL from app server"

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.server_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "cloneugc_db" {
  identifier             = "cloneugc-db"
  allocated_storage      = 20
  engine                 = "postgres"
  engine_version         = "17.5"
  instance_class         = "db.t3.micro"
  username               = "cloneugc"
  password               = random_password.db_password.result
  db_name                = "cloneugc"
  skip_final_snapshot    = false
  publicly_accessible    = false
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
}

output "rds_endpoint" {
  value       = aws_db_instance.cloneugc_db.endpoint
  description = "The endpoint of the RDS instance."
}

output "rds_secret_arn" {
  value       = aws_secretsmanager_secret.db_password.arn
  description = "The ARN of the RDS password secret in Secrets Manager."
}
