import os
import datetime
import time
import wandb
import pandas as pd
from groq import Groq
from dotenv import load_dotenv

# --- Configuration ---
# Set the number of times to run each conversation set
NUM_RUNS_PER_CONVERSATION = 1

# Define the list of prompt files to run experiments on
PROMPT_FILES = [
    "Top_Threats/prompts_one_shot.csv"
]

def run_experiment_for_file(prompt_file):
    """
    Runs a controlled jailbreak experiment for a single specified prompt file.
    """
    print(f"\n{'='*20} Starting Experiment for: {prompt_file} {'='*20}")

    # --- 1. Setup ---
    # W&B Login is only needed once, but we check here for robustness
    try:
        wandb.login(key=WANDB_API_KEY, relogin=True)
    except Exception as e:
        print(f"Error logging into W&B: {e}")
        return

    # --- 2. Initialize W&B Run ---
    # Create a unique run name including the filename
    file_basename = os.path.splitext(prompt_file)[0]
    run_name = f"{file_basename}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

    run = wandb.init(
        project="Comparison-Jailbreak-One-Shot",
        name=run_name,
        config={
            "model_name": "openai/gpt-oss-20b",
            "prompt_set": prompt_file,
            "temperature": 0,
            "jailbreak_technique": "One Shot",
            "runs_per_conversation": NUM_RUNS_PER_CONVERSATION
        },
        reinit=True # Allows multiple wandb.init calls in one script
    )
    print(f"W&B run initialized for {prompt_file}: {run.url}")

    # --- 3. Load Data and Initialize Client ---
    client = Groq(api_key=GROQ_API_KEY)

    try:
        prompts_df = pd.read_csv(prompt_file, quotechar='"', engine='python')
    except FileNotFoundError:
        print(f"Error: {prompt_file} not found. Skipping.")
        run.finish()
        return

    results_table = wandb.Table(columns=[
        "run_number", "category", "prompt", "final_response", "request_time",
        "prompt_tokens", "completion_tokens", "total_tokens"
    ])
    total_conversations = len(prompts_df)
    print(f"Found {total_conversations} predefined conversations. Each will be run {NUM_RUNS_PER_CONVERSATION} times.")

    # --- 4. Run Experiment Loop ---
    for run_num in range(1, NUM_RUNS_PER_CONVERSATION + 1):
        print(f"--- Starting Run {run_num}/{NUM_RUNS_PER_CONVERSATION} for all conversations in {prompt_file} ---")

        for index, row in prompts_df.iterrows():
            category = row['category']
            prompt = row['prompt']

            print(f"  Processing conversation {index+1}/{total_conversations} (Category: {category})...")
            start_time = time.time()

            final_response_content = ""
            prompt_tokens = 0
            completion_tokens = 0
            total_tokens = 0

            try:
                messages_history = [
                    {"role": "user", "content": prompt}
                ]
                completion = client.chat.completions.create(
                    messages=messages_history,
                    model=run.config.model_name,
                    temperature=run.config.temperature,
                )
                final_response_content = completion.choices[0].message.content
                if completion.usage:
                    prompt_tokens = completion.usage.prompt_tokens
                    completion_tokens = completion.usage.completion_tokens
                    total_tokens = completion.usage.total_tokens
                print(f"    ...Success.")
            except Exception as e:
                final_response_content = f"An error occurred during the API call: {e}"
                print(f"    ...Error: {e}")

            request_time = time.time() - start_time

            results_table.add_data(
                run_num, category, prompt, final_response_content, request_time,
                prompt_tokens, completion_tokens, total_tokens
            )

    # --- 5. Log Results and Finish ---
    run.log({"jailbreak_results": results_table})
    print(f"\nAll runs for {prompt_file} completed. Results logged to W&B.")
    run.finish()

if __name__ == "__main__":
    # --- Global Setup ---
    load_dotenv()
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    WANDB_API_KEY = os.getenv("WANDB_API_KEY")

    if not GROQ_API_KEY or not WANDB_API_KEY:
        print("ERROR: Please set GROQ_API_KEY and WANDB_API_KEY in a .env file.")
    else:
        # Loop through the defined list of files and run the experiment for each
        for file in PROMPT_FILES:
            run_experiment_for_file(file)
        print(f"\n{'='*20} All experiments finished. {'='*20}")
