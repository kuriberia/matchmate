# Note: The openai-python library support for Azure OpenAI is in preview.
import os
import openai
openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_key = os.getenv("OPENAI_API_KEY")


def chatgpt(message_history):

    response = openai.ChatCompletion.create(
        engine=os.getenv("OPENAI_ENGINE"),
        messages=message_history,
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )

    assistant_message = response.choices[0].message.content

    message_history.append({"role": "assistant", "content": assistant_message})
