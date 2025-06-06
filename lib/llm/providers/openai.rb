require "openai"
require "json"

class Llm::Providers::Openai
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
