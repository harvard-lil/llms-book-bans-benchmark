"""
Tests prompt against LLMs at all available temperatures and saves to CSV.
"""
import os
import json
import datetime

import requests
from dotenv import load_dotenv
import google.generativeai as palm
import openai

from const import DATA_PATH, PROMPT, ROUNDS_PER_COMBINATION

load_dotenv()


def ask_gpt():
    """
    Runs the prompt against gpt3.5-turbo and gpt-4 and saves output to CSV.
    Temperatures: 0.0 to 1.0.
    The OPENAI_API_KEY environment variable needs to be defined.
    """
    # Do we have an API key?
    if "OPENAI_API_KEY" not in os.environ:
        raise Exception("OPENAI_API_KEY not provided.")

    openai.api_key = os.environ["OPENAI_API_KEY"]

    for model in ["gpt-3.5-turbo", "gpt-4"]:
        for temperature in range(0, 10 + 1):
            temperature = temperature / 10

            for i in range(0, ROUNDS_PER_COMBINATION):
                print(f"Prompting {model} at temperature {temperature}")

                chat_completion = openai.ChatCompletion.create(
                    model=model,
                    temperature=temperature,
                    messages=[{"role": "user", "content": PROMPT}],
                )

                response = chat_completion.choices[0].message.content
                response_to_csv(model, PROMPT, temperature, response)


def ask_palm():
    """
    Runs the prompt against Palm2 (text-bison-001) and saves output to CSV.
    Temperatures: 0.0 to 1.0.
    The PALM_API_KEY environment variable needs to be defined.

    Note: The Palm2 API sometimes refuses to produce a response, if it is deemed "unsafe".
    For the purpose of this experiment, we are not disabling this safety mechanism.
    """
    # Do we have an API key?
    if "PALM_API_KEY" not in os.environ:
        raise Exception("PALM_API_KEY not provided.")

    palm.configure(api_key=os.environ["PALM_API_KEY"])

    for temperature in range(0, 10 + 1):
        temperature = temperature / 10

        for i in range(0, ROUNDS_PER_COMBINATION):
            print(f"Prompting Palm2 at temperature {temperature}")

            attempts = 0
            while attempts < 5:
                response = palm.generate_text(
                    model="models/text-bison-001", prompt=PROMPT, temperature=temperature
                )

                # The response might have been discarded for safety reasons.
                # i.e: BlockedReason.OTHER: 2
                # We only keep responses that Google deem safe.
                if not response.result:
                    attempts += 1
                    print("The Palm API did not return a response (blocked)")
                    print(response)
                    print("-- Will try again")

                else:
                    response_to_csv("palm2", PROMPT, temperature, response.result)
                    break


def ask_llama2():
    """
    Runs the prompt against Llama2 (13B-chat and 70B-chat) and saves output to CSV.
    Temperatures: 0.0 to 1.0.
    The OLLAMA_API_ENDPOINT environment variable needs to be defined.
    """
    # Do we have an OLLAMA API endpoint?
    if "OLLAMA_API_ENDPOINT" not in os.environ:
        raise Exception("OLLAMA_API_ENDPOINT not provided.")

    for model in ["llama2:13b", "llama2:70b"]:
        for temperature in range(0, 10 + 1):
            temperature = temperature / 10

            for i in range(0, ROUNDS_PER_COMBINATION):
                print(f"Prompting {model} at temperature {temperature}")

                response = ""

                raw_response = requests.post(
                    os.environ["OLLAMA_API_ENDPOINT"],
                    json={
                        "model": model,
                        "prompt": PROMPT,
                        "options": {"temperature": temperature},
                    },
                )

                for chunk in raw_response.text.split("\n"):
                    if not chunk:
                        continue

                    parsed_chunk = json.loads(chunk)
                    if "response" in parsed_chunk and parsed_chunk["done"] is False:
                        response += parsed_chunk["response"]

                response_to_csv(model, PROMPT, temperature, response)


# TODO: Replace with Python's built-in CSV module.
def response_to_csv(model: str, prompt: str, temperature: str, response: str):
    """
    Saves an LLM response to CSV. Creates file if it does not exist.
    """
    filepath = os.path.join(DATA_PATH, f"{model.replace(':', '-')}.csv")

    # Check if file exists: if not, create it with headings
    if not os.path.exists(filepath):
        with open(filepath, "w") as file:
            file.write("timestamp,model,prompt,temperature,response\n")

    # Append to file
    with open(filepath, "a") as file:
        line = datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + ","
        line += f"{model},"
        line += '"' + prompt.replace('"', '""') + '",'
        line += f"{temperature},"
        line += '"' + response.replace('"', '""') + '"\n'

        file.write(line)


if __name__ == "__main__":
    ask_llama2()
    ask_gpt()
    ask_palm()
