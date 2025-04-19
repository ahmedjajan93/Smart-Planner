import streamlit as st
from agent.plan_agent import build_plan_chain
from utils.mindmap import create_mindmap
import json
from PIL import Image
from agent.plan_agent import build_plan_chain
from dotenv import load_dotenv

# Streamlit setup
st.set_page_config(page_title="🧠 Smart Planner", layout="wide")
st.title("🧠 Smart Planner – From Goals to Actionable Plans")
# Input the API key from the sidebar
api_key = st.sidebar.text_input("🔐 Enter your OpenAI API key:", type="password")

# Input
goal = st.text_input("🎯 Enter your goal (e.g., 'Launch an online course')", "")
submit = st.button("🚀 Generate Plan")

if submit and goal:
    if api_key:
    
        with st.spinner("Generating actionable plan..."):
            
                plan = build_plan_chain(goal,api_key)
                if "error" in plan:
                    st.error("❌ Failed to parse plan. Please try again.")
                    st.text(plan.get("raw", ""))
                else:
                    st.session_state.plan = plan
        if plan:
            # Display plan
            st.subheader("📋 Action Plan")
            if "phases" in plan:
                    for i, phase in enumerate(plan["phases"]):
                        st.subheader(f"📌 {phase['name']}")
                        st.write("### Tasks")
                        for task in phase["tasks"]:
                            st.markdown(f"- **{task['task']}** (Deadline: {task['deadline']})\n  *Resources:* {task['resources']}")
                            

            # Mind Map
            st.subheader("🧠 Mind Map")
            mindmap_path = create_mindmap(plan)
            st.image(Image.open(mindmap_path), use_container_width=True)

        else:
            st.info("👈 Enter a goal and click 'Generate Plan' to get started.")
    else:
        st.warning("Please enter your OpenAI API key to continue.")
