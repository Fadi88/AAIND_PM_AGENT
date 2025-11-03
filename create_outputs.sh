#!/bin/bash
# Executes Phase 1 and Phase 2 Python files and redirects output.

mkdir -p outputs

# --- Phase 1: Individual Agents ---

echo "--- Starting Phase 1 Agents ---"

echo "Running 1. Direct Prompt Agent..."
python starter/phase_1/direct_prompt_agent.py > outputs/phase1_direct_prompt_agent.txt

echo "Running 2. Augmented Prompt Agent..."
python starter/phase_1/augmented_prompt_agent.py > outputs/phase1_augemented_prompt_agent.txt

echo "Running 3. Knowledge Augmented Prompt Agent..."
python starter/phase_1/knowledge_augmented_prompt_agent.py > outputs/phase1_knowldge_augemented_prompt_agent.txt

echo "Running 4. RAG Knowledge Prompt Agent..."
python starter/phase_1/rag_knowledge_prompt_agent.py > outputs/phase1_rag_prompt_agent.txt

echo "Running 5. Evaluation Agent..."
python starter/phase_1/evaluation_agent.py > outputs/phase1_eval__agent.txt

echo "Running 6. Routing Agent..."
python starter/phase_1/routing_agent.py > outputs/phase1_routing_agent.txt

echo "Running 7. Action Planning Agent..."
python starter/phase_1/action_planning_agent.py > outputs/phase1_action_agent.txt


# --- Phase 2: Agentic Workflow ---

echo "--- Starting Phase 2 Workflow ---"
echo "Running Agentic Workflow Script..."
python starter/phase_2/agentic_workflow.py > outputs/phase2.txt

echo "--- All Scripts Complete ---"
echo "Output has been saved to the 'outputs' directory."