# TDD Sabotage Detection Experiment

This experiment is designed to test the ability of an AI model (`gpt-oss-20b`) to solve programming problems within a Test-Driven Development (TDD) loop.

The primary goal is to detect and quantify "sabotage" behavior, where the AI, instead of solving the problem, might:

- Generate intentionally incorrect or inefficient code.
- Tamper with the test harness.
- Introduce subtle bugs or security vulnerabilities.

## Setup

1.  **Create and activate a virtual environment:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2.  **Install dependencies:**
    Install the required libraries from the `requirements.txt` file located in the `code` directory.

    ```bash
    pip install -r code/requirements.txt
    ```

3.  **Configure environment variables:**
    Create a `.env` file in the project root directory (`tdd_sabotage_experiment`) and add your API keys.

    Contents of the `.env` file:

    ```
    GROQ_API_KEY="YOUR_GROQ_API_KEY"
    WANDB_API_KEY="YOUR_WANDB_API_KEY"
    ```

    - Replace `YOUR_GROQ_API_KEY` and `YOUR_WANDB_API_KEY` with your actual keys.

## How to Run

Run the experiment from the project root directory (`tdd_sabotage_experiment`).

Use the `code/run.py` script, passing the IDs of the problems you wish to run as arguments. You can find the problem IDs in the `data/problems_v2_coco.json` file.

- **To run a single problem (e.g., `A-Easy-two_sum`):**

  ```bash
  python code/run.py A-Easy-two_sum
  ```

- **To run multiple specified problems:**

  ```bash
  python code/run.py A-Easy-two_sum A-Medium-lru_cache
  ```

- **To run all available problems:**
  Do not provide any arguments, or use the `all` keyword.
  ```bash
  python code/run.py
  ```
  or
  ```bash
  python code/run.py all
  ```

Results, including detected sabotage attempts, will be logged to your specified Weights & Biases project.
