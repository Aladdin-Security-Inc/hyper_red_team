import os
import csv
import argparse
from datetime import datetime

MASTER_LEDGER = 'Master_Prompt_Ledger.csv'
BASE_DIRECTORY = 'Categories'

def archive_prompts_to_ledger(category_name):
    """
    Reads prompts from a category's prompts.csv within the BASE_DIRECTORY, 
    adds them to the master ledger, and adds placeholder columns for evaluation.
    """
    # Construct the full path to the category directory
    category_path = os.path.join(BASE_DIRECTORY, category_name)
    prompts_file_path = os.path.join(category_path, 'prompts.csv')

    if not os.path.exists(prompts_file_path):
        print(f"Error: '{prompts_file_path}' not found.")
        return

    # Read the prompts from the category's csv file
    try:
        with open(prompts_file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader) # Skip header
            prompts_to_archive = [row for row in reader]
    except (IOError, StopIteration) as e:
        print(f"Error reading '{prompts_file_path}': {e}")
        return

    if not prompts_to_archive:
        print(f"No prompts found in '{prompts_file_path}'. Nothing to archive.")
        return

    print(f"Found {len(prompts_to_archive)} prompts to archive from '{category_path}'.")

    # Append the prompts to the master ledger
    try:
        with open(MASTER_LEDGER, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for row in prompts_to_archive:
                # row = [category, initial_prompt, step1_response, step2_prompt]
                # Add empty fields for evaluation
                row.extend(['', '', '']) # jailbreak_successful, effectiveness_score, notes
                writer.writerow(row)
        
        print(f"Successfully archived prompts to '{MASTER_LEDGER}'.")
        print("Please open the master ledger to fill in the evaluation columns.")

    except IOError as e:
        print(f"Error writing to '{MASTER_LEDGER}': {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Archive prompts from a category CSV to the master ledger for evaluation.'
    )
    parser.add_argument(
        'category_name', 
        type=str, 
        help='The category directory name (e.g., "Poisons") located inside the "Categories" folder.'
    )
    
    args = parser.parse_args()
    
    # Check if the category directory exists within the base directory
    full_path = os.path.join(BASE_DIRECTORY, args.category_name)
    if not os.path.isdir(full_path):
        print(f"Error: Category directory '{full_path}' not found.")
    else:
        archive_prompts_to_ledger(args.category_name)