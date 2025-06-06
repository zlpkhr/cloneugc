require "aws-sdk-secretsmanager"

# A collection of providers for fetching secrets.
#
# ## Usage
#   # For AWS:
#   # SECRET_MANAGER = SecretManager::Providers::AWS.new(region: "us-east-1")
#
#   # For testing with the mock provider:
#   # SECRET_MANAGER = SecretManager::Providers::Mock.new(
#   #   secrets: { "my/test/secret" => "super_secret_value" }
#   # )
module SecretManager
  module Providers
    # AWS Secrets Manager provider.
    class AWS
      def initialize(options)
        @logger = options[:logger]
        @aws_client = options[:client]

        if @aws_client.nil?
          region = options[:region]
          raise ArgumentError, "Either a region or an AWS client must be provided." unless region
          @aws_client = ::Aws::SecretsManager::Client.new(region: region)
        end
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
