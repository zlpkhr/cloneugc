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
  bucket = "cloneugc-media"
}

output "media_bucket_name" {
  value = aws_s3_bucket.media_bucket.bucket
}

resource "random_password" "db_password" {
  length  = 20
  special = true
}

resource "aws_db_parameter_group" "main" {
  name   = "cloneugc-db-params"
  family = "postgres17"

  parameter {
    name  = "rds.force_ssl"
    value = "0"
  }
}

resource "aws_db_instance" "main" {
  identifier              = "cloneugc-db"
  allocated_storage       = 20
  engine                  = "postgres"
  engine_version          = "17.5"
  instance_class          = "db.t4g.micro"
  username                = "cloneugc"
  password                = random_password.db_password.result
  backup_retention_period = 7
  parameter_group_name    = aws_db_parameter_group.main.name
}

resource "aws_elasticache_cluster" "main" {
  cluster_id           = "cloneugc-redis"
  engine               = "redis"
  engine_version       = "7.1"
  node_type            = "cache.t4g.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
}

output "rds_connection" {
  value = {
    username = aws_db_instance.main.username
    password = random_password.db_password.result
    host     = aws_db_instance.main.address
    port     = aws_db_instance.main.port
  }
  sensitive = true
}

output "redis_connection" {
  value = {
    host = aws_elasticache_cluster.main.cache_nodes[0].address
    port = aws_elasticache_cluster.main.cache_nodes[0].port
  }
}

resource "aws_iam_role" "apprunner_s3" {
  name = "apprunner-s3-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = [
          "build.apprunner.amazonaws.com",
          "tasks.apprunner.amazonaws.com"
        ]
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "apprunner_s3_fullaccess" {
  role       = aws_iam_role.apprunner_s3.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}
