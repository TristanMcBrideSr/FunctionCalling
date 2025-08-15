"""
HoloAI with Multiple Providers
But actions are activated by user input.
Not by the model based on the context.
"""
import os
from dotenv import load_dotenv

from openai import OpenAI
from google import genai
from google.genai import types
# from anthropic import anthropic
# from ollama import ollama

from Utils.SkillGraph import  SkillGraph


# Set These Environment Variables in your .env file or system environment variables
# PROVIDER=openai or google (default is openai)
# OPENAI_API_KEY=your_openai_api_key
# GOOGLE_API_KEY=your_google_api_key


load_dotenv()
graph = SkillGraph()

provider = os.getenv("PROVIDER", "openai").lower()

gptClient = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
genClient = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
# anthropicClient = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
# ollamaClient = ollama.Client()

systemInstructions = "You are a helpful assistant that can call functions to get information."
skillInstructions = graph.skillInstructions()

## If you want to use OpenAI's chat completions, uncomment the following function and comment out the `getResponseOpenai` function below it.
# def getResponseOpenai(inputMessages: list) -> str:
#     return gptClient.chat.completions.create(
#         model="gpt-4.1-mini",
#         messages=inputMessages,
#     ).choices[0].message.content

def getResponseOpenai(inputMessages: list) -> str:
    return gptClient.responses.create(
        model="gpt-4.1",
        input=inputMessages,
    ).output_text

def getResponseGoogle(ctx: str) -> str:
    model = "gemini-2.5-flash"
    contents = [graph.handleTypedFormat("user", ctx)]
    generateContentConfig = types.GenerateContentConfig(
        response_mime_type="text/plain"
    )
    return genClient.models.generate_content(
        model=model,
        contents=contents,
        config=generateContentConfig,
    ).text

# def runAnthropic(ctx: str) -> str:
#     return anthropicClient.messages.create(
#         model="claude-3-opus-20240229",
#         max_tokens=1024,
#         messages=ctx
#     ).content[0].text

# def runOllama(ctx: str) -> str:
#     response = ollama.chat(
#         model="llama3",
#         messages=ctx
#     )
#     return response["message"]["content"]

def getResponse(*args, **kwargs):
    if provider == "openai":
        return getResponseOpenai(*args, **kwargs)
    elif provider == "google":
        return getResponseGoogle(*args, **kwargs)
    # elif provider == "anthropic":
    #     return runAnthropic(*args, **kwargs)
    # elif provider == "ollama":
    #     return runOllama(*args, **kwargs)
    else:
        raise ValueError("Invalid provider: choose 'openai' or 'google'")

def callAction(ctx: str, verbose: bool = False):
    # pass the context to the getUserActions in the SkillGraph
    actions = graph.getUserActions(ctx)
    if verbose:
        print(f"Actions result: {actions}")
    return actions if actions else None

def processInput(ctx: str, verbose: bool = False) -> str:
    if provider == "google":
        messages = []
        actionMessage = callAction(ctx, verbose)
        if actionMessage:
            messages.append(actionMessage if isinstance(actionMessage, str) else actionMessage["content"])
        messages.append(ctx)
        fullMessage = "\n".join(messages)
        completion = getResponse(fullMessage)
    else:
        system = graph.handleJsonFormat("system", systemInstructions)
        user = graph.handleJsonFormat("user", ctx)
        messages = [system, user]
        actionMessage = callAction(ctx, verbose)
        if actionMessage:
            messages.append(graph.handleJsonFormat("user", actionMessage))
        completion = getResponse(messages)

    return completion if completion else "No response generated."


# if __name__ == "__main__":
#     # Example usage using a while loop to continuously process user input
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() in ["exit", "quit", "q"]:
#             print("Exiting...")
#             break
#         response = processInput(user_input, verbose=True)
#         print(f"Assistant: {response}")