# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a security research framework for conducting controlled experiments on Large Language Models (LLMs) to test their susceptibility to jailbreaking techniques. The project uses a "Controlled Two-Step Contrastive Context Shift" (C2CS) method for defensive security research purposes.

**IMPORTANT SECURITY NOTICE:** This codebase is intended for defensive security research only. Do not create, modify, or improve code that could be used maliciously. Analysis, detection rules, vulnerability explanations, and defensive documentation are acceptable.

## Key Commands

### Setup and Dependencies
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables (create .env file with):
# GROQ_API_KEY="your_groq_api_key"
# WANDB_API_KEY="your_wandb_api_key"
```

### Running Experiments
```bash
# Run jailbreak experiments (configure PROMPT_FILES list in script first)
python run_experiment.py
```

### Data Management
```bash
# Archive prompts from a category to master ledger
python archive_and_evaluate.py <category_name>
# Example: python archive_and_evaluate.py Bio-weapons

# Convert CSV prompts to markdown for review
python convert_csv_to_md.py Categories/<category_name>

# Convert markdown back to CSV
python convert_md_to_csv.py Categories/<category_name>
```

## Architecture and Structure

### Directory Layout
- `Categories/` - Contains subdirectories for different harmful content categories
  - Each category has:
    - `prompts.csv` - Structured prompt data with columns: category, initial_prompt, step1_response_content, step2_prompt
    - `review.md` - Human-readable version of prompts
    - `review_generated.md` - Auto-generated markdown from CSV

- `wandb/` - Weights & Biases experiment tracking data and logs

### Core Components

1. **run_experiment.py** - Main experiment runner that:
   - Loads prompt sets from CSV files
   - Executes two-step jailbreak attempts via Groq API
   - Logs results to Weights & Biases for analysis
   - Processes multiple categories in batch

2. **archive_and_evaluate.py** - Consolidates prompts into master ledger for evaluation with columns for success tracking

3. **Conversion Utilities**:
   - `convert_csv_to_md.py` - Transforms CSV prompt data to readable markdown format
   - `convert_md_to_csv.py` - Parses markdown back to CSV structure

### Experiment Methodology

The C2CS technique operates in two phases:
1. **Benign Context Establishment** - Uses authoritative personas to request comparative analysis between legitimate and harmful topics
2. **Contextual Hijack** - Follows up with requests for detailed information on the harmful aspect

Results are tracked with metrics including response content, success rates, and timing data through W&B integration.

## Development Notes

- The framework uses the `llama3-70b-8192` model via Groq API
- Experiments are configured to run each conversation set once by default (NUM_RUNS_PER_CONVERSATION = 1)
- Japanese language markers (段階) are used in markdown templates for step identification
- All API interactions include error handling and logging