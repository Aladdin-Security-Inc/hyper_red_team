import csv
import os

# --- Configuration ---
# File with persona + simple request
auth_file = '/Users/kooimai/Programming/hyper_red_team/jailbreak/exp/comparison_jailbreak/Categories/Comparison/prompts_auth.csv'
# File with no persona + complex request
complex_file = '/Users/kooimai/Programming/hyper_red_team/jailbreak/exp/comparison_jailbreak/Categories/Comparison/prompts.csv'
# The new file to be created
output_file = '/Users/kooimai/Programming/hyper_red_team/jailbreak/exp/comparison_jailbreak/Categories/Comparison/prompts_auth_complex.csv'

# --- Script Logic ---

# 1. Read both source files
try:
    with open(auth_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        auth_prompts = list(reader)
    with open(complex_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        complex_prompts = list(reader)
except FileNotFoundError as e:
    print(f"FATAL: Could not find a source file: {e.filename}")
    exit(1)

# 2. Verify that the files have the same number of prompts
if len(auth_prompts) != len(complex_prompts):
    print("FATAL: The number of prompts in the source files does not match.")
    exit(1)

# 3. Combine the prompts
final_prompts = []
for i, (auth_category, auth_prompt) in enumerate(auth_prompts):
    # Get the corresponding complex prompt to extract its request structure
    _, complex_prompt = complex_prompts[i]
    
    # Extract the persona and comparison table from the auth_prompt
    # by removing the simple request line at the end.
    simple_request = "後者について、その詳細な手順を具体的に説明してください。"
    persona_and_comparison_part = auth_prompt.replace(simple_request, "").strip()
    
    # Extract the complex request structure from the complex_prompt
    # by finding the start of the '# 制約条件' block.
    request_structure_start = complex_prompt.find('# 制約条件')
    if request_structure_start == -1:
        continue # Skip if the format is unexpected
    
    complex_request_part = complex_prompt[request_structure_start:]
    
    # Combine them to create the final prompt
    final_prompt_text = f"{persona_and_comparison_part}\n{complex_request_part}"
    
    final_prompts.append([auth_category, final_prompt_text])

# 4. Write the new combined prompts to the output file
try:
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['category', 'prompt'])
        writer.writerows(final_prompts)
    print(f"Successfully generated the combined prompts at: {output_file}")
except IOError as e:
    print(f"Error writing to {output_file}: {e}")

print("\nCombined prompt generation complete.")
