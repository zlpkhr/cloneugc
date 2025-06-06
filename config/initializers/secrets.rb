require "secret_manager"

Secrets = SecretManager::Providers::AWS.new(
  region: "us-east-1",
  logger: Rails.logger
)
