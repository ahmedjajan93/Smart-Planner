# prompts/planner_prompt.py

from langchain.prompts import PromptTemplate

planner_prompt = PromptTemplate(
    input_variables=["goal"],
    template="""
You are an expert strategic planner. Your task is to create a detailed, multi-phase action plan to achieve the following goal:

🎯 Goal: {goal}

Instructions:
- Structure the plan into 3 to 5 major **phases**.
- Each phase should have 2 to 5 specific, actionable **tasks**.
- For each task, include:
    - A short, clear description
    - A relative **deadline** (e.g., "Week 1, Day 3")
    - Required **resources/tools** (if applicable)
- Use clear, concise language.

Return the plan as a **valid JSON** object in this format:

{{
  "phases": [
    {{
      "name": "Phase 1 Name",
      "tasks": [
        {{
          "task": "Description of task",
          "deadline": "Week 1, Day 3",
          "resources": "List of tools/resources"
        }},
        ...
      ]
    }},
    ...
  ]
}}
"""
)
