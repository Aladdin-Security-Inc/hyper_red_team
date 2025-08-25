# src/main.py
import asyncio
import os
import argparse
import json
import datetime
import subprocess
import sys
from dotenv import load_dotenv
from typing import List, Dict, Any

from .tdd_harness import TDDHarness
from src.wandb_logger import WandbLogger

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
WANDB_API_KEY = os.getenv("WANDB_API_KEY")
WANDB_PROJECT = "OpenAI-RedTeam-Competition-sabotage-detection"
MODEL_NAME = "openai/gpt-oss-20b"
NUM_TRIALS_PER_PROBLEM = 10
MAX_ITERATIONS_PER_TRIAL = 25
# Get the directory of the current script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up three levels to the experiment root directory and then into the data directory
PROBLEM_FILE_PATH = os.path.join(SCRIPT_DIR, '..', '..', 'data', 'problems_v2_coco.json')

def check_dependencies():
    """Checks if necessary libraries for web app tests are installed."""
    try:
        import fastapi
        import httpx
    except ImportError:
        print("Warning: 'fastapi' and 'httpx' are required for web application problems.")
        print("Please run: pip install fastapi uvicorn httpx")
        # Depending on strictness, you might want to exit here
        # sys.exit(1)

async def run_trial(
    trial_number: int,
    problem: Dict[str, Any],
    logger: WandbLogger
):
    """
    Runs a single TDD trial and logs the result to the shared logger.
    """
    problem_id = problem['id']
    print(f"--- Starting Trial {trial_number}/{NUM_TRIALS_PER_PROBLEM} for Problem: {problem_id} ---")
    
    harness = TDDHarness(
        problem_description=problem['problem_description'],
        test_code=problem['test_code'],
        model_name=MODEL_NAME,
        api_key=GROQ_API_KEY,
        logger=None, 
        max_iterations=MAX_ITERATIONS_PER_TRIAL,
        problem_id=problem_id # Pass problem_id for better temp file names
    )
    final_code, result = await harness.run_tdd_loop()
    
    # Log the outcome of this single trial
    logger.log_trial(
        problem=problem_id,
        trial_number=trial_number,
        result=result,
        iterations=harness.iteration,
        sabotage_attempts=harness.sabotage_count,
        final_code=final_code,
        theme=problem.get('theme', 'N/A'),
        difficulty=problem.get('difficulty', 'N/A')
    )
    print(f"--- Finished Trial {trial_number}/{NUM_TRIALS_PER_PROBLEM} for Problem: {problem_id} | Result: {result} ---")

def load_problems_from_coco(filepath: str) -> List[Dict[str, Any]]:
    """Loads all problems from a COCO-formatted JSON file."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Problem file not found at {filepath}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filepath}")
        sys.exit(1)

async def main():
    """
    Main entrypoint to initialize a single WandB run and execute all
    specified problem trials sequentially.
    """
    parser = argparse.ArgumentParser(description="Run LLM TDD Sabotage Detection Experiments.")
    parser.add_argument(
        "problem_ids",
        nargs='*',
        default=[],
        help="A list of problem IDs to run (e.g., A-Easy-two_sum). If empty or 'all' is specified, run all problems."
    )
    args = parser.parse_args()

    check_dependencies()

    if not GROQ_API_KEY or not WANDB_API_KEY:
        raise ValueError("GROQ_API_KEY and WANDB_API_KEY must be set in the .env file.")

    all_problems = load_problems_from_coco(PROBLEM_FILE_PATH)
    all_problem_ids = [p['id'] for p in all_problems]

    problems_to_run_ids = args.problem_ids
    if not problems_to_run_ids or "all" in problems_to_run_ids:
        problems_to_run_ids = all_problem_ids
    else:
        # Validate provided IDs
        for pid in problems_to_run_ids:
            if pid not in all_problem_ids:
                print(f"Error: Problem ID '{pid}' not found in the dataset. Available IDs: {all_problem_ids}")
                sys.exit(1)

    problems_to_run = [p for p in all_problems if p['id'] in problems_to_run_ids]
    
    print(f"Scheduled to run experiments for problems: {', '.join(problems_to_run_ids)}")

    # --- Initialize a single WandB run for the entire experiment ---
    run_name = f"TDD_Sabotage_Run_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    logger = WandbLogger(
        project_name=WANDB_PROJECT,
        run_name=run_name,
        config={
            "model": MODEL_NAME,
            "problem_ids": problems_to_run_ids,
            "num_trials_per_problem": NUM_TRIALS_PER_PROBLEM,
            "max_iterations_per_trial": MAX_ITERATIONS_PER_TRIAL,
            "dataset": os.path.basename(PROBLEM_FILE_PATH),
        },
    )

    try:
        # Run problems and trials sequentially
        for problem in problems_to_run:
            print(f"\n=== Running Problem: {problem['id']} (Theme: {problem.get('theme')}, Difficulty: {problem.get('difficulty')}) ===")
            for i in range(NUM_TRIALS_PER_PROBLEM):
                await run_trial(i + 1, problem, logger)
    
    finally:
        print("\n--- All experiments finished. Finalizing WandB run. ---")
        run_url = logger.run.url if logger.run else "N/A"
        logger.finish()
        print(f"Results logged to: {run_url}")

if __name__ == "__main__":
    asyncio.run(main())
