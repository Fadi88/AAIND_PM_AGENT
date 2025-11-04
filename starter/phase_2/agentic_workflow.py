# agentic_workflow.py

# TODO: 1 - Import the following agents: ActionPlanningAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, RoutingAgent from the workflow_agents.base_agents module
from workflow_agents.base_agents import (
    ActionPlanningAgent,
    KnowledgeAugmentedPromptAgent,
    EvaluationAgent,
    RoutingAgent,
)

import os

# TODO: 2 - Load the OpenAI key into a variable called openai_api_key
openai_api_key = os.getenv("OPENAI_API_KEY")

# load the product spec
# TODO: 3 - Load the product spec document Product-Spec-Email-Router.txt into a variable called product_spec
try:
    with open(
        "starter/phase_2/Product-Spec-Email-Router.txt", "r", encoding="utf-8"
    ) as f:
        product_spec = f.read()
except FileNotFoundError:
    print("Error: Product spec file not found. Please check the file path.")
    product_spec = ""  # Set to empty string to avoid downstream errors

# Instantiate all the agents

# Action Planning Agent
knowledge_action_planning = (
    "Stories are defined from a product spec by identifying a "
    "persona, an action, and a desired outcome for each story. "
    "Each story represents a specific functionality of the product "
    "described in the specification. \n"
    "Features are defined by grouping related user stories. \n"
    "Tasks are defined for each story and represent the engineering "
    "work required to develop the product. \n"
    "A development Plan for a product contains all these components"
)
# TODO: 4 - Instantiate an action_planning_agent using the 'knowledge_action_planning'
action_planning_agent = ActionPlanningAgent(
    openai_api_key=openai_api_key, knowledge=knowledge_action_planning
)

# Product Manager - Knowledge Augmented Prompt Agent
persona_product_manager = "You are a Product Manager, you are responsible for defining the user stories for a product."
knowledge_product_manager = (
    "Stories are defined by writing sentences with a persona, an action, and a desired outcome. "
    "The sentences always start with: As a "
    "Write several stories for the product spec below, where the personas are the different users of the product. "
    # TODO: 5 - Complete this knowledge string by appending the product_spec loaded in TODO 3
    f"\n--- PRODUCT SPEC ---\n{product_spec}"
)
# TODO: 6 - Instantiate a product_manager_knowledge_agent using 'persona_product_manager' and the completed 'knowledge_product_manager'
product_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key=openai_api_key,
    persona=persona_product_manager,
    knowledge=knowledge_product_manager,
)
# Product Manager - Evaluation Agent
# TODO: 7 - Define the persona and evaluation criteria for a Product Manager evaluation agent and instantiate it as product_manager_evaluation_agent. This agent will evaluate the product_manager_knowledge_agent.
persona_product_manager_eval = (
    "You are an evaluation agent that checks the answers of other worker agents."
)
evaluation_criteria_pm = (
    "The answer must be a list of user stories. "
    "Each story must strictly follow the format: 'As a [type of user], I want [an action or feature] so that [benefit/value].'"
)

product_manager_evaluation_agent = EvaluationAgent(
    openai_api_key=openai_api_key,
    persona=persona_product_manager_eval,
    evaluation_criteria=evaluation_criteria_pm,
    worker_agent=product_manager_knowledge_agent,
    max_interactions=10,
)

# Program Manager - Knowledge Augmented Prompt Agent
persona_program_manager = "You are a Program Manager, you are responsible for defining the features for a product."
knowledge_program_manager = (
    "Features of a product are defined by organizing similar user stories into cohesive groups.\n"
    "Each feature must include: Feature Name, Description, Key Functionality, and User Benefit.\n"
    "Use the actual user stories from Step 1 and the product spec below to generate concrete features for the Email Router product.\n"
    "Focus on components such as: email ingestion, LLM-based classification, RAG system, routing logic, and monitoring dashboard.\n"
    f"\n--- PRODUCT SPEC ---\n{product_spec}"
)
# Instantiate a program_manager_knowledge_agent using 'persona_program_manager' and 'knowledge_program_manager'
program_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key=openai_api_key,
    persona=persona_program_manager,
    knowledge=knowledge_program_manager,
)

# Program Manager - Evaluation Agent
persona_program_manager_eval = (
    "You are an evaluation agent that checks the answers of other worker agents."
)

# TODO: 8 - Instantiate a program_manager_evaluation_agent using 'persona_program_manager_eval' and the evaluation criteria below.
evaluation_criteria_prog_m = (
    "The answer should include Email Router-specific product features. "
    "Each must have: Feature Name, Description, Key Functionality, and User Benefit. "
    "The answer should be product features that follow the following structure: "
    "Feature Name: A clear, concise title that identifies the capability\n"
    "Description: A brief explanation of what the feature does and its purpose\n"
    "Key Functionality: The specific capabilities or actions the feature provides\n"
    "User Benefit: How this feature creates value for the user"
)

program_manager_evaluation_agent = EvaluationAgent(
    openai_api_key=openai_api_key,
    persona=persona_program_manager_eval,
    evaluation_criteria=evaluation_criteria_prog_m,
    worker_agent=program_manager_knowledge_agent,
    max_interactions=10,
)

# Development Engineer - Knowledge Augmented Prompt Agent
persona_dev_engineer = "You are a Development Engineer, you are responsible for defining the development tasks for a product."
knowledge_dev_engineer = (
    "You are defining technical tasks based on user stories or features. "
    "The response MUST be a list of tasks. Each task MUST contain ALL of the following fields, in this exact order: "
    "Focus strictly on implementing Email Router capabilities such as email ingestion, classification, routing, and monitoring. "
    "Do NOT create generic login or authentication tasks.\n"
    "Task ID: A unique identifier for tracking purposes (e.g., TSK-001)\n"
    "Task Title: Brief description of the specific development work\n"
    "Related User Story: Reference to the parent user story\n"
    "Description: Detailed explanation of the technical work required\n"
    "Acceptance Criteria: Specific requirements that must be met for completion\n"
    "Estimated Effort: Time or complexity estimation\n"
    "Dependencies: Any tasks that must be completed first"
    f"\n--- PRODUCT SPEC ---\n{product_spec}"
)
# Instantiate a development_engineer_knowledge_agent using 'persona_dev_engineer' and 'knowledge_dev_engineer'
development_engineer_knowledge_agent = KnowledgeAugmentedPromptAgent(
    openai_api_key=openai_api_key,
    persona=persona_dev_engineer,
    knowledge=knowledge_dev_engineer,
)

# Development Engineer - Evaluation Agent
persona_dev_engineer_eval = (
    "You are an evaluation agent that checks the answers of other worker agents."
)

# TODO: 9 - Instantiate a development_engineer_evaluation_agent using 'persona_dev_engineer_eval' and the evaluation criteria below.
# --- MODIFICATION: Tightened evaluation criteria ---
evaluation_criteria_dev = (
    "The response MUST be a list of tasks. Each task MUST contain ALL of the following fields, in this exact order: "
    "Each task must be Email Router-specific (e.g., email ingestion, LLM classification, routing, monitoring). "
    "Do NOT include login, authentication, or generic web app tasks. "
    "Task ID: A unique identifier for tracking purposes (e.g., TSK-001)\n"
    "Task Title: Brief description of the specific development work\n"
    "Related User Story: Reference to the parent user story\n"
    "Description: Detailed explanation of the technical work required\n"
    "Acceptance Criteria: Specific requirements that must be met for completion\n"
    "Estimated Effort: Time or complexity estimation\n"
    "Dependencies: Any tasks that must be completed first"
)

development_engineer_evaluation_agent = EvaluationAgent(
    openai_api_key=openai_api_key,
    persona=persona_dev_engineer_eval,
    evaluation_criteria=evaluation_criteria_dev,
    worker_agent=development_engineer_knowledge_agent,
    max_interactions=10,
)

# Routing Agent
# TODO: 10 - Instantiate a routing_agent.
routing_agent = RoutingAgent(openai_api_key=openai_api_key, agents=[])


# Job function persona support functions
# TODO: 11 - Define the support functions for the routes of the routing agent
def product_manager_support_function(query):
    eval_result = product_manager_evaluation_agent.evaluate(initial_prompt=query)
    return eval_result["final_response"]


def program_manager_support_function(query):
    eval_result = program_manager_evaluation_agent.evaluate(initial_prompt=query)
    return eval_result["final_response"]


def development_engineer_support_function(query):
    eval_result = development_engineer_evaluation_agent.evaluate(initial_prompt=query)
    return eval_result["final_response"]


routes = [
    {
        "name": "Product Manager",
        "description": "Use this agent ONLY for creating **new user stories** from a product spec. Do not use for features or tasks.",
        "func": product_manager_support_function,
    },
    {
        "name": "Program Manager",
        "description": "Use this agent ONLY for **grouping existing user stories** into **high-level product features** with a name, description, and benefit.",
        "func": program_manager_support_function,
    },
    {
        "name": "Development Engineer",
        "description": "Use this agent ONLY for **breaking down** features or stories into **detailed, technical engineering tasks** that MUST include a Task ID, Related User Story, Acceptance Criteria, and Effort.",
        "func": development_engineer_support_function,
    },
]

# Assign the routes to the agent (completes TODO 10)
routing_agent.agents = routes

# Run the workflow

print("\n*** Workflow execution started ***\n")
# Workflow Prompt
# ****
workflow_prompt = "Generate a comprehensive project plan for this product, including user stories, product features, and development tasks."
# ****
print(f"Task to complete in this workflow, workflow prompt = {workflow_prompt}")

print("\nDefining workflow steps from the workflow prompt")
# TODO: 12 - Implement the workflow.
workflow_steps = action_planning_agent.extract_steps_from_prompt(workflow_prompt)
print(f"Workflow steps defined: {workflow_steps}")

completed_steps_output = []

cumulative_context = ""

for step in workflow_steps:
    if not step:
        continue

    print(f"\n--- EXECUTING STEP: {step} ---")

    prompt_with_context = (
        f"--- CONTEXT SO FAR ---\n"
        f"{cumulative_context}\n\n"
        f"--- CURRENT TASK ---\n"
        f"Based on the context above, please complete the following task: {step}"
    )
    result = routing_agent.route(prompt_with_context)

    completed_steps_output.append(result)

    cumulative_context += f"\n\n--- Output for Step: '{step}' ---\n{result}"

    print(f"--- STEP COMPLETED. Result: ---")
    print(result)
    print("-" * (len(step) + 21))

if completed_steps_output:
    print("\n*** Workflow execution finished ***\n")
    print("--- Consolidated Project Plan (Console Output) ---")

    for i, result in enumerate(completed_steps_output, 1):
        step_title = (
            workflow_steps[i - 1] if i - 1 < len(workflow_steps) else f"Step {i}"
        )
        print(f"\n--- Output from Step {i}: {step_title} ---")
        print(result)

    print("\n*** Saving consolidated plan to file ***\n")

    output_folder = "outputs"
    output_filename = os.path.join(output_folder, "phase2_tasks.txt")

    os.makedirs(output_folder, exist_ok=True)

    with open(output_filename, "w", encoding="utf-8") as f:
        f.write("--- Consolidated Project Plan ---\n\n")
        for i, result in enumerate(completed_steps_output, 1):
            step_title = (
                workflow_steps[i - 1] if i - 1 < len(workflow_steps) else f"Step {i}"
            )
            f.write(f"--- Output from Step {i}: {step_title} ---\n")
            f.write(result)
            f.write("\n\n")  #
    print(f"Successfully saved results to {output_filename}")

else:
    print("\n*** Workflow execution finished with no steps. ***\n")
