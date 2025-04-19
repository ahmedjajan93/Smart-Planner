from graphviz import Digraph
import tempfile
import os
import uuid

def create_mindmap(plan: dict) -> str:
    dot = Digraph(comment="Mind Map")
    dot.attr(rankdir='LR')  # left to right layout

    root_id = "Goal"
    dot.node(root_id, "🎯 Goal")

    if "phases" not in plan:
        dot.node("Error", "No valid phases found")
        return dot.pipe(format='png')

    for i, phase in enumerate(plan["phases"]):
        phase_id = f"phase_{i}"
        dot.node(phase_id, f"📂 {phase['name']}")
        dot.edge(root_id, phase_id)

        for j, task in enumerate(phase.get("tasks", [])):
            task_id = f"{phase_id}_task_{j}"
            task_label = f"📝 {task['task']}\n🗓 {task['deadline']}"
            dot.node(task_id, task_label)
            dot.edge(phase_id, task_id)

    # Use a unique filename in a temp directory
    tmp_dir = tempfile.gettempdir()
    filename = f"mindmap_{uuid.uuid4().hex}"
    output_path = os.path.join(tmp_dir, filename)

    # Render the mind map (will create output_path.png)
    dot.render(filename=output_path, format='png', cleanup=True)

    return output_path + ".png"
