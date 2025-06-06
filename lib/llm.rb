require "json"

class Llm
  def initialize(provider)
    @provider = provider
  end

  def extract_person_attributes(image_url)
    prompt = "Extract person attributes from the image."
    schema = JSON.parse(File.read(File.join(__dir__, "llm", "schemas", "person_attributes.json")))

    @provider.analyze_image(image_url, prompt, schema)
  end
end
