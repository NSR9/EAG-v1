import os
import subprocess
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda


# Step 1: Ask user for path to install repo
def get_install_path(state: dict) -> dict:
    path = input("📁 Enter the full path where you want to install the repo: ").strip()
    if not os.path.exists(path):
        os.makedirs(path)
        state["logs"].append(f"📁 Created directory: {path}")
    else:
        state["logs"].append(f"📁 Using existing directory: {path}")
    state["install_path"] = os.path.abspath(path)
    return state


# Step 2: Generate list of GitHub setup commands
def generate_setup_commands(state: dict) -> dict:
    repo_dir = os.path.join(state["install_path"], state["git_repo_url"].split("/")[-1])
    git_repo_url = state["git_repo_url"]
    state["commands"] = [
        f"mkdir -p {repo_dir}",
        f"cd {repo_dir}",
        f"git clone {git_repo_url} "
    ]
    state["logs"].append(f"⚙️ Generated {len(state['commands'])} setup commands.")
    return state


def execute_command(state: dict) -> dict:
    idx = state["current_step"]
    if idx >= len(state["commands"]):
        state["logs"].append("✅ All commands executed successfully.")
        return state

    command = state["commands"][idx]
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode().strip()
        state["logs"].append(f"✅ Command {idx + 1}: `{command}` succeeded.\nOutput: {output}")
    except subprocess.CalledProcessError as e:
        error = e.stderr.decode().strip()
        state["logs"].append(f"❌ Command {idx + 1}: `{command}` failed.\nError: {error}")
        state["success"] = False  # ⛔ stop further execution
        return state

    state["current_step"] += 1
    return state


# Step 4: Determine whether to continue or end
def check_next_step(state: dict) -> str:
    # Stop if we've run out of commands or had a failure
    if state["current_step"] >= len(state["commands"]) or not state.get("success", True):
        return END
    return "execute_command"


# Step 5: Build LangGraph
def build_graph():
    builder = StateGraph(dict)

    builder.add_node("get_install_path", RunnableLambda(get_install_path))
    builder.add_node("generate_setup_commands", RunnableLambda(generate_setup_commands))
    builder.add_node("execute_command", RunnableLambda(execute_command))

    builder.set_entry_point("get_install_path")
    builder.add_edge("get_install_path", "generate_setup_commands")
    builder.add_edge("generate_setup_commands", "execute_command")
    builder.add_conditional_edges("execute_command", check_next_step)

    return builder.compile()


# Step 6: Run the graph
if __name__ == "__main__":
        initial_state = {
        "git_repo_url":"https://github.com/crewAIInc/crewAI-examples/tree/main/marketing_strategy",    
        "commands": [],
        "current_step": 0,
        "success": True,  # ✅ allow loop to continue by default
        "logs": [],
        "install_path": None,
    }

        graph = build_graph()
        final_state = graph.invoke(initial_state)

        print("\n🧾 Final Output Log:")
        for log in final_state["logs"]:
            print(log)
