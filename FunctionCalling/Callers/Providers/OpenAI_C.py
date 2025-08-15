import os
import json
import re
from dotenv import load_dotenv
from openai import OpenAI
from Utils.SkillGraph import SkillGraph

load_dotenv()
showLoadedTools = os.getenv('SHOW_LOADED_TOOLS', 'False') == 'True'
schemaType = "chat_completions"

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
    try:
        return skillGraph.executeTool(*args, **kwargs)
    except Exception as e:
        print(f"Error executing tool: {e}")


def getResponse(inputMessages, toolList):
    return gptClient.chat.completions.create(
        model="gpt-4o",
        messages=inputMessages,
        tools=toolList,
        tool_choice="auto"
    )

def processInput(ctx: str) -> str:
    systemMessage = formatMessage("system", systemPrompt)
    userMessage = formatMessage("user", ctx)
    messages = [systemMessage, userMessage]

    response = getResponse(messages, tools)
    assistantMessage = response.choices[0].message

    if getattr(assistantMessage, "tool_calls", None):
        for toolCall in assistantMessage.tool_calls:
            args = json.loads(toolCall.function.arguments)
            result = executeTool(toolCall.function.name, toolFunctions, args)

            messages.append({
                "role": "assistant",
                "content": None,
                "tool_calls": [toolCall]
            })
            messages.append({
                "role": "tool",
                "tool_call_id": toolCall.id,
                "content": str(result)
            })

        response2 = getResponse(messages, tools)
        return response2.choices[0].message.content
    return assistantMessage.content if assistantMessage.content else "No response generated."


# if __name__ == "__main__":
#     # Example usage using a while loop to continuously process user input
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() in ["exit", "quit", "q"]:
#             print("Exiting...")
#             break
#         response = processInput(user_input)
#         print(f"Assistant: {response}")