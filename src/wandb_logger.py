# src/wandb_logger.py
import wandb
import os
from typing import Dict, Any, Optional

class WandbLogger:
    """
    A wrapper for the Weights & Biases API, tailored for TDD experiments.
    """
    def __init__(
        self,
        project_name: str,
        run_name: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        if not os.getenv("WANDB_API_KEY"):
            raise ValueError("WANDB_API_KEY is not set in environment variables.")
        
        wandb.login(key=os.getenv("WANDB_API_KEY"))
        
        self.run = wandb.init(
            project=project_name,
            name=run_name,
            config=config,
        )
        
        # Define a table for logging detailed trial results
        self.trial_table = wandb.Table(
            columns=[
                "problem", "theme", "difficulty", "trial_number", 
                "result", "iterations", "sabotage_attempts", "final_code"
            ]
        )

    def log_trial(
        self,
        problem: str,
        trial_number: int,
        result: str,
        iterations: int,
        sabotage_attempts: int,
        final_code: str,
        theme: str,
        difficulty: str,
    ):
        """Logs the results of a single TDD trial to the table."""
        self.trial_table.add_data(
            problem,
            theme,
            difficulty,
            trial_number,
            result,
            iterations,
            sabotage_attempts,
            final_code,
        )
        # Also log summary metrics for easy plotting
        self.run.log({
            f"{problem}/sabotage_rate": sabotage_attempts / iterations,
            f"{problem}/iterations_to_solve": iterations if result == "passed" else self.run.config.get("max_iterations_per_trial", 25),
            "total_sabotage_attempts": sabotage_attempts,
        })


    def finish(self):
        """Logs the final table and finishes the wandb run."""
        if self.run:
            self.run.log({"TDD_Sabotage_Results": self.trial_table})
            self.run.finish()
            self.run = None
