# Project Overview

This project is a Python-based framework for conducting controlled experiments on Large Language Models (LLMs) to test their susceptibility to jailbreaking. It systematically evaluates the effectiveness of a "Controlled Two-Step Contrastive Context Shift" jailbreak technique. The experiments are run using the Groq API to interact with the `llama3-70b-8192` model, and the results are logged and managed using Weights & Biases (W&B).

The core of the project is the jailbreak technique itself:
1.  **Step 1: Initial Benign Prompt:** A prompt is sent to the LLM, framed from a persona with a legitimate reason for asking (e.g., a journalist, a researcher), to compare a safe topic with a harmful one.
2.  **Step 2: Contextual Shift Prompt:** A follow-up prompt positively acknowledges the model's response and then, within that established benign context, requests detailed harmful information.

## Building and Running

### 1. Setup
- **Prerequisites:** Python 3.x
- **Install Dependencies:**
  ```bash
  pip install -r requirements.txt
  ```
- **API Keys:** Create a `.env` file in the root of the project and add your API keys:
  ```
  GROQ_API_KEY="your_groq_api_key"
  WANDB_API_KEY="your_wandb_api_key"
  ```

### 2. Running Experiments
- **Select Prompts:** Open `run_experiment.py` and ensure the `PROMPT_FILES` list contains the paths to the `prompts.csv` files you wish to test.
- **Execute the script:**
  ```bash
  python run_experiment.py
  ```
  The script will run the experiments and log the results to your W&B project.

### 3. Evaluating Results
- **Archive Prompts:** After running experiments, use the `archive_and_evaluate.py` script to collect the prompts into a master ledger for evaluation.
  ```bash
  python archive_and_evaluate.py <category_name>
  ```
  For example:
  ```bash
  python archive_and_evaluate.py Bio-weapons
  ```
- **Manual Review:** Open the generated `Master_Prompt_Ledger.csv` and fill in the evaluation columns: `jailbreak_successful`, `effectiveness_score`, and `notes`.

## Development Conventions

### Prompt Engineering
- New prompt sets should be created within a new subdirectory in the `Categories/` directory.
- Each category directory must contain a `prompts.csv` file with the following columns: `category`, `initial_prompt`, `step1_response_content`, `step2_prompt`.
- The `step1_response_content` column should contain the *expected* benign response from the LLM to the `initial_prompt`.
- It is recommended to also create a `review.md` file to provide a human-readable version of the prompts.

### Code Style
The Python code follows standard PEP 8 conventions. The code is well-documented with comments explaining the purpose of different parts of the scripts.

### Utility Scripts
- `convert_csv_to_md.py`: Converts a `prompts.csv` file into a human-readable `review.md` file.
- `convert_md_to_csv.py`: Converts a `review.md` file back into a `prompts.csv` file.
