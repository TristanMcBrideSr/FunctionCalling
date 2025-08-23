
---

# FunctionCalling

**FunctionCalling** is a modular Python framework for building, managing, and deploying basic or advanced AI function-calling systems.
It enables orchestration of specialized function-calling operations powered by multiple providers (like OpenAI and Google), with flexible skill and tool integration—all from a simple interactive console.

---

## Features

* **Multiple Function Styles:**

  * **Options 1-2:** Switch between basic and advanced function calling (No Vendor Lock). Set your provider (`openai` or `google` etc) in the `.env` file.
  * **Options 3-5:** Use OpenAI and Google GenAI function calling directly.
* **Extensible Skills & Tools:** Easily add or customize callable functions and integrations.
* **API-Driven Intelligence:** Integrates with OpenAI and Google GenAI for responses.
* **Dynamic Option Selection:** Change function types in real time using a terminal prompt.
* **Environment Configuration:** Secure API management using `.env`.

---

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/TristanMcBrideSr/FunctionCalling.git
   cd FunctionCalling
   ```

2. **Install Python dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

3. **Set up your environment variables:**

   * Create a `.env` file in the project root.
   * Add your API keys and configuration as needed (see below).

---

## Quick Start

To launch the interactive function calling demo, run:

```sh
python FunctionCalling/FunctionCalling.py
```

### You will see:

```
Function Calling Demo
------------------------------
Available function option types:
  1: Basic
  2: Advanced
  3: HoloAI

------------------------------
Select option by number (default: 1):
```

* **Options 1 and 2** are vendor-neutral. Set your provider in the `.env` file (e.g., `PROVIDER=openai` or `PROVIDER=google`).
* Enter a number to select a function option type.
* Enter your query for processing.
* Type `:switch` to change option types at any time.
* Press Enter on an empty line to exit.

#### Example Session

```
Enter your query (or ':switch' to change option, Enter to exit):
What's the weather in New York?

[User Input]: What's the weather in New York?

<function output here>

Enter your query (or ':switch' to change option, Enter to exit):
:switch
...
```

---

## Project Structure

```
FunctionCalling/
│
├── Callers/              # Function orchestration modules
│   ├── Providers/        # Provider-specific callers
│   ├── Advanced.py
│   └── Basic.py
├── Skills/               # Function skills: date, time, weather, etc.
├── Tools/                # Function tools: date, time, weather, etc.
├── Utils/                # Utility modules: skill graph, schemas, etc.
├── FunctionCalling.py    # Interactive function calling launcher
└── requirements.txt
```

---

## Environment Variables

Configure your `.env` file with the required keys. For example:

```
GROQ_API_KEY=Please Visit https://groq.com to get an api key
OPENAI_API_KEY=Please Visit https://openai.com to get an api key
GEMINI_API_KEY=Please Visit https://cloud.google.com to get an api key
ANTHROPIC_API_KEY=Please Visit https://www.anthropic.com to get an api key
XAI_API_KEY=Please Visit https://xaia.ai to get an api key
PROVIDER=openai   # or 'google', 'anthropic', 'groq', 'xai'
```

---

## Requirements

* Python 3.10+
* Install all dependencies in `requirements.txt`:

  ```
  HoloAI
  ```

---

## Extending the Framework

* **Add new skills:** Create new modules in `Skills/` or `Tools/` and they will automatically be registered in the skill graph.
* **Skills are for options 1-2:** Basic and Advanced options can use any skill in the `Skills/` directory.
* **Tools are for options 3-5:** OpenAI and Google GenAI options can use any tool in the `Tools/` directory.

---

## Contributing

Pull requests are welcome!
For major changes, please open an issue first to discuss your proposal.

---

## License

This project is licensed under the [Apache License, Version 2.0](LICENSE).
Copyright 2025 Tristan McBride Sr.

You may use, modify, and distribute this software under the terms of the license.
Please just give credit to the original authors.

If you like this project, consider supporting it by starring the repository or contributing improvements!

---

**Authors:**
- Tristan McBride Sr.
- Sybil