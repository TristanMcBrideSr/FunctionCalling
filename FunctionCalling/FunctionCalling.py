

import logging
import importlib

logging.basicConfig(
    level=logging.WARNING,
    format="[%(asctime)s] [%(levelname)s] [%(threadName)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

CHOICE_MAP = {
    1: "Basic",
    2: "Advanced",
    3: "HoloAI",
}

PROCESS_MAP = {
    "Basic":                   ("Callers.Basic",    "processInput"),
    "Advanced":                ("Callers.Advanced", "processInput"),
    "HoloAI":                  ("Callers.Holo",     "processInput"),
}

def selectFunction():
    print("\nFunction Calling Demo\n" + "-" * 30)
    print("Available function option types:")
    for num, desc in CHOICE_MAP.items():
        print(f"  {num}: {desc}")
    print("-" * 30)
    while True:
        try:
            userChoice = input("\nSelect function option by number (default: 1): ").strip()
            if not userChoice:
                userChoice = 1
            else:
                userChoice = int(userChoice)
            choiceStr = CHOICE_MAP[userChoice]
            modulePath, func_name = PROCESS_MAP[choiceStr]
            module = importlib.import_module(modulePath)
            fn = getattr(module, func_name)
            print(f"\n[Selected function option]: {choiceStr}")
            return fn, choiceStr
        except (ValueError, KeyError, ImportError) as e:
            print(f"Invalid choice or import error: {e}")

if __name__ == "__main__":
    processInput, functionName = selectFunction()
    print("-" * 30)
    while True:
        userInput = input("Enter your query (or ':switch' to change function option, Enter to exit):\n")
        if userInput.strip() == "":
            print("Goodbye!")
            break
        if userInput.strip().lower() == ":switch":
            processInput, functionName = selectFunction()
            print("-" * 30)
            continue
        print(f"\n[User Input]: {userInput}\n")
        try:
            response = processInput(userInput)
            if response:
                print(f"\nResponse: {response}")
            else:
                print("\nNo response generated.")
        except Exception as e:
            logging.exception("Error during processing:")


