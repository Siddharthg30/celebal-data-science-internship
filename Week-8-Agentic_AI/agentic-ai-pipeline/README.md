# Agentic AI Pipeline

An agentic AI pipeline that automatically routes user queries to the appropriate agent based on the type of task. The system supports data analysis, mathematical calculations, and general data science questions.

> **Note:** The pipeline architecture is designed to work with Gemini. For local development and testing, Ollama with `llama3.1:latest` is used to avoid Gemini API quota limitations. The agent architecture and workflow remain the same.

## Overview

The system follows a simple agentic workflow:

```text
User Query
    ↓
Planner
    ↓
Conditional Router
    ├── DATA → Data Agent → CSV Analysis Tool
    ├── MATH → Math Agent → Calculator Tool
    └── GENERAL → General Agent
    ↓
Retry Handling
    ↓
Final Response
```

The main goal is to demonstrate how multiple specialized agents and tools can work together instead of sending every query to a single agent.

## Features

* Query classification using a planner agent
* Conditional routing to specialized agents
* CSV data analysis
* Mathematical calculations
* General data science question answering
* Tool calling with AutoGen
* Retry handling for failed agent executions
* Query trajectory tracking
* Response-time measurement
* Completion-rate evaluation
* Sequential and parallel execution testing
* Streamlit interface
* Local testing with Ollama
* Gemini-compatible architecture

## Tech Stack

* Python
* AutoGen AgentChat
* Ollama
* Llama 3.1
* Pandas
* Streamlit
* python-dotenv
* CSV
* AsyncIO

### Production / API Model

The architecture is designed to support **Google Gemini** as the model client.

### Local Testing Model

For development and testing:

```text
Ollama
└── llama3.1:latest
```

This allows the project to be tested locally without depending on Gemini API request quotas.

## Project Structure

```text
agentic-ai-pipeline/
│
├── agents.py
├── tools.py
├── config.py
├── app.py
├── test_pipeline.py
├── agentic_ai_pipeline.ipynb
├── sales.csv
├── requirements.txt
├── .env
└── README.md
```

### File Description

| File                        | Purpose                                                      |
| --------------------------- | ------------------------------------------------------------ |
| `agents.py`                 | Defines planner, specialized agents, routing and retry logic |
| `tools.py`                  | Contains calculator and CSV analysis tools                   |
| `config.py`                 | Creates the model client                                     |
| `app.py`                    | Streamlit user interface                                     |
| `test_pipeline.py`          | Tests the complete pipeline from the terminal                |
| `agentic_ai_pipeline.ipynb` | Project demonstration, experiments and evaluation            |
| `sales.csv`                 | Sample dataset used for data-agent testing                   |
| `requirements.txt`          | Project dependencies                                         |
| `.env`                      | Environment configuration                                    |
| `README.md`                 | Project documentation                                        |

## Agents

### 1. Planner Agent

The planner identifies what type of query the user has entered.

It classifies queries into:

```text
DATA
MATH
GENERAL
```

For example:

```text
"Find the average sales from sales.csv"
→ DATA
```

```text
"Calculate 125 multiplied by 8"
→ MATH
```

```text
"What is overfitting in machine learning?"
→ GENERAL
```

### 2. Data Agent

The data agent handles questions related to CSV data.

It uses the `analyze_data` tool to perform operations such as:

* Average
* Sum
* Maximum
* Minimum

Example:

```text
Find the average sales from sales.csv
```

Result:

```text
1800.0
```

### 3. Math Agent

The math agent handles direct mathematical calculations.

It uses the calculator tool for operations such as:

* Addition
* Subtraction
* Multiplication
* Division

Example:

```text
Calculate 125 multiplied by 8
```

Result:

```text
1000.0
```

### 4. General Agent

The general agent handles questions that do not require a dataset or calculator.

Example:

```text
What is overfitting in machine learning?
```

It provides a natural-language explanation.

## Tools

### Calculator

The calculator accepts:

```python
calculator(operation, a, b)
```

Supported operations include:

```text
add
subtract
multiply
divide
```

Example:

```python
calculator("multiply", 125, 8)
```

Output:

```text
1000
```

### CSV Analysis

The data tool accepts:

```python
analyze_data(file_path, column, operation)
```

Example:

```python
analyze_data(
    "sales.csv",
    "sales",
    "average"
)
```

Output:

```text
1800.0
```

The tool also handles column names without requiring an exact case match.

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd agentic-ai-pipeline
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

## Ollama Setup

Install Ollama and make sure it is running.

Check the installed models:

```powershell
ollama list
```

The project currently uses:

```text
llama3.1:latest
```

If the model is not available:

```powershell
ollama pull llama3.1:latest
```

You can verify it with:

```powershell
ollama run llama3.1:latest
```

Exit the model with:

```text
/bye
```

## Configuration

The current local testing configuration is handled in `config.py`.

```python
from autogen_ext.models.ollama import OllamaChatCompletionClient


def get_model_client():
    return OllamaChatCompletionClient(
        model="llama3.1:latest"
    )
```

The architecture can later be switched to Gemini by changing the model client configuration without changing the overall agent workflow.

## Running the Pipeline

### Terminal Test

Run:

```powershell
python test_pipeline.py
```

Example output:

```text
Query: Find the average sales from sales.csv
Route: DATA
Answer: 1800.0

Query: Calculate 125 multiplied by 8
Route: MATH
Answer: 1000.0

Query: What is overfitting in machine learning?
Route: GENERAL
Answer: ...
```

## Running the Streamlit App

Start the application:

```powershell
streamlit run app.py
```

The application provides a simple interface where users can enter questions and see:

* Selected route
* Final answer
* Execution trajectory

Example:

```text
User Query
    ↓
Planner
    ↓
DATA
    ↓
Data Agent
    ↓
analyze_data()
    ↓
1800.0
```

## Notebook

The main project demonstration is available in:

```text
agentic_ai_pipeline.ipynb
```

The notebook contains:

1. Project introduction
2. Model configuration note
3. Agent imports
4. Data-agent testing
5. Math-agent testing
6. General-agent testing
7. Multiple-query testing
8. Completion-rate calculation
9. Response-time measurement
10. Sales statistics
11. Results table
12. Parallel execution testing
13. Sequential vs parallel comparison
14. Agent workflow
15. Final evaluation
16. Future improvements

## Evaluation

The pipeline was tested using three representative queries.

| Query Type               | Route   | Result                 |
| ------------------------ | ------- | ---------------------- |
| CSV average              | DATA    | 1800.0                 |
| Mathematical calculation | MATH    | 1000.0                 |
| ML concept               | GENERAL | Successful explanation |

The evaluation tracks:

* Completion Rate
* Average Response Time
* Number of Attempts
* Route Selection
* Execution Status

Example evaluation output:

```text
Completion Rate: 100.0%
Average Response Time: 8.24 seconds
```

Response time can vary depending on the local machine and model.

## Retry Handling

The pipeline includes retry handling for agent execution failures.

The trajectory records information such as:

```python
{
    "query": "...",
    "route": "DATA",
    "attempt": 1,
    "status": "success"
}
```

If an execution fails, the system can retry the agent before returning a failure response.

## Parallel Execution

The notebook also tests running independent queries concurrently using Python's `asyncio`.

This allows comparison between:

```text
Sequential execution
```

and:

```text
Parallel execution
```

The actual performance difference depends on the local model, hardware, and workload.

## Example Queries

### Data

```text
Find the average sales from sales.csv
```

```text
Find the maximum sales from sales.csv
```

```text
Find the minimum sales from sales.csv
```

### Math

```text
Calculate 125 multiplied by 8
```

```text
Calculate 500 divided by 5
```

### General

```text
What is overfitting in machine learning?
```

```text
What is the difference between supervised and unsupervised learning?
```

## Design Decisions

### Why multiple agents?

Different types of queries require different capabilities.

Instead of using one agent for everything, the system routes the query to a specialized agent.

This makes the workflow easier to understand and extend.

### Why tools?

Tools allow agents to perform deterministic operations.

For example, mathematical calculations and CSV statistics are better handled by Python functions than by asking an LLM to calculate the result itself.

### Why Ollama for testing?

The local Ollama model allows the complete agentic workflow to be tested without repeatedly consuming Gemini API quota.

The model can also be changed later while keeping the same overall architecture.

## Limitations

The current version has some limitations:

* Only a small number of query categories are supported.
* CSV analysis currently focuses on basic statistical operations.
* The planner depends on the language model for classification.
* Local LLM response time depends on available hardware.
* The current sample data uses a simple CSV file.
* Production deployment would require stronger error handling and security controls.

## Future Improvements

Possible improvements include:

* Support for multiple CSV files
* Automatic dataset selection
* More advanced data analysis
* SQL database tools
* Web search tools
* Better query classification
* Improved retry and fallback strategies
* RAG-based knowledge retrieval
* Persistent conversation memory
* More comprehensive evaluation datasets
* Agent observability and logging
* Gemini-based production deployment
* Docker-based deployment
* Authentication for the Streamlit application

## Conclusion

This project demonstrates a basic but extensible agentic AI architecture where a planner identifies the user's intent and routes the query to a specialized agent.

The current pipeline supports:

```text
Query Routing
      ↓
Specialized Agents
      ↓
Tool Execution
      ↓
Retry Handling
      ↓
Evaluation
      ↓
Final Response
```

The architecture is intentionally modular so additional agents, tools, models, and data sources can be added without redesigning the complete system.
