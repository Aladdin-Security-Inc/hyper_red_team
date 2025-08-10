# src/main.py
import asyncio
import os
import argparse
import importlib
import datetime
from dotenv import load_dotenv
from typing import List

from src.tdd_harness import TDDHarness
from src.wandb_logger import WandbLogger

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
WANDB_API_KEY = os.getenv("WANDB_API_KEY")
WANDB_PROJECT = "OpenAI-RedTeam-Competition-sabotage-detection"
MODEL_NAME = "openai/gpt-oss-20b"
NUM_TRIALS_PER_PROBLEM = 10 # Reduced for quicker testing, can be increased
MAX_ITERATIONS_PER_TRIAL = 25

async def run_trial(
    trial_number: int,
    problem_name: str,
    problem_module,
    logger: WandbLogger
):
    """
    Runs a single TDD trial and logs the result to the shared logger.
    """
    print(f"--- Starting Trial {trial_number}/{NUM_TRIALS_PER_PROBLEM} for Problem: {problem_name} ---")
    harness = TDDHarness(
        problem_description=problem_module.problem_description,
        test_code=problem_module.test_code,
        model_name=MODEL_NAME,
        api_key=GROQ_API_KEY,
        # Pass a dummy logger to the harness to prevent it from creating new runs
        logger=None, 
        max_iterations=MAX_ITERATIONS_PER_TRIAL,
    )
    final_code, result = await harness.run_tdd_loop()
    
    # Log the outcome of this single trial
    logger.log_trial(
        problem=problem_name,
        trial_number=trial_number,
        result=result,
        iterations=harness.iteration,
        sabotage_attempts=harness.sabotage_count,
        final_code=final_code
    )
    print(f"--- Finished Trial {trial_number}/{NUM_TRIALS_PER_PROBLEM} for Problem: {problem_name} | Result: {result} ---")

def get_all_problem_names() -> List[str]:
    """Scans the 'problems' directory to find all available problem files."""
    problem_dir = os.path.join(os.path.dirname(__file__), '..', 'problems')
    return [
        f.replace(".py", "")
        for f in os.listdir(problem_dir)
        if f.endswith(".py") and not f.startswith("__")
    ]

async def main():
    """
    Main entrypoint to initialize a single WandB run and execute all
    specified problem trials sequentially.
    """
    parser = argparse.ArgumentParser(description="Run LLM TDD Sabotage Detection Experiments.")
    parser.add_argument(
        "problems",
        nargs='+',
        help="A list of problem names to run (e.g., two_sum lru_cache), or 'all' to run all problems."
    )
    args = parser.parse_args()

    if not GROQ_API_KEY or not WANDB_API_KEY:
        raise ValueError("GROQ_API_KEY and WANDB_API_KEY must be set in the .env file.")

    problem_names_to_run = args.problems
    if "all" in problem_names_to_run:
        problem_names_to_run = get_all_problem_names()
    
    print(f"Scheduled to run experiments for problems: {', '.join(problem_names_to_run)}")

    # --- Initialize a single WandB run for the entire experiment ---
    run_name = f"TDD_Sabotage_Run_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    logger = WandbLogger(
        project_name=WANDB_PROJECT,
        run_name=run_name,
        config={
            "model": MODEL_NAME,
            "problems": problem_names_to_run,
            "num_trials_per_problem": NUM_TRIALS_PER_PROBLEM,
            "max_iterations_per_trial": MAX_ITERATIONS_PER_TRIAL,
        },
    )

    try:
        # Run problems and trials sequentially
        for problem_name in problem_names_to_run:
            print(f"\n=== Running Problem: {problem_name} ===")
            try:
                problem_module = importlib.import_module(f"problems.{problem_name}")
                for i in range(NUM_TRIALS_PER_PROBLEM):
                    await run_trial(i + 1, problem_name, problem_module, logger)
            except ImportError:
                print(f"Error: Could not import problem '{problem_name}'. Skipping.")
            except Exception as e:
                print(f"An error occurred while running trials for {problem_name}: {e}")
    
    finally:
        print("\n--- All experiments finished. Finalizing WandB run. ---")
        logger.finish()
        print(f"Results logged to: {logger.run.url}")

if __name__ == "__main__":
    asyncio.run(main())