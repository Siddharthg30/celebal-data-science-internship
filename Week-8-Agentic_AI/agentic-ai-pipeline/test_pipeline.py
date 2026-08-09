import asyncio
from agents import run_agent


async def main():
    queries = [
        "Find the average sales from sales.csv",
        "Calculate 125 multiplied by 8",
        "What is overfitting in machine learning?"
    ]

    for query in queries:
        route, result, trajectory = await run_agent(query)

        print("Query:", query)
        print("Route:", route)

        if result:
            print("Answer:", result.messages[-1].content)
        else:
            print("Error:", trajectory["error"])

        print("Trajectory:", trajectory)
        print()


asyncio.run(main())