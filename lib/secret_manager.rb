require "aws-sdk-secretsmanager"

# A simple client for fetching secrets from different providers.
#
# ## Usage
#
#   # In a Rails initializer (e.g., config/initializers/secret_manager.rb)
#
#   # For development/production with AWS
#   provider = SecretManager::Providers::AWS.new(region: ENV.fetch('AWS_REGION', 'us-east-1'))
#   SECRET_MANAGER = SecretManager.new(provider)
#
#   # For testing with the Mock provider
#   # provider = SecretManager::Providers::Mock.new(
#   #   secrets: { 'my/test/secret' => 'super_secret_value' }
#   # )
#   # SECRET_MANAGER = SecretManager.new(provider)
#
class SecretManager
  attr_reader :provider

  def initialize(provider)
    @provider = provider
  end

  # Fetches a secret's value as a plaintext string.
  def get_plaintext(secret_name)
    provider.get_plaintext(secret_name)
  end

  # --- Providers ---
  module Providers
    # AWS Secrets Manager provider.
    class AWS
      def initialize(options)
        region = options[:region]
        raise ArgumentError, "AWS region is required." unless region
        @aws_client = ::Aws::SecretsManager::Client.new(region: region)
        @logger = options[:logger]
      end

      def get_plaintext(secret_name)
        response = @aws_client.get_secret_value(secret_id: secret_name)
        response.secret_string
      rescue ::Aws::SecretsManager::Errors::ServiceError => e
        @logger&.error("Failed to fetch the secret '#{secret_name}': #{e.message}")
        nil
      end
    end

    # Mock provider for testing.
    class Mock
      def initialize(options)
        @secrets = options[:secrets] || {}
      end

      def get_plaintext(secret_name)
        @secrets[secret_name.to_s]
      end
    end
  end
end
