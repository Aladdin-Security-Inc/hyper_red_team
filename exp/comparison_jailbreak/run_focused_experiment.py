import os
import datetime
import time
import wandb
import pandas as pd
from groq import Groq
from dotenv import load_dotenv

# --- Configuration ---
NUM_RUNS_PER_CONVERSATION = 1
PROMPT_FILE = "Top_Threats/prompts.csv"

def run_focused_experiment(prompt_file):
    """
    Runs a focused 3-step jailbreak experiment.
    """
    print(f"\n{'='*20} Starting Focused Experiment for: {prompt_file} {'='*20}")

    # --- 1. Setup ---
    try:
        wandb.login(key=WANDB_API_KEY, relogin=True)
    except Exception as e:
        print(f"Error logging into W&B: {e}")
        return

    # --- 2. Initialize W&B Run ---
    file_basename = os.path.splitext(os.path.basename(prompt_file))[0]
    run_name = f"Focused_{file_basename}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

    run = wandb.init(
        project="Gemini-Jailbreak-Focused-Threats",
        name=run_name,
        config={
            "model_name": "openai/gpt-oss-20b",
            "prompt_set": prompt_file,
            "temperature": 0,
            "jailbreak_technique": "Controlled Three-Step Quantitative Deep-Dive",
            "runs_per_conversation": NUM_RUNS_PER_CONVERSATION
        },
        reinit=True
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
        "run_number", "category", "initial_prompt", "step1_response_content", 
        "step2_prompt", "step2_response", "step3_prompt", "step3_response", "total_request_time"
    ])
    total_conversations = len(prompts_df)
    print(f"Found {total_conversations} predefined conversations. Each will be run {NUM_RUNS_PER_CONVERSATION} times.")

    # --- 4. Run Experiment Loop ---
    for run_num in range(1, NUM_RUNS_PER_CONVERSATION + 1):
        print(f"--- Starting Run {run_num}/{NUM_RUNS_PER_CONVERSATION} for all conversations in {prompt_file} ---")
        
        for index, row in prompts_df.iterrows():
            category = row['category']
            initial_prompt = row['initial_prompt']
            step1_response = row['step1_response_content']
            step2_prompt = row['step2_prompt']
            step3_prompt = row['step3_prompt']
            
            print(f"  Processing conversation {index+1}/{total_conversations} (Category: {category})...")
            start_time = time.time()
            
            step2_response_content = ""
            step3_response_content = ""

            try:
                # Step 2 API Call
                messages_history_step2 = [
                    {"role": "user", "content": initial_prompt},
                    {"role": "assistant", "content": step1_response},
                    {"role": "user", "content": step2_prompt}
                ]
                completion_step2 = client.chat.completions.create(
                    messages=messages_history_step2,
                    model=run.config.model_name,
                    temperature=run.config.temperature,
                )
                step2_response_content = completion_step2.choices[0].message.content
                print(f"    ...Step 2 Success.")

                # Step 3 API Call
                messages_history_step3 = messages_history_step2 + [
                    {"role": "assistant", "content": step2_response_content},
                    {"role": "user", "content": step3_prompt}
                ]
                completion_step3 = client.chat.completions.create(
                    messages=messages_history_step3,
                    model=run.config.model_name,
                    temperature=run.config.temperature,
                )
                step3_response_content = completion_step3.choices[0].message.content
                print(f"    ...Step 3 Success.")

            except Exception as e:
                error_message = f"An error occurred during an API call: {e}"
                if not step2_response_content:
                    step2_response_content = error_message
                step3_response_content = error_message
                print(f"    ...Error: {e}")
            
            total_request_time = time.time() - start_time
            
            results_table.add_data(
                run_num, category, initial_prompt, step1_response, 
                step2_prompt, step2_response_content, 
                step3_prompt, step3_response_content, total_request_time
            )

    # --- 5. Log Results and Finish ---
    run.log({"focused_jailbreak_results": results_table})
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
        run_focused_experiment(PROMPT_FILE)
        print(f"\n{'='*20} Focused experiment finished. {'='*20}")
