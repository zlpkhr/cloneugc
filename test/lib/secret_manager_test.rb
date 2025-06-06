require "test_helper"
require "secret_manager"
require "aws-sdk-secretsmanager"

class SecretManagerTest < ActiveSupport::TestCase
  test "Mock provider should return the secret value" do
    secrets = { "my/test/secret" => "super_secret_value" }
    secret_manager = SecretManager::Providers::Mock.new(secrets: secrets)

    assert_equal "super_secret_value", secret_manager.get_plaintext("my/test/secret")
  end

  test "Mock provider should return nil for an unknown secret" do
    secrets = { "my/test/secret" => "super_secret_value" }
    secret_manager = SecretManager::Providers::Mock.new(secrets: secrets)

    assert_nil secret_manager.get_plaintext("unknown/secret")
  end

  test "AWS provider should fetch a secret" do
    aws_client_stub = Aws::SecretsManager::Client.new(stub_responses: true)
    aws_client_stub.stub_responses(
      :get_secret_value,
      { secret_string: "aws_secret_value" }
    )

    secret_manager = SecretManager::Providers::AWS.new(client: aws_client_stub)
    assert_equal "aws_secret_value", secret_manager.get_plaintext("aws/secret")
  end

  test "AWS provider should return nil when a service error occurs" do
    aws_client_stub = Aws::SecretsManager::Client.new(stub_responses: true)
    aws_client_stub.stub_responses(
      :get_secret_value,
      "ServiceError"
    )

    secret_manager = SecretManager::Providers::AWS.new(client: aws_client_stub)
    assert_nil secret_manager.get_plaintext("aws/secret")
  end
end
