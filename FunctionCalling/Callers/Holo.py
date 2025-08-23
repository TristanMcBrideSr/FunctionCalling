"""
HoloAI with Multiple Providers
But actions are called by the model based on the context.
Not activated by user input.
"""
import os
from dotenv import load_dotenv

from HoloAI import HoloAI

from Utils.SkillGraph import  SkillGraph


# Set These Environment Variables in your .env file or system environment variables
# PROVIDER=openai or google (default is openai)
# OPENAI_API_KEY=your_openai_api_key
# GEMINI_API_KEY=your_google_api_key
##-------------------------------------- NOTE --------------------------------------
# HoloAI supports OpenAI, Google, xAI, Anthropic, Groq.
# Make sure to add your api keys for the Provider(s) in the .env file or set them in your environment variables that you want to use.
# Add Provider models to the modelMap in AgentTool class.


load_dotenv()

holoAI = HoloAI()
graph = SkillGraph()

provider = os.getenv("PROVIDER", "openai").lower()

systemInstructions = "You are a helpful assistant."
skills = graph.getAgentCapabilities()
actions = graph.getAgentActions()


OPTION = 1  # Change to 2 if you want to use the controlled execution mode

def getModel() -> str:
    models = {
        "openai": "gpt-4.1",
        "google": "gemini-2.5-flash"
    }
    try:
        return models[provider]
    except KeyError:
        raise ValueError("Invalid provider: choose 'openai' or 'google'")


# ===================================================================================================================
# OPTION 1: Simple direct call — model decides skills & actions automatically
# Copy this function into your project if you want the simpler automatic mode.
# ===================================================================================================================
def processInput1(ctx: str, verbose: bool = False) -> str:
    completion = holoAI.HoloCompletion(
        model=getModel(),
        system=systemInstructions,
        input=ctx,
        skills=skills,
        actions=actions,
    )
    return completion or "No response generated."


# ===================================================================================================================
# OPTION 2: Controlled execution — you manage skills & actions manually
# Copy this function into your project if you want more control.
# ===================================================================================================================
def processInput2(ctx: str, verbose: bool = False) -> str:
    skillInstruct = graph.skillInstructions()
    calledSkills = holoAI.HoloCompletion(
        model=getModel(),
        system=skillInstruct,
        input=ctx,
    )

    results = None
    getActions = graph.getActions(calledSkills)
    if getActions:
        executed = graph.executeActions(actions, getActions)
        filtered = [str(r) for r in executed if r]
        if filtered:
            combined = "\n".join(filtered)
            if verbose:
                print(f"Combined Results:\n{combined}\n")
            results = f"Use these results from the actions called:\n{combined}"

    completion = holoAI.HoloCompletion(
        model=getModel(),
        system=systemInstructions,
        instructions=results,
        input=ctx,
    )
    return completion or "No response generated."

def processInput(ctx: str, verbose: bool = False) -> str:
    if OPTION == 1:
        return processInput1(ctx, verbose)
    elif OPTION == 2:
        return processInput2(ctx, verbose)
    else:
        raise ValueError("Invalid option selected. Choose 1 or 2.")


# if __name__ == "__main__":
#     # Example usage using a while loop to continuously process user input
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() in ["exit", "quit", "q"]:
#             print("Exiting...")
#             break
#         response = processInput(user_input, verbose=True)
#         print(f"Assistant: {response}")