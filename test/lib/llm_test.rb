require_relative "../../lib/llm"
require_relative "../../lib/secret_manager"

class LLMTest < ActiveSupport::TestCase
  def setup
    @secrets = ::SecretManager::Providers::AWS.new(
      region: "us-east-1"
    )
  end

  def test_analyze_image_returns_expected_result
    image_url = "http://example.com/image.jpg"
    prompt = "Extract person attributes from the image."
    schema = { "type" => "object" }
    expected_result = { "name" => "John Doe", "age" => 30 }
    mock = ::LLM::Providers::Mock.new(
      "analyze_image" => {
        [ image_url, prompt, schema ] => expected_result
      }
    )
    result = mock.analyze_image(image_url, prompt, schema)
    assert_equal expected_result, result
  end

  def test_analyze_image_raises_when_no_mock_response
    image_url = "http://example.com/image.jpg"
    prompt = "Extract person attributes from the image."
    schema = { "type" => "object" }
    mock = ::LLM::Providers::Mock.new(
      "analyze_image" => {
        [ image_url, prompt, schema ] => { "name" => "John Doe", "age" => 30 }
      }
    )
    assert_raises(RuntimeError) do
      mock.analyze_image("other_url", prompt, schema)
    end
  end

  def test_extract_person_attributes_with_mock
    image_url = "http://example.com/image.jpg"
    prompt = "Extract person attributes from the image."
    schema = JSON.parse(File.read(File.join(__dir__, "../fixtures/files/person_attributes.json")))
    expected_result = { "gender" => "male", "ethnicity" => "asian", "age_group" => "young_adult" }
    mock_provider = ::LLM::Providers::Mock.new(
      "analyze_image" => {
        [ image_url, prompt, schema ] => expected_result
      }
    )
    llm = ::LLM.new(mock_provider)
    result = llm.extract_person_attributes(image_url)
    assert_equal expected_result, result
  end

  def test_openai_provider_analyze_image
    api_key = @secrets.get_plaintext("openai-api-key")
    image_url = "https://upload.wikimedia.org/wikipedia/commons/5/52/Kassym-Jomart_Tokayev_in_January_2025_%28cropped%29.jpg"
    prompt = "Extract person attributes from the image."
    schema = JSON.parse(File.read(File.join(__dir__, "../fixtures/files/person_attributes.json")))

    provider = ::LLM::Providers::OpenAI.new(api_key)
    result = provider.analyze_image(image_url, prompt, schema)

    assert_includes schema["schema"]["properties"]["gender"]["enum"], result["gender"]
    assert_includes schema["schema"]["properties"]["ethnicity"]["enum"], result["ethnicity"]
    assert_includes schema["schema"]["properties"]["age_group"]["enum"], result["age_group"]
  end
end
