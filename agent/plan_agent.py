# agent/plan_agent.py
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from prompts.planner_prompts import planner_prompt
from langchain.chains import LLMChain
import json
import re
import os


def clean_llm_output(output: str) -> str:
    # Remove markdown code block if present
    output = re.sub(r"```(json)?", "", output)
    output = output.replace("```", "").strip()
    return output

def build_plan_chain(goal: str,api_key: str) -> dict:
    os.environ["OPENAI_API_KEY"] = api_key
    llm = ChatOpenAI(
        model="gpt-4-turbo",
        temperature=0.7,
        max_tokens=1024
    )

    chain = LLMChain(prompt=planner_prompt, llm=llm)
    raw_result = chain.run(goal)

    try:
        cleaned = clean_llm_output(raw_result)
        plan = json.loads(cleaned)
    except Exception as e:
        try:
            json_str = re.search(r"\{.*\}", raw_result, re.DOTALL).group().strip()
            plan = json.loads(json_str)
        except Exception as e2:
            plan = {
                "error": f"Initial parsing failed: {e}; fallback also failed: {e2}",
                "raw": raw_result
            }

    if isinstance(plan, dict):
        plan["llm_model"] = "gpt-4-turbo"

    return plan
