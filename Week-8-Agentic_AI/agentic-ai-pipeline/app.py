import streamlit as st
import asyncio

from agents import run_agent


st.set_page_config(
    page_title="Agentic AI Pipeline",
    page_icon="🤖"
)


st.title("Agentic AI Pipeline")
st.write("Ask a question and let the agent choose the right route.")

examples = [
    "Find the average sales from sales.csv",
    "Calculate 125 multiplied by 8",
    "What is overfitting in machine learning?"
]

selected = st.selectbox("Try an example", [""] + examples)

query = st.text_input("Enter your query", value=selected)

if st.button("Run") and query:
    with st.spinner("Processing..."):
        route, result, trajectory = asyncio.run(run_agent(query))

    st.subheader("Route")
    st.write(route)

    st.subheader("Answer")

    if result:
        st.write(result.messages[-1].content)
    else:
        st.error(trajectory["error"])

    st.subheader("Trajectory")
    st.json(trajectory)