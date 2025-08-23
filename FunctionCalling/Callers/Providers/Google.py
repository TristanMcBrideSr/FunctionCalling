import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from Utils.SkillGraph import SkillGraph

load_dotenv()
apiKey = os.getenv("GEMINI_API_KEY")
genClient = genai.Client(api_key=apiKey)

# schemaManager = TypedSchemaManager()
# toolFunctions = schemaManager.getToolFunctions()
# toolSchemas = schemaManager.getToolSchemas()
skillGraph = SkillGraph()
tools, toolFunctions = skillGraph.getTypedTools()

def formatMessage(role, content):
    return skillGraph.handleTypedFormat(role, content)

def executeTool(*args, **kwargs):
    return skillGraph.executeTool(*args, **kwargs)

def getResponse(contents, tool):
    generateContentConfig = types.GenerateContentConfig(
        tools=tool,
        response_mime_type="text/plain",
    )
    return [genClient.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=generateContentConfig,
    )]

def buildResponsePayload(funcName, result):
    if isinstance(result, dict):
        return result
    return {funcName: result}

def processInput(ctx: str) -> str:
    msg = formatMessage("user", ctx)
    messages = [msg] if not isinstance(msg, list) else msg
    while True:
        chunk = getResponse(messages, tools)[0]
        if chunk.function_calls:
            for funcCall in chunk.function_calls:
                funcName = funcCall.name
                funcArgs = funcCall.args or {}
                result = executeTool(funcName, toolFunctions, funcArgs)
                responsePayload = buildResponsePayload(funcName, result)
                functionResponse = types.Content(
                    role="function",
                    parts=[types.Part.from_function_response(
                        name=funcName,
                        response=responsePayload
                    )]
                )
                messages.append(functionResponse)
            continue
        if chunk.text:
            return chunk.text
        break
    return "No response from model."


# if __name__ == "__main__":
#     # Example usage using a while loop to continuously process user input
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() in ["exit", "quit", "q"]:
#             print("Exiting...")
#             break
#         response = processInput(user_input)
#         print(f"Assistant: {response}")