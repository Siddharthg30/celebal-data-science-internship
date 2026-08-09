from autogen_agentchat.agents import AssistantAgent

from config import get_model_client
from tools import calculator, analyze_data


def create_agents():
    model_client = get_model_client()

    planner = AssistantAgent(
        name="planner",
        model_client=model_client,
        system_message="""
You are a query classifier.

Return only one category:

DATA - questions about CSV files, datasets, columns, rows, sales, averages from data, statistics from data, or data analysis.

MATH - direct mathematical calculations that do not require a dataset.

GENERAL - general questions about data science or machine learning.

Return only: DATA, MATH, or GENERAL.
"""
    )

    data_agent = AssistantAgent(
        name="data_agent",
        model_client=model_client,
        tools=[analyze_data],
        system_message="""
You analyze CSV data.

For sales.csv, use:
file_path = "sales.csv"
column = "sales"

Use analyze_data for calculations.
"""
    )

    math_agent = AssistantAgent(
        name="math_agent",
        model_client=model_client,
        tools=[calculator],
        system_message="""
You solve mathematical calculations.

Use the calculator tool.

For multiplication use operation='multiply'.
"""
    )

    general_agent = AssistantAgent(
        name="general_agent",
        model_client=model_client,
        system_message="""
You are a data science assistant.
Answer general questions clearly and simply.
"""
    )

    return planner, data_agent, math_agent, general_agent


async def run_agent(query, retries=2):
    planner, data_agent, math_agent, general_agent = create_agents()

    result = await planner.run(task=query)
    route = result.messages[-1].content.strip().upper()

    if route == "DATA":
        agent = data_agent
    elif route == "MATH":
        agent = math_agent
    else:
        agent = general_agent

    for attempt in range(retries + 1):
        try:
            result = await agent.run(task=query)

            trajectory = {
                "query": query,
                "route": route,
                "attempt": attempt + 1,
                "status": "success"
            }

            return route, result, trajectory

        except Exception as e:
            if attempt == retries:
                trajectory = {
                    "query": query,
                    "route": route,
                    "attempt": attempt + 1,
                    "status": "failed",
                    "error": str(e)
                }

                return route, None, trajectory