import os
import json
import re
from dotenv import load_dotenv
from openai import OpenAI
from Utils.SkillGraph import SkillGraph

load_dotenv()
showLoadedTools = os.getenv('SHOW_LOADED_TOOLS', 'False') == 'True'
schemaType = "responses"

# toolSchemaManager = JsonSchemaManager()
# toolFunctions = toolSchemaManager.getToolFunctions()
# tools = [toolSchemaManager.buildToolSchema(f, schemaType) for f in toolFunctions.values()]
# systemPrompt = "You are a helpful assistant that can call functions to get information."
# gptClient = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
skillGraph = SkillGraph()
tools, toolFunctions = skillGraph.getJsonTools(schemaType)
#print(f"Discovered tools: {tools}")
systemPrompt = "You are a helpful assistant that can call functions to get information."
gptClient = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def formatMessage(role, content):
    return skillGraph.handleJsonFormat(role, content)

def executeTool(*args, **kwargs):
    return skillGraph.executeTool(*args, **kwargs)

def getResponse(inputMessages: list, toolList):
    return gptClient.responses.create(
        model="gpt-4.1",
        input=inputMessages,
        tools=toolList,
    )

def processInput(ctx: str) -> str:
    systemMessage = formatMessage("system", systemPrompt)
    userMessage = formatMessage("user", ctx)
    messages = [systemMessage, userMessage]

    response = getResponse(messages, tools)
    functionCalls = []
    functionOutputs = []
    #print(f"Response: {response}")
    for toolCall in response.output:
        if toolCall.type != "function_call":
            continue

        functionCalls.append({
            "type": "function_call",
            "call_id": toolCall.call_id,
            "name": toolCall.name,
            "arguments": toolCall.arguments
        })

        args = json.loads(toolCall.arguments)
        result = executeTool(toolCall.name, toolFunctions, args)

        functionOutputs.append({
            "type": "function_call_output",
            "call_id": toolCall.call_id,
            "output": str(result)
        })

    messages.extend(functionCalls)
    messages.extend(functionOutputs)
    response2 = getResponse(messages, tools)
    return response2.output_text.strip()


# if __name__ == "__main__":
#     # Example usage using a while loop to continuously process user input
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() in ["exit", "quit", "q"]:
#             print("Exiting...")
#             break
#         response = processInput(user_input)
#         print(f"Assistant: {response}")