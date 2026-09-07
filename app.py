import streamlit as st
from src.pipelines.pipelines import run_research_pipeline

st.title("🔎 Research Assistant")

topic = st.text_input("Enter a topic")

if st.button("Run"):
    with st.spinner("Working on it..."):
        state = run_research_pipeline(topic)

    st.header("Report")
    st.write(state["report"])

    st.header("Critic Feedback")
    st.write(state["feedback"])