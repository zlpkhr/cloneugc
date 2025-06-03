import json

from django.conf import settings
from openai import OpenAI

oai_client = OpenAI(api_key=settings.OPENAI_API_KEY)


def format_sonic_text(text: str) -> str:
    res = oai_client.responses.create(
        model="gpt-4o-mini-2024-07-18",
        instructions='Prepare user-submitted scripts for audio generation according to Cartesia\'s Sonic-2 model text formatting best practices. Convert the input script into a JSON format for optimal audio synthesis.\n\nTake into account that users may not be familiar with the best practices and may not explicitly indicate emotions or intentions. It\'s crucial to infer these from the submitted script where possible and make necessary formatting changes for improved audio generation quality.\n\n# Steps\n\n1. **Analyze the Script**: Review the provided script to understand the intended emotions and context.\n2. **Apply Formatting Best Practices**: Implement the best practices from the Sonic-2 model, including punctuation, pauses, language matching, question emphasis, and correct formatting rules for URLs and quotes.\n3. **Optimize for Pronunciation**: Address any potential pronunciation issues, especially for domain-specific or ambiguous words.\n4. **Prepare the JSON Output**: Structure the modified text in a JSON format with the key `preparedScript`.\n\n# Output Format\n\nThe final output must be a JSON object structured as follows:\n\n```json\n{ "preparedScript": "formatted and improved text" }\n```\n\nEnsure that the text is styled according to the requirements mentioned in the best practices.\n\n# Examples\n\n- **Input**: Script: "Hello user  can you confirm the date 2023-04-20"\n  \n  **Reasoning**:\n  - Add punctuation for clarity.\n  - Format the date correctly.\n  \n  **Output**:\n  ```json\n  { "preparedScript": "Hello, user. Can you confirm the date 04/20/2023?" }\n  ```\n\n- **Input**: Script: "visit our website at www cartesia ai"\n  \n  **Reasoning**:\n  - Use "dot" for easier pronunciation.\n  - Remove unneeded spaces around the URL components.\n  \n  **Output**:\n  ```json\n  { "preparedScript": "Visit our website at cartesia dot ai" }\n  ```\n\n# Notes\n\n- When uncertain about the user\'s intention, make reasonable assumptions to improve clarity and delivery.\n- Ensure the text adheres to the guidelines for optimal performance with the Sonic-2 model.\n- Refer to the Cartesia documentation for any updates or specific nuances in formatting.\n\n# Cartesia Documentation\n\n## Formatting Text for Sonic-2\n\n1. **Use appropriate punctuation.** Add punctuation where appropriate and at the end of each transcript whenever possible.\n2. **Use dates in MM/DD/YYYY form.** For example, 04/20/2023.\n3. **Insert pauses.** To insert pauses, insert "-" or use [break tags](/build-with-cartesia/formatting-text-for-sonic-2/inserting-breaks-pauses) where you need the pause. These tags are considered 1 character and do not need to be separated with adjacent text using a space -- to save credits you can remove spaces around break tags.\n4. **Match the voice to the language.** Each voice has a language that it works best with. You can use the playground to quickly understand which voices are most appropriate for a language.\n5. **Stream in inputs for contiguous audio.** Use [continuations](/build-with-cartesia/capability-guides/stream-inputs-using-continuations) if generating audio that should sound contiguous in separate chunks.\n6. **Specify [custom pronunciations](/build-with-cartesia/capability-guides/specify-custom-pronunciations) for domain-specific or ambiguous words.** You may want to do this for proper nouns and trademarks, as well as for words that are spelled the same but pronounced differently, like the city of Nice and the adjective "nice."\n7. **Use two question marks to emphasize questions.** For example, "Are you here??" vs. "Are you here?"\n8. **Avoid using quotation marks.** (Unless you intend to refer to a quote.)\n9. **Use a space between a URL or email and a question mark.** Otherwise, the question mark will be read out. For example, write `Did you send the email to support@cartesia.ai ?` instead of `Did you send the email to support@cartesia.ai?`.\n10. **Use "dot" instead of "." in URLs.** For example, write "cartesia dot ai" instead of "cartesia.ai" for better pronunciation.',
        text={
            "format": {
                "type": "json_schema",
                "name": "audio_generation_script",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "preparedScript": {
                            "type": "string",
                            "description": "Formatted and improved text based on the user's submitted script for optimal audio synthesis.",
                        }
                    },
                    "required": ["preparedScript"],
                    "additionalProperties": False,
                },
            }
        },
        input=f"Script: {text}",
        store=True,
    )

    return json.loads(res.output_text).get("preparedScript")
