require "json"
require "openai"

class LLM
  def initialize(provider)
    @provider = provider
  end

  def extract_person_attributes(image_url)
    prompt = "Extract person attributes from the image."
    schema = JSON.parse(File.read(File.join(__dir__, "llm", "schemas", "person_attributes.json")))

    @provider.analyze_image(image_url, prompt, schema)
  end
end

module LLM::Providers
  class OpenAI
    def initialize(api_key)
      @oai_client = ::OpenAI::Client.new(access_token: api_key)
    end

    def analyze_image(image_url, prompt, schema)
      response = @oai_client.responses.create(parameters: {
        model: "gpt-4.1-nano",
        text: {
          format: {
            type: "json_schema",
            **schema
          }
        },
        input: [
          {
            role: "user",
            content: [
              {
                type: "input_image",
                image_url: image_url
              },
              {
                type: "input_text",
                text: prompt
              }
            ]
          }
        ],
        store: true
      }
      )

      JSON.parse(aggregate_output_text(response))
    end

    private

    def aggregate_output_text(response)
      texts = []

      outputs = response.dig("output") || []
      outputs.each do |output|
        if output["type"] == "message"
          output["content"].each do |content|
            if content["type"] == "output_text"
              texts << content["text"]
            end
          end
        end
      end

      texts.join
    end
  end

  class Mock
    def initialize(responses)
      @responses = responses
    end

    def analyze_image(image_url, prompt, schema)
      result = @responses["analyze_image"][[ image_url, prompt, schema ]]
      raise "No mock response for analyze_image" if result.nil?
      result
    end
  end
end
