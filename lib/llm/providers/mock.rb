class Llm::Providers::Mock
  def initialize(responses)
    @responses = responses
  end

  def analyze_image(image_url, prompt, schema)
    result = @responses["analyze_image"][[ image_url, prompt, schema ]]
    raise "No mock response for analyze_image" if result.nil?
    result
  end
end
