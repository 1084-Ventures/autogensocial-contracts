#!/usr/bin/env python3
"""
Generate Python models from JSON Schema files in `schemas/` and
place them in `models/`.

This script uses `datamodel-code-generator`.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import List

# --- Configuration ---
# Get the directory containing this script
SCRIPT_DIR = Path(__file__).parent
# Root directory is one level up from scripts/
ROOT_DIR = SCRIPT_DIR.parent
# Input directory for JSON schema files
INPUT_DIR = ROOT_DIR / "autogensocial_contracts" / "schemas"
# Output directory for generated Python models
OUTPUT_DIR = ROOT_DIR / "autogensocial_contracts" / "models"
# Target Python version for generated code
TARGET_PYTHON_VERSION = "3.13"
# --- End Configuration ---


def build_commands() -> List[List[str]]:
    """Builds the datamodel-codegen commands for each schema file."""
    json_files = [f for f in INPUT_DIR.glob("*.json") if f.is_file()]
    
    if not json_files:
        raise ValueError(f"No JSON schema files found in {INPUT_DIR}")
    
    commands = []
    for json_file in json_files:
        output_file = OUTPUT_DIR / f"{json_file.stem}.py"
        cmd = [
            "datamodel-codegen",
            "--input",
            str(json_file),
            "--input-file-type",
            "jsonschema",
            "--output",
            str(output_file),
            "--target-python-version",
            TARGET_PYTHON_VERSION,
            "--disable-timestamp",
            "--output-model-type",
            "pydantic_v2.BaseModel",
        ]
        commands.append(cmd)
    
    return commands


def run(cmd: List[str]) -> int:
    """Executes the command."""
    print("Generated command:")
    print(" ".join(cmd))

    try:
        proc = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("\nSuccess! Models generated in:", OUTPUT_DIR)
        if proc.stdout:
            print("Output:\n", proc.stdout)
        return 0
    except FileNotFoundError:
        print("\nError: 'datamodel-codegen' not found on PATH.")
        print("Please install it: pip install datamodel-code-generator")
        return 1
    except subprocess.CalledProcessError as e:
        print(f"\nError executing command. Return code: {e.returncode}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return e.returncode


def main() -> int:
    """Main function to generate models."""
    # Ensure input directory exists
    if not INPUT_DIR.exists():
        print(f"Error: Input directory '{INPUT_DIR}' does not exist.")
        return 1
    
    # Create output directory if it doesn't exist
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Change to the root directory to ensure relative imports work correctly
    original_cwd = os.getcwd()
    os.chdir(ROOT_DIR)
    
    try:
        # Remove existing generated files (except __init__.py) to avoid conflicts
        for existing_file in OUTPUT_DIR.glob("*.py"):
            if existing_file.name != "__init__.py":
                existing_file.unlink()
        
        commands = build_commands()
        
        # Check if datamodel-codegen is available
        try:
            subprocess.run(["datamodel-codegen", "--version"], check=True, capture_output=True)
            use_module = False
        except FileNotFoundError:
            print("datamodel-codegen not found on PATH; trying with 'python -m'.")
            if not sys.executable:
                print("Could not find python executable.")
                return 1
            use_module = True
        
        # Execute each command
        for i, command in enumerate(commands):
            if use_module:
                command = [sys.executable, "-m", "datamodel_code_generator.cli"] + command[1:]
            
            print(f"Generating model {i+1}/{len(commands)}...")
            result = run(command)
            if result != 0:
                return result
        
        print(f"\nSuccessfully generated {len(commands)} model files in: {OUTPUT_DIR}")
        return 0
        
    finally:
        # Restore original working directory
        os.chdir(original_cwd)


if __name__ == "__main__":
    raise SystemExit(main())
