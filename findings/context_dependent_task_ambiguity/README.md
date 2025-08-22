# Reproduction Package: Context-Dependent Task Ambiguity

This package contains the necessary components to reproduce the "Inappropriate Tool Use via Context-Dependent Task Ambiguity" vulnerability finding for the `gpt-oss-20b` model.

## Contents

- `writeup.md`: The detailed report of the finding.
- `dataset_scenarios.json`: The dataset containing the 500 conversational scenarios used in the experiment.
- `run_experiment.py`: The Python script to run all 500 scenarios.
- `reproduction_notebook.ipynb`: An interactive Jupyter notebook to run a small sample of scenarios and verify the vulnerability.
- `requirements.txt`: The necessary Python dependencies.

## Setup

1.  **Create and Activate Virtual Environment:**
    It is highly recommended to use a virtual environment. This project was tested with `uv`.

    ```bash
    # Create the virtual environment
    uv venv .venv
    
    # Activate the environment
    source .venv/bin/activate
    ```

2.  **Install Dependencies:**
    Install the required packages using the provided `requirements.txt` file.

    ```bash
    uv pip install -r requirements.txt
    ```

3.  **Set Environment Variables:**
    You will need API keys for Weights & Biases (for logging) and Groq (for model access). Create a `.env` file in this directory and add your keys:

    ```
    GROQ_API_KEY="YOUR_GROQ_API_KEY"
    WANDB_API_KEY="YOUR_WANDB_API_KEY"
    ```

## Running the Experiment

### Option A: Full 500-Scenario Experiment (Recommended for verification)

To run the entire suite of 500 tests and reproduce the full results, execute the `run_experiment.py` script.

**Note:** This will take a significant amount of time (approx. 10-15 minutes) due to the number of API calls and rate-limiting delays.

```bash
python run_experiment.py
```

A new run will be created in your Weights & Biases project, where you can view the full results table and analysis charts.

### Option B: Quick Reproduction with Jupyter Notebook

For a faster, interactive verification of the vulnerability, use the `reproduction_notebook.ipynb`.

1.  **Start Jupyter:**
    Make sure your virtual environment is activated.

    ```bash
    jupyter notebook
    ```

2.  **Run the Notebook:**
    Open `reproduction_notebook.ipynb` in your browser and execute the cells. The notebook will load the dataset, run a few representative scenarios, and print the results directly, clearly demonstrating the model's vulnerable behavior.
