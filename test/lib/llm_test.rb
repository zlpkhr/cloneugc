require_relative "../../lib/llm"

class LLMProvidersMockTest < ActiveSupport::TestCase
  def setup
    @image_url = "http://example.com/image.jpg"
    @prompt = "Extract person attributes from the image."
    @schema = { "type" => "object" }
    @expected_result = { "name" => "John Doe", "age" => 30 }
    @mock = LLM::Providers::Mock.new(
      "analyze_image" => {
        [ @image_url, @prompt, @schema ] => @expected_result
      }
    )
  end

  def test_analyze_image_returns_expected_result
    result = @mock.analyze_image(@image_url, @prompt, @schema)
    assert_equal @expected_result, result
  end

  def test_analyze_image_raises_when_no_mock_response
    assert_raises(RuntimeError) do
      @mock.analyze_image("other_url", @prompt, @schema)
    end
  end
end
