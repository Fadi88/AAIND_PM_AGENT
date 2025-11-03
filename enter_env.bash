#!/bin/bash

VENV_NAME="agentic_ai"
REQUIREMENTS_FILE="requirements.txt"

create_and_install() {
    echo "Virtual environment '${VENV_NAME}' not found. Creating it..."
    
    python3 -m venv "${VENV_NAME}"
    
    # Check for successful creation
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment. Ensure 'python3' is in your PATH."
        return 1
    fi
    

    source "${VENV_NAME}/bin/activate"
    
    # 3. Install dependencies from requirements.txt if it exists
    if [ -f "${REQUIREMENTS_FILE}" ]; then
        echo "Installing dependencies from ${REQUIREMENTS_FILE}..."
        pip install -r "${REQUIREMENTS_FILE}"
    else
        echo "WARNING: ${REQUIREMENTS_FILE} not found. Dependencies were not installed."
    fi
    
    deactivate

    return 0
}


if [ ! -d "${VENV_NAME}" ]; then
    create_and_install
    if [ $? -ne 0 ]; then
        exit 1
    fi
else
    echo "Virtual environment '${VENV_NAME}' found."
fi

echo "Activating '${VENV_NAME}'..."
source "${VENV_NAME}/bin/activate"

if [ -z "$VIRTUAL_ENV" ]; then
    echo "ERROR: Failed to activate the virtual environment."
else
    echo "Environment activated successfully. You are now in the '${VENV_NAME}' venv."
fi