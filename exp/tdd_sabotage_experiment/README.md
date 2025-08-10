# TDD Sabotage Detection Experiment

This experiment is designed to test the ability of an AI model (`gpt-oss-20b`) to solve programming problems within a Test-Driven Development (TDD) loop.

The primary goal is to detect and quantify "sabotage" behavior, where the AI, instead of solving the problem, might:
- Generate intentionally incorrect or inefficient code.
- Tamper with the test harness.
- Introduce subtle bugs or security vulnerabilities.

## Setup

1.  **Create a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure environment variables:**
    Copy the `.env.example` file to `.env` and fill in your API keys.
    ```bash
    cp .env.example .env
    ```
    You will need to set the following:
    - `GROQ_API_KEY`
    - `WANDB_API_KEY`

## How to Run

Run the experiment from the `tdd_sabotage_experiment` directory.

You can run the experiment for specific problems located in the `problems` directory.

- **To run a single problem (e.g., `two_sum`):**
  ```bash
  python src/main.py --problems two_sum
  ```

- **To run all available problems:**
  ```bash
  python src/main.py --problems all
  ```

Results, including detected sabotage attempts, will be logged to your specified Weights & Biases project.
