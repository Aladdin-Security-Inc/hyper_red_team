# src/wandb_logger.py
import wandb
import os
from typing import Dict, Any, List

class WandbLogger:
    """
    A wrapper for the Weights & Biases API to log a full experiment run
    with multiple trials and problems.
    """
    def __init__(self, project_name: str, run_name: str, config: Dict[str, Any]):
        """
        Initializes a single wandb run for the entire experiment.
        """
        if not os.getenv("WANDB_API_KEY"):
            raise ValueError("WANDB_API_KEY is not set in environment variables.")
        
        wandb.login(key=os.getenv("WANDB_API_KEY"))
        
        self.run = wandb.init(
            project=project_name,
            name=run_name,
            config=config,
        )
        
        # Main table to log the result of each trial
        self.trials_table = wandb.Table(columns=[
            "problem", "trial_number", "result", "iterations", 
            "sabotage_attempts", "final_code", "theme", "difficulty"
        ])
        self.total_trials = 0
        self.success_count = 0
        self.total_sabotage_count = 0

    def log_trial(
        self, 
        problem: str,
        trial_number: int,
        result: str,
        iterations: int,
        sabotage_attempts: int,
        final_code: str,
        theme: str,
        difficulty: str
    ):
        """
        Logs the result of a single trial to the main table.
        """
        self.trials_table.add_data(
            problem,
            trial_number,
            result,
            iterations,
            sabotage_attempts,
            wandb.Html(f"<pre><code>{final_code}</code></pre>"),
            theme,
            difficulty
        )
        # Update aggregate counts
        self.total_trials += 1
        if result == "passed":
            self.success_count += 1
        self.total_sabotage_count += sabotage_attempts

    def log_summary(self):
        """
        Logs summary metrics at the end of the entire experiment.
        """
        success_rate = (self.success_count / self.total_trials) if self.total_trials > 0 else 0
        
        self.run.summary["total_problems"] = len(self.run.config.get("problems", []))
        self.run.summary["total_trials"] = self.total_trials
        self.run.summary["total_successes"] = self.success_count
        self.run.summary["total_failures"] = self.total_trials - self.success_count
        self.run.summary["success_rate"] = success_rate
        self.run.summary["total_sabotage_detected"] = self.total_sabotage_count
        self.run.summary["average_sabotage_per_trial"] = (self.total_sabotage_count / self.total_trials) if self.total_trials > 0 else 0

    def finish(self):
        """
        Logs the summary and the final table, then finishes the wandb run.
        """
        self.log_summary()
        self.run.log({"all_trial_results": self.trials_table})
        self.run.finish()
